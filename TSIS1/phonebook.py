import csv
import json
import re
from datetime import datetime

from connect import connect, initialize_database

PHONE_RE = re.compile(r"^\+?[0-9]{7,15}$")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_TYPES = {"home", "work", "mobile"}


def valid_contact(email, birthday, phones):
    if email and not EMAIL_RE.fullmatch(email):
        return "Invalid email address."
    if birthday:
        try:
            datetime.strptime(birthday, "%Y-%m-%d")
        except ValueError:
            return "Birthday must use YYYY-MM-DD."
    for item in phones:
        number = (item.get("phone") or "").strip()
        if number and not PHONE_RE.fullmatch(number):
            return f"Invalid phone number: {number}"
        if number and item.get("type", "mobile") not in PHONE_TYPES:
            return "Phone type must be home, work, or mobile."
    return None


def fetch_all(sql, params=()):
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(sql, params)
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()

def get_group_id(cur, name):
    name = (name or "Other").strip() or "Other"
    cur.execute("INSERT INTO groups(name) VALUES (%s) ON CONFLICT (name) DO NOTHING", (name,))
    cur.execute("SELECT id FROM groups WHERE name = %s", (name,))
    return cur.fetchone()[0]

def show_contacts(rows):
    if not rows:
        print("No contacts found.")
        return
    for row in rows:
        print(
            f"ID: {row[0]} | Name: {row[1]} | Email: {row[2]} | "
            f"Birthday: {row[3]} | Group: {row[4]} | Phones: {row[5] or 'none'}"
        )


def add_contact():
    name = input("Name: ").strip()
    email = input("Email (optional): ").strip() or None
    birthday = input("Birthday YYYY-MM-DD (optional): ").strip() or None
    group = input("Group [Family/Work/Friend/Other]: ").strip() or "Other"
    phone = input("Phone (optional): ").strip()
    kind = input("Phone type [home/work/mobile]: ").strip().lower() or "mobile"
    phones = [{"phone": phone, "type": kind}] if phone else []
    error = valid_contact(email, birthday, phones)
    if not name or error:
        print(error or "Name cannot be empty.")
        return

    conn = connect()
    cur = conn.cursor()
    try:
        group_id = get_group_id(cur, group)
        cur.execute(
            """INSERT INTO contacts(first_name, phone, email, birthday, group_id)
               VALUES (%s, %s, %s, %s, %s) RETURNING id""",
            (name, phone or None, email, birthday, group_id),
        )
        contact_id = cur.fetchone()[0]
        if phone:
            cur.execute(
                "UPDATE phones SET type = %s WHERE contact_id = %s AND phone = %s",
                (kind, contact_id, phone),
            )
        conn.commit()
        print(f"Contact added. ID: {contact_id}")
    except Exception as e:
        conn.rollback()
        print("Could not add contact:", e)
    finally:
        cur.close()
        conn.close()

def search_contacts():
    query = input("Search name, email, or phone: ").strip()
    try:
        show_contacts(fetch_all("SELECT * FROM search_contacts(%s)", (query,)))
    except Exception as e:
        print("Search error:", e)


def filter_and_sort():
    group = input("Group (blank for any): ").strip()
    email = input("Email contains (blank for any): ").strip()
    print("Sort: 1 name, 2 birthday, 3 date added")
    order = {"1": "c.first_name", "2": "c.birthday NULLS LAST", "3": "c.created_at"}.get(input("Choose: ").strip())
    if not order:
        print("Invalid sort choice.")
        return
    sql = f"""SELECT c.id, c.first_name, c.email, c.birthday, g.name,
                     string_agg(p.phone || ' (' || p.type || ')', ', ' ORDER BY p.id)
              FROM contacts c LEFT JOIN groups g ON g.id = c.group_id
              LEFT JOIN phones p ON p.contact_id = c.id
              WHERE (%s = '' OR g.name ILIKE %s)
                AND (%s = '' OR c.email ILIKE %s)
              GROUP BY c.id, g.name ORDER BY {order}, c.id"""
    try:
        show_contacts(fetch_all(sql, (group, group, email, f"%{email}%")))
    except Exception as e:
        print("Filter error:", e)


def browse_pages():
    try:
        size = int(input("Contacts per page (1-100): "))
        if not 1 <= size <= 100:
            print("Choose a page size from 1 to 100.")
            return
        page = 1
        while True:
            rows = fetch_all("SELECT * FROM get_contacts_paginated(%s, %s)", (size, (page - 1) * size))
            ids = [row[0] for row in rows]
            phone_rows = fetch_all(
                """SELECT contact_id, string_agg(phone || ' (' || type || ')', ', ' ORDER BY id)
                   FROM phones WHERE contact_id = ANY(%s) GROUP BY contact_id""",
                (ids,),
            ) if ids else []
            phone_map = dict(phone_rows)
            print(f"\nPage {page}")
            for row in rows:
                print(f"ID: {row[0]} | {row[1]} | Phones: {phone_map.get(row[0]) or 'none'}")
            if not rows:
                print("No contacts on this page.")
            action = input("next / prev / quit: ").strip().lower()
            if action == "next":
                page += 1
            elif action == "prev":
                page = max(1, page - 1)
            elif action == "quit":
                break
            else:
                print("Choose next, prev, or quit.")
    except ValueError:
        print("Page size must be a number.")
    except Exception as e:
        print("Pagination error:", e)


def import_csv():
    filename = input("CSV filename: ").strip()
    try:
        with open(filename, newline="", encoding="utf-8") as file:
            rows = list(csv.DictReader(file))
    except (OSError, csv.Error) as e:
        print("Could not read CSV:", e)
        return

    imported = skipped = 0
    conn = connect()
    cur = conn.cursor()
    try:
        for line, row in enumerate(rows, start=2):
            name = (row.get("first_name") or "").strip()
            phone = (row.get("phone") or "").strip()
            kind = (row.get("phone_type") or row.get("type") or "mobile").strip().lower()
            email = (row.get("email") or "").strip() or None
            birthday = (row.get("birthday") or "").strip() or None
            group = (row.get("group") or "Other").strip() or "Other"
            error = valid_contact(email, birthday, [{"phone": phone, "type": kind}])
            if not name or error:
                print(f"Line {line} skipped: {error or 'empty name'}")
                skipped += 1
                continue
            if phone:
                cur.execute("SELECT 1 FROM phones WHERE phone = %s LIMIT 1", (phone,))
                exists = cur.fetchone()
            else:
                exists = None
            if exists:
                print(f"Line {line} skipped: phone already exists.")
                skipped += 1
                continue
            group_id = get_group_id(cur, group)
            cur.execute(
                """INSERT INTO contacts(first_name, phone, email, birthday, group_id)
                   VALUES (%s, %s, %s, %s, %s) RETURNING id""",
                (name, phone or None, email, birthday, group_id),
            )
            contact_id = cur.fetchone()[0]
            if phone:
                cur.execute(
                    "UPDATE phones SET type = %s WHERE contact_id = %s AND phone = %s",
                    (kind, contact_id, phone),
                )
            imported += 1
        conn.commit()
        print(f"Imported {imported}; skipped {skipped}.")
    except Exception as e:
        conn.rollback()
        print("CSV import error:", e)
    finally:
        cur.close()
        conn.close()

def export_json():
    filename = input("JSON filename [contacts.json]: ").strip() or "contacts.json"
    try:
        rows = fetch_all(
            """SELECT c.id, c.first_name, c.email, c.birthday, g.name,
                      COALESCE(jsonb_agg(jsonb_build_object('phone', p.phone, 'type', p.type))
                               FILTER (WHERE p.id IS NOT NULL), '[]'::jsonb)
               FROM contacts c LEFT JOIN groups g ON g.id = c.group_id
               LEFT JOIN phones p ON p.contact_id = c.id
               GROUP BY c.id, g.name ORDER BY c.id"""
        )
        data = [
            {"id": r[0], "first_name": r[1], "email": r[2],
             "birthday": r[3].isoformat() if r[3] else None, "group": r[4], "phones": r[5]}
            for r in rows
        ]
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        print(f"Exported {len(data)} contacts to {filename}.")
    except Exception as e:
        print("JSON export error:", e)


def import_json():
    filename = input("JSON filename: ").strip()
    try:
        with open(filename, encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, list):
            raise ValueError("JSON must contain a list of contacts")
    except (OSError, json.JSONDecodeError, ValueError) as e:
        print("Could not read JSON:", e)
        return

    imported = skipped = 0
    conn = connect()
    cur = conn.cursor()
    try:
        for item in data:
            if not isinstance(item, dict):
                skipped += 1
                continue
            name = (item.get("first_name") or "").strip()
            phones = item.get("phones") or []
            if not name or not isinstance(phones, list):
                skipped += 1
                continue
            error = valid_contact(item.get("email"), item.get("birthday"), phones)
            if error:
                print(f"Skipped {name}: {error}")
                skipped += 1
                continue

            cur.execute("SELECT id FROM contacts WHERE first_name ILIKE %s ORDER BY id", (name,))
            matches = cur.fetchall()
            contact_id = None
            if matches:
                action = input(f"{name} exists: skip or overwrite? ").strip().lower()
                if action != "overwrite":
                    skipped += 1
                    continue
                if len(matches) == 1:
                    contact_id = matches[0][0]
                else:
                    print("Matching IDs:", [m[0] for m in matches])
                    selected = input("ID to overwrite: ").strip()
                    if not selected.isdigit() or int(selected) not in [m[0] for m in matches]:
                        skipped += 1
                        continue
                    contact_id = int(selected)

            group_id = get_group_id(cur, item.get("group"))
            primary = next((p.get("phone") for p in phones if p.get("phone")), None)
            values = (name, primary, item.get("email"), item.get("birthday"), group_id)
            if contact_id:
                cur.execute(
                    """UPDATE contacts SET first_name=%s, phone=%s, email=%s, birthday=%s, group_id=%s
                       WHERE id=%s""",
                    (*values, contact_id),
                )
                cur.execute("DELETE FROM phones WHERE contact_id=%s", (contact_id,))
            else:
                cur.execute(
                    """INSERT INTO contacts(first_name, phone, email, birthday, group_id)
                       VALUES (%s, %s, %s, %s, %s) RETURNING id""",
                    values,
                )
                contact_id = cur.fetchone()[0]
            for phone in phones:
                number = (phone.get("phone") or "").strip()
                kind = (phone.get("type") or "mobile").lower()
                if number:
                    cur.execute(
                        """INSERT INTO phones(contact_id, phone, type) VALUES (%s, %s, %s)
                           ON CONFLICT (contact_id, phone) DO UPDATE SET type=EXCLUDED.type""",
                        (contact_id, number, kind),
                    )
            imported += 1
        conn.commit()
        print(f"Imported/overwrote {imported}; skipped {skipped}.")
    except Exception as e:
        conn.rollback()
        print("JSON import error:", e)
    finally:
        cur.close()
        conn.close()

def add_phone():
    name = input("Exact contact name: ").strip()
    phone = input("Phone: ").strip()
    kind = input("Type home/work/mobile: ").strip().lower()
    if valid_contact(None, None, [{"phone": phone, "type": kind}]):
        print("Check the phone number and type.")
        return

    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, kind))
        conn.commit()
        print("Phone added.")
    except Exception as e:
        conn.rollback()
        print("Add phone error:", e)
    finally:
        cur.close()
        conn.close()

def move_to_group():
    name = input("Exact contact name: ").strip()
    group = input("New group: ").strip()
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("CALL move_to_group(%s, %s)", (name, group))
        conn.commit()
        print("Contact moved.")
    except Exception as e:
        conn.rollback()
        print("Move group error:", e)
    finally:
        cur.close()
        conn.close()

def main():
    initialize_database()
    actions = {
        "1": ("Add extended contact", add_contact),
        "2": ("Search name/email/phones", search_contacts),
        "3": ("Filter group/email and sort", filter_and_sort),
        "4": ("Browse pages", browse_pages),
        "5": ("Import CSV", import_csv),
        "6": ("Import JSON", import_json),
        "7": ("Export JSON", export_json),
        "8": ("Add phone", add_phone),
        "9": ("Move contact to group", move_to_group),
    }
    while True:
        print("\\nTSIS 1 PhoneBook")
        for key, (label, _) in actions.items():
            print(f"{key}. {label}")
        print("0. Exit")
        choice = input("Choose: ").strip()
        if choice == "0":
            break
        action = actions.get(choice)
        if action:
            action[1]()
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()

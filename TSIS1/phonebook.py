import csv
import json
import re
from datetime import datetime

from connect import connect, initialize_database

PHONE_RE = re.compile(r"^\+?[0-9]{7,15}$")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_valid_phone(phone):
    return bool(PHONE_RE.match(phone or ""))


def is_valid_email(email):
    return not email or bool(EMAIL_RE.match(email))


def is_valid_date(value):
    if not value:
        return True
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_contact_fields(email, birthday, phones):
    """Return an error text, or None if everything is valid."""
    if not is_valid_email(email):
        return "invalid email"
    if not is_valid_date(birthday):
        return "birthday must be YYYY-MM-DD"
    for item in phones:
        number = (item.get("phone") or "").strip()
        if number and not is_valid_phone(number):
            return f"invalid phone {number}"
    return None


def escape_like(text):
    """Escape % and _ so they are searched as ordinary characters."""
    return text.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def confirm(question):
    return input(f"{question} (yes/no): ").strip().lower() in ("yes", "y")


def print_contacts(rows):
    for contact_id, name, phones in rows:
        print(f"ID: {contact_id}, Name: {name}, Phones: {phones or 'No phone'}")


# 1. Add a new contact

def choose_contact_id(contacts):
    """Return the selected contact ID, or None when no match is chosen."""
    if not contacts:
        return None
    if len(contacts) == 1:
        return contacts[0][0]

    print("Several contacts match:")
    for contact_id, name, phone in contacts:
        print(f"ID: {contact_id}, Name: {name}, Phone: {phone}")
    selected = input("Enter the ID of the contact: ").strip()
    if not selected.isdigit() or int(selected) not in {row[0] for row in contacts}:
        print("That ID is not in the list.")
        return None
    return int(selected)


def find_matching_contacts(name=None, phone=None):
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            """SELECT id, first_name, phone FROM contacts
               WHERE (%s::VARCHAR IS NOT NULL AND first_name = %s)
                  OR (%s::VARCHAR IS NOT NULL AND phone = %s)
               ORDER BY id""",
            (name, name, phone, phone),
        )
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()


def save_contact(name, phone):
    if not name or not phone:
        print("Name and phone cannot be empty!")
        return

    try:
        matches = find_matching_contacts(name=name, phone=phone)
        contact_id = choose_contact_id(matches)
        if len(matches) > 1 and contact_id is None:
            return
        conn = connect()
        cur = conn.cursor()
        try:
            cur.execute("CALL upsert_contact(%s, %s, %s)", (name, phone, contact_id))
            conn.commit()
            cur.execute(
                "SELECT id, first_name, phone FROM contacts WHERE phone = %s",
                (phone,),
            )
            saved_contact = cur.fetchone()
            print("Contact added or updated successfully!")
            if saved_contact:
                print(
                    f"ID: {saved_contact[0]}, Name: {saved_contact[1]}, "
                    f"Phone: {saved_contact[2]}"
                )
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close()
            conn.close()
    except Exception as e:
        print("Error saving contact:", e)


def add_contact():
    name = input("Enter first name: ").strip()
    phone = input("Enter phone number: ").strip()
    save_contact(name, phone)


# 2. Import contacts from CSV

def import_csv():
    filename = input("Enter CSV filename: ").strip()
    try:
        with open(filename, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            conn = connect()
            cur = conn.cursor()
            try:
                imported = 0
                skipped = 0
                for line_no, row in enumerate(reader, start=2):
                    name = (row.get("first_name") or "").strip()
                    phone = (row.get("phone") or "").strip()
                    email = (row.get("email") or "").strip() or None
                    birthday = (row.get("birthday") or "").strip() or None
                    group_name = (row.get("group") or "Other").strip() or "Other"
                    phone_type = (row.get("phone_type") or row.get("type") or "mobile").strip().lower()

                    if not name:
                        print(f"Line {line_no} skipped: empty name")
                        skipped += 1
                        continue
                    error = validate_contact_fields(email, birthday, [{"phone": phone}])
                    if error:
                        print(f"Line {line_no} skipped: {error}")
                        skipped += 1
                        continue
                    if phone_type not in ("home", "work", "mobile"):
                        print(f"Line {line_no} skipped: invalid phone_type")
                        skipped += 1
                        continue
                    if phone:
                        cur.execute("SELECT 1 FROM phones WHERE phone = %s LIMIT 1", (phone,))
                        if cur.fetchone():
                            print(f"Line {line_no} skipped: phone {phone} already exists")
                            skipped += 1
                            continue

                    group_id = get_or_create_group(cur, group_name)
                    cur.execute(
                        """INSERT INTO contacts(first_name, phone, email, birthday, group_id)
                           VALUES (%s, %s, %s, %s, %s) RETURNING id""",
                        (name, phone or None, email, birthday, group_id),
                    )
                    contact_id = cur.fetchone()[0]
                    if phone:
                        cur.execute(
                            """INSERT INTO phones(contact_id, phone, type)
                               VALUES (%s, %s, %s)
                               ON CONFLICT (contact_id, phone) DO UPDATE SET type = EXCLUDED.type""",
                            (contact_id, phone, phone_type),
                        )
                    imported += 1
                conn.commit()
                print(f"Imported {imported} contacts, skipped {skipped}.")
            except Exception:
                conn.rollback()
                raise
            finally:
                cur.close()
                conn.close()
    except FileNotFoundError:
        print("CSV file not found.")
    except Exception as e:
        print("CSV import error:", e)

# 3. Update contact by ID

def update_contact():
    contact_id = input("Enter contact ID: ").strip()
    new_name = input("Enter new first name: ").strip()
    new_phone = input("Enter new phone: ").strip()

    if not contact_id.isdigit():
        print("ID must be a number!")
        return
    if not new_name:
        print("Name cannot be empty!")
        return
    if not is_valid_phone(new_phone):
        print("Invalid phone. Use 7-15 digits, optionally starting with +.")
        return

    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE contacts SET first_name = %s, phone = %s WHERE id = %s RETURNING id",
            (new_name, new_phone, int(contact_id)),
        )
        result = cur.fetchone()
        conn.commit()
        print("Contact updated successfully!" if result else "Contact not found.")
    except Exception as e:
        conn.rollback()
        print("Update error:", e)
    finally:
        cur.close()
        conn.close()


# 4. Search by name
def search_by_name():
    name = input("Enter first name: ").strip()

    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT c.id, c.first_name,
                   COALESCE(string_agg(p.phone || ' (' || p.type || ')', ', ' ORDER BY p.id), '')
            FROM contacts c
            LEFT JOIN phones p ON p.contact_id = c.id
            WHERE c.first_name ILIKE %s
            GROUP BY c.id, c.first_name
            ORDER BY c.id
            """,
            ("%" + escape_like(name) + "%",),
        )
        rows = cur.fetchall()
        if rows:
            print_contacts(rows)
        else:
            print("No contacts found.")
    except Exception as e:
        print("Search error:", e)
    finally:
        cur.close()
        conn.close()




# 5. Search by phone prefix

def search_by_prefix():
    prefix = input("Enter phone prefix: ").strip()
    if not prefix:
        print("Prefix cannot be empty.")
        return

    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT c.id, c.first_name,
                   COALESCE(string_agg(p.phone || ' (' || p.type || ')', ', ' ORDER BY p.id), '')
            FROM contacts c
            LEFT JOIN phones p ON p.contact_id = c.id
            WHERE EXISTS (
                SELECT 1 FROM phones px
                WHERE px.contact_id = c.id AND px.phone LIKE %s
            )
            GROUP BY c.id, c.first_name
            ORDER BY c.id
            """,
            (escape_like(prefix) + "%",),
        )
        rows = cur.fetchall()
        if rows:
            print_contacts(rows)
        else:
            print("No contacts found.")
    except Exception as e:
        print("Search error:", e)
    finally:
        cur.close()
        conn.close()



# 6. Delete contact by ID

def delete_contact_by_id():
    contact_id = input("Enter contact ID: ").strip()
    if not contact_id.isdigit():
        print("ID must be a number!")
        return

    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT first_name, phone FROM contacts WHERE id = %s",
            (int(contact_id),),
        )
        row = cur.fetchone()
        if not row:
            print("Contact not found.")
            return
        if not confirm(f"Delete {row[0]} ({row[1] or 'no phone'})?"):
            print("Cancelled.")
            return

        cur.execute("DELETE FROM contacts WHERE id = %s", (int(contact_id),))
        conn.commit()
        print("Contact deleted successfully!")
    except Exception as e:
        conn.rollback()
        print("Delete error:", e)
    finally:
        cur.close()
        conn.close()

# 8. Search by pattern using FUNCTION

def search_by_pattern():
    pattern = input("Enter name or phone pattern: ").strip()

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            SELECT *
            FROM search_contacts(%s)
            """,
            (pattern,)
        )

        contacts = cur.fetchall()

        if contacts:
            print("\n--- SEARCH RESULTS ---")

            for contact in contacts:
                print(
                    f"ID: {contact[0]}, Name: {contact[1]}, Email: {contact[2]}, "
                    f"Birthday: {contact[3]}, Group: {contact[4]}, Phones: {contact[5]}"
                )
        else:
            print("No contacts found.")

    except Exception as e:
        print("Search error:", e)

    finally:
        cur.close()
        conn.close()


# 9. Insert or update using PROCEDURE

def upsert_contact_python():
    name = input("Enter first name: ").strip()
    phone = input("Enter phone: ").strip()
    save_contact(name, phone)


# 10. Insert many contacts using PROCEDURE

def bulk_insert_contacts():
    try:
        count = int(input("How many contacts do you want to add? "))

        if count <= 0:
            print("Enter a positive number.")
            return

    except ValueError:
        print("Please enter a valid number.")
        return

    contacts = []

    for i in range(count):
        print(f"\nContact {i + 1}")

        name = input("Enter first name: ").strip()
        phone = input("Enter phone: ").strip()

        contacts.append({
            "first_name": name,
            "phone": phone
        })

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            CALL insert_many_contacts(
                %s::jsonb,
                %s::jsonb
            )
            """,
            (json.dumps(contacts), "[]")
        )

        result = cur.fetchone()
        conn.commit()

        invalid_contacts = result[0]

        if invalid_contacts:
            print("\n--- INCORRECT CONTACTS ---")

            for contact in invalid_contacts:
                print(contact)
        else:
            print("All contacts processed successfully!")

    except Exception as e:
        conn.rollback()
        print("Bulk insert error:", e)

    finally:
        cur.close()
        conn.close()


# 11. Pagination using FUNCTION

def show_contacts_paginated():
    try:
        limit = int(input("Contacts per page (1-100): "))
        if not 1 <= limit <= 100:
            print("Page size must be from 1 to 100.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    page = 1
    while True:
        conn = connect()
        cur = conn.cursor()
        try:
            cur.execute(
                "SELECT * FROM get_contacts_paginated(%s, %s)",
                (limit, (page - 1) * limit),
            )
            contacts = cur.fetchall()

            print(f"\n--- Page {page} ---")
            if contacts:
                contact_ids = [contact[0] for contact in contacts]
                cur.execute(
                    """SELECT contact_id,
                              string_agg(phone || ' (' || type || ')', ', ' ORDER BY id)
                       FROM phones
                       WHERE contact_id = ANY(%s)
                       GROUP BY contact_id""",
                    (contact_ids,),
                )
                phone_map = dict(cur.fetchall())

                for contact in contacts:
                    phones = phone_map.get(contact[0]) or contact[2] or "No phone"
                    print(f"ID: {contact[0]}, Name: {contact[1]}, Phones: {phones}")
            else:
                print("No contacts on this page.")
        except Exception as e:
            print("Pagination error:", e)
            return
        finally:
            cur.close()
            conn.close()

        command = input("Type next, prev, or quit: ").strip().lower()
        if command == "next":
            page += 1
        elif command == "prev":
            page = max(1, page - 1)
        elif command == "quit":
            break
        else:
            print("Please type next, prev, or quit.")


# 12. Delete by name or phone using PROCEDURE

def delete_by_name_or_phone():
    print("\n1. Delete by name")
    print("2. Delete by phone")
    choice = input("Choose option: ").strip()
    if choice == "1":
        name = input("Enter exact first name: ").strip()
        if not name:
            print("Name cannot be empty.")
            return
        matches = find_matching_contacts(name=name)
    elif choice == "2":
        phone = input("Enter exact phone number: ").strip()
        if not phone:
            print("Phone cannot be empty.")
            return
        matches = find_matching_contacts(phone=phone)
    else:
        print("Invalid choice.")
        return

    if not matches:
        print("No matching contact found.")
        return
    contact_id = choose_contact_id(matches)
    if contact_id is None:
        return
    chosen = next(m for m in matches if m[0] == contact_id)
    
    if not confirm(f"Delete {chosen[1]} ({chosen[2]})?"):
        print("Cancelled.")
        return

    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("CALL delete_contact(NULL, NULL, %s)", (contact_id,))
        conn.commit()
        print(f"Contact with ID {contact_id} deleted successfully!")
    except Exception as e:
        conn.rollback()
        print("Delete error:", e)
    finally:
        cur.close()
        conn.close()



def get_or_create_group(cur, group_name):
    group_name = (group_name or "Other").strip() or "Other"
    cur.execute("INSERT INTO groups(name) VALUES (%s) ON CONFLICT (name) DO NOTHING", (group_name,))
    cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
    return cur.fetchone()[0]


def add_extended_contact():
    name = input("Name: ").strip()
    email = input("Email (optional): ").strip() or None
    birthday = input("Birthday YYYY-MM-DD (optional): ").strip() or None
    group_name = input("Group Family/Work/Friend/Other: ").strip() or "Other"
    phone = input("First phone (optional): ").strip()
    phone_type = input("Phone type home/work/mobile: ").strip().lower() or "mobile"
    if not name:
        if not name:
           print("Name cannot be empty.")
        return
    error = validate_contact_fields(email, birthday, [{"phone": phone}])
    if error:
        print("Cannot add contact:", error)
        return
    if phone and phone_type not in ("home", "work", "mobile"):
        print("Phone type must be home, work, or mobile.")
        return
    conn = connect()
    cur = conn.cursor()
    try:
        group_id = get_or_create_group(cur, group_name)
        cur.execute("""INSERT INTO contacts(first_name, phone, email, birthday, group_id)
                       VALUES (%s, %s, %s, %s, %s) RETURNING id""",
                    (name, phone or None, email, birthday, group_id))
        contact_id = cur.fetchone()[0]
        if phone:
            cur.execute("UPDATE phones SET type = %s WHERE contact_id = %s AND phone = %s",
                        (phone_type, contact_id, phone))
        conn.commit()
        print(f"Contact created. ID: {contact_id}")
    except Exception as e:
        conn.rollback()
        print("Could not add contact:", e)
    finally:
        cur.close()
        conn.close()


def advanced_filter_sort():
    group_name = input("Group name (blank = any): ").strip()
    email_query = input("Email contains (blank = any): ").strip()
    print("Sort by: 1 name, 2 birthday, 3 date added")
    sort_choice = input("Choose sort: ").strip()
    order_by = {"1": "c.first_name", "2": "c.birthday NULLS LAST", "3": "c.created_at"}.get(sort_choice)
    if not order_by:
        print("Invalid sort choice.")
        return
    conn = connect()
    cur = conn.cursor()
    try:
        query = f"""SELECT c.id, c.first_name, c.email, c.birthday, g.name,
                           COALESCE(string_agg(p.phone || ' (' || p.type || ')', ', ' ORDER BY p.id), '')
                    FROM contacts c LEFT JOIN groups g ON g.id = c.group_id
                    LEFT JOIN phones p ON p.contact_id = c.id
                    WHERE (%s = '' OR g.name ILIKE %s)
                      AND (%s = '' OR COALESCE(c.email, '') ILIKE %s)
                    GROUP BY c.id, g.name ORDER BY {order_by}, c.id"""
        cur.execute(query, (group_name, group_name, email_query, f"%{email_query}%"))
        rows = cur.fetchall()
        if not rows:
            print("No matching contacts.")
        for r in rows:
            print(f"ID: {r[0]} | {r[1]} | Email: {r[2]} | Birthday: {r[3]} | Group: {r[4]} | Phones: {r[5]}")
    except Exception as e:
        print("Filter/search error:", e)
    finally:
        cur.close()
        conn.close()


def export_json():
    filename = input("JSON output filename (for example contacts.json): ").strip() or "contacts.json"
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("""SELECT c.id, c.first_name, c.email, c.birthday, g.name,
                              COALESCE(jsonb_agg(jsonb_build_object('phone', p.phone, 'type', p.type))
                                       FILTER (WHERE p.id IS NOT NULL), '[]'::jsonb)
                       FROM contacts c LEFT JOIN groups g ON g.id = c.group_id
                       LEFT JOIN phones p ON p.contact_id = c.id
                       GROUP BY c.id, g.name ORDER BY c.id""")
        data = [{"id": r[0], "first_name": r[1], "email": r[2],
                 "birthday": r[3].isoformat() if r[3] else None,
                 "group": r[4], "phones": r[5]} for r in cur.fetchall()]
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        print(f"Exported {len(data)} contacts to {filename}.")
    except Exception as e:
        print("JSON export error:", e)
    finally:
        cur.close()
        conn.close()


def import_json():
    filename = input("JSON input filename: ").strip()
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, list):
            print("JSON must contain a list of contacts.")
            return
    except Exception as e:
        print("Could not read JSON:", e)
        return

    conn = connect()
    cur = conn.cursor()
    imported = 0
    try:
        for item in data:
            name = (item.get("first_name") or "").strip()
            if not name:
                print("Skipped a contact without a name.")
                continue
            cur.execute("SELECT id FROM contacts WHERE first_name = %s ORDER BY id", (name,))
            matches = cur.fetchall()
            contact_id = None
            if matches:
                action = input(f"Contact '{name}' exists. Skip or overwrite? ").strip().lower()
                if action == "skip":
                    continue
                if action != "overwrite":
                    print("Skipped: answer must be skip or overwrite.")
                    continue
                if len(matches) == 1:
                    contact_id = matches[0][0]
                else:
                    print("Matching IDs:", [m[0] for m in matches])
                    selected = input("ID to overwrite: ").strip()
                    if not selected.isdigit() or int(selected) not in [m[0] for m in matches]:
                        print("Skipped: invalid ID.")
                        continue
                    contact_id = int(selected)
            group_id = get_or_create_group(cur, item.get("group") or "Other")
            phones = item.get("phones") or []
            primary_phone = next((x.get("phone") for x in phones if x.get("phone")), None)
            if contact_id is None:
                cur.execute("""INSERT INTO contacts(first_name, phone, email, birthday, group_id)
                               VALUES (%s, %s, %s, %s, %s) RETURNING id""",
                            (name, primary_phone, item.get("email"), item.get("birthday"), group_id))
                contact_id = cur.fetchone()[0]
            else:
                cur.execute("""UPDATE contacts SET first_name=%s, phone=%s, email=%s,
                               birthday=%s, group_id=%s WHERE id=%s""",
                            (name, primary_phone, item.get("email"), item.get("birthday"), group_id, contact_id))
                cur.execute("DELETE FROM phones WHERE contact_id=%s", (contact_id,))
            for phone_item in phones:
                number = (phone_item.get("phone") or "").strip()
                kind = (phone_item.get("type") or "mobile").lower()
                if number and kind in ("home", "work", "mobile"):
                    cur.execute("""INSERT INTO phones(contact_id, phone, type) VALUES (%s,%s,%s)
                                   ON CONFLICT (contact_id, phone) DO UPDATE SET type = EXCLUDED.type""",
                                (contact_id, number, kind))
            imported += 1
        conn.commit()
        print(f"Imported/overwrote {imported} contacts.")
    except Exception as e:
        conn.rollback()
        print("JSON import error:", e)
    finally:
        cur.close()
        conn.close()


def add_phone_to_contact():
    name = input("Exact contact name: ").strip()
    phone = input("New phone number: ").strip()
    kind = input("Type home/work/mobile: ").strip().lower()
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


def move_contact_to_group():
    name = input("Exact contact name: ").strip()
    group_name = input("New group name: ").strip()
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("CALL move_to_group(%s, %s)", (name, group_name))
        conn.commit()
        print("Contact moved to group.")
    except Exception as e:
        conn.rollback()
        print("Move group error:", e)
    finally:
        cur.close()
        conn.close()


def main():
    initialize_database()

    while True:

        print("\n========== PHONEBOOK ==========")

        print("1. Add contact")
        print("2. Import contacts from CSV")
        print("3. Update contact")
        print("4. Search by name")
        print("5. Search by phone prefix")
        print("6. Delete contact by ID")
        print("7. Show all contacts")

    
        print("8. Search by pattern")
        print("9. Insert or update contact")
        print("10. Insert many contacts")
        print("11. Navigate pages (next/prev/quit)")
        print("12. Delete by name or phone")
        print("13. Add extended contact")
        print("14. Filter by group/email and sort")
        print("15. Export contacts to JSON")
        print("16. Import contacts from JSON")
        print("17. Add phone to contact")
        print("18. Move contact to group")

        print("\n0. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            add_contact()

        elif choice == "2":
            import_csv()

        elif choice == "3":
            update_contact()

        elif choice == "4":
            search_by_name()

        elif choice == "5":
            search_by_prefix()

        elif choice == "6":
            delete_contact_by_id()

        elif choice == "7":
            show_contacts()

        elif choice == "8":
            search_by_pattern()
            input("\nPress Enter to return to the menu...")

        elif choice == "9":
            upsert_contact_python()
            input("\nPress Enter to return to the menu...")

        elif choice == "10":
            bulk_insert_contacts()

        elif choice == "11":
            show_contacts_paginated()
            input("\nPress Enter to return to the menu...")

        elif choice == "12":
            delete_by_name_or_phone()

        elif choice == "13":
            add_extended_contact()

        elif choice == "14":
            advanced_filter_sort()

        elif choice == "15":
            export_json()

        elif choice == "16":
            import_json()

        elif choice == "17":
            add_phone_to_contact()

        elif choice == "18":
            move_contact_to_group()

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

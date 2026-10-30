import csv
from connect import connect, create_table
# 1. Add a new contact
def add_contact():
    first_name = input("Enter first name: ").strip()
    phone = input("Enter phone number: ").strip()
    if not first_name or not phone:
        print("Name and phone cannot be empty!")
        return
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO contacts (first_name, phone) VALUES (%s, %s)",
            (first_name, phone)
        )
        conn.commit()
        print("Contact added successfully!")
    except Exception as e:
        conn.rollback()
        print("Error adding contact:", e)
    finally:
        cur.close()
        conn.close()
# 2. Import contacts from CSV
def import_csv():
    filename = input("Enter CSV filename (example: contacts.csv): ").strip()
    try:
        with open(filename, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            conn = connect()
            cur = conn.cursor()
            try:
                for row in reader:
                    first_name = row.get("first_name", "").strip()
                    phone = row.get("phone", "").strip()
                    if first_name and phone:
                        cur.execute(
                            """
                            INSERT INTO contacts (first_name, phone)
                            VALUES (%s, %s)
                            ON CONFLICT (phone) DO NOTHING
                            """,
                            (first_name, phone)
                        )
                conn.commit()
                print("CSV imported successfully!")
            except Exception as e:
                conn.rollback()
                print("Error importing contacts:", e)
            finally:
                cur.close()
                conn.close()
    except FileNotFoundError:
        print("File not found. Check the filename and try again.")
    except Exception as e:
        print("Error reading CSV:", e)
# 3. Update a contact
def update_contact():
    contact_id = input("Enter contact ID: ").strip()
    new_name = input("Enter new first name: ").strip()
    new_phone = input("Enter new phone number: ").strip()
    if not contact_id.isdigit():
        print("ID must be a number!")
        return
    if not new_name or not new_phone:
        print("Name and phone cannot be empty!")
        return
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            UPDATE contacts
            SET first_name = %s, phone = %s
            WHERE id = %s
            RETURNING id
            """,
            (new_name, new_phone, int(contact_id))
        )
        result = cur.fetchone()
        conn.commit()
        if result:
            print("Contact updated successfully!")
        else:
            print("Contact not found.")
    except Exception as e:
        conn.rollback()
        print("Error updating contact:", e)
    finally:
        cur.close()
        conn.close()
# 4. Search contacts by name
def search_by_name():
    name = input("Enter first name to search: ").strip()
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id, first_name, phone FROM contacts WHERE first_name ILIKE %s",
            ("%" + name + "%",)
        )
        contacts = cur.fetchall()
        if contacts:
            for contact in contacts:
                print(
                    f"ID: {contact[0]}, "
                    f"Name: {contact[1]}, "
                    f"Phone: {contact[2]}"
                )
        else:
            print("No contacts found.")
    except Exception as e:
        print("Search error:", e)
    finally:
        cur.close()
        conn.close()
# 5. Search contacts by phone prefix
def search_by_prefix():
    prefix = input("Enter phone prefix: ").strip()
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id, first_name, phone FROM contacts WHERE phone LIKE %s",
            (prefix + "%",)
        )
        contacts = cur.fetchall()
        if contacts:
            for contact in contacts:
                print(
                    f"ID: {contact[0]}, "
                    f"Name: {contact[1]}, "
                    f"Phone: {contact[2]}"
                )
        else:
            print("No contacts found.")
    except Exception as e:
        print("Search error:", e)
    finally:
        cur.close()
        conn.close()
# 6. Delete a contact
def delete_contact():
    contact_id = input("Enter contact ID to delete: ").strip()
    if not contact_id.isdigit():
        print("ID must be a number!")
        return
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            "DELETE FROM contacts WHERE id = %s RETURNING id",
            (int(contact_id),)
        )
        result = cur.fetchone()
        conn.commit()
        if result:
            print("Contact deleted successfully!")
        else:
            print("Contact not found.")
    except Exception as e:
        conn.rollback()
        print("Error deleting contact:", e)
    finally:
        cur.close()
        conn.close()
# 7. Show all contacts
def show_contacts():
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id, first_name, phone FROM contacts ORDER BY id"
        )
        contacts = cur.fetchall()
        if contacts:
            print("\n--- PhoneBook Contacts ---")
            for contact in contacts:
                print(
                    f"ID: {contact[0]}, "
                    f"Name: {contact[1]}, "
                    f"Phone: {contact[2]}"
                )
        else:
            print("PhoneBook is empty.")
    except Exception as e:
        print("Error displaying contacts:", e)
    finally:
        cur.close()
        conn.close()
# Main menu
def main():
    create_table()
    while True:
        print("\n========== PHONEBOOK ==========")
        print("1. Add contact")
        print("2. Import contacts from CSV")
        print("3. Update contact")
        print("4. Search by name")
        print("5. Search by phone prefix")
        print("6. Delete contact")
        print("7. Show all contacts")
        print("0. Exit")
        choice = input("Choose an option: ").strip()
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
            delete_contact()
        elif choice == "7":
            show_contacts()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
    main()




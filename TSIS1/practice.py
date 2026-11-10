# #search by email

# def search_by_email():
#     email=input().strip()
#     conn=connect()
#     cur=conn.cursor()
#     try:
#         cur.execute(
#             "Select id, first_name, email From contacts Where email ILIKE %s Order by id ",
#             ("%"+email+"%",),
#         )
#         rows=cur.fetchall()
#         for r in row:
#             print(f"Id: {r[0]}, Name: {r[1]}, email: {r[3]}")
#         if not rows:
#             print("Nothing found.")
#     except Exception as e:
#         print("Error:",e)
#     finally:
#         cur.close()
#         conn.close()

#посчитать контакты
def count_contact():
    conn=connect()
    cur=conn.cursor()

    try:
        cur.excecute("Select count(*) from contacts")
        print("Total contacts:",cur.fetchone()[0])
    except Exception as e:
        print("error:",e) 
    finally:
        cur.close()
        conn.close()
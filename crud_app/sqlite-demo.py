import sqlite3


conn = sqlite3.connect('test.db')
cursor = conn.cursor()

# List all tables in database
cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
table = cursor.fetchall()
print("Tables:", table)


# Query from the first table 
if table:
    table_name = table[0][0]
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()
    for row in rows:
        print(row)


conn.close()

import sqlite3
connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table_query = "CREATE TABLE IF NOT EXISTS items (name text, price real)"
create_table_query2 = "CREATE TABLE IF NOT EXISTS users (id INTEGER, username text, password text)"
cursor.execute(create_table_query)
cursor.execute(create_table_query2)
cursor.execute("INSERT INTO  items VALUES ('test', '10.99')")

connection.commit()
connection.close()

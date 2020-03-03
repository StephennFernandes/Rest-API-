import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()
create_table = "CREATE TABLE users (id int, username text, passowrd text)"
cursor.execute(create_table)

user = (2, 'tom', 'asdf')
insert_query = "INSERT INTO users VALUES(?, ?, ?)"



users = [
    (3, 'rolf', 'asdf'),
    (4, 'anne', 'xyz')
]
cursor.executemany(insert_query, users)
select_query = "SELECT * FROM users"

for row in cursor.execute(select_query):
    print(row)


connection.commit()
connection.close()
import os
import sqlite3

connection = sqlite3.connect('database.db')


with open(os.path.dirname(os.path.realpath(__file__)) + '/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content, author, author_email) VALUES (?, ?, ?, ?)",
            ('First Post', 'Content for the first post', 'Theodore', 'capinski@berkeley.edu')
            )

cur.execute("INSERT INTO posts (title, content, author, author_email) VALUES (?, ?, ?, ?)",
            ('Second Post', 'Content for the second post', 'Thedorus', 'capinski@berkeley.edu')
            )

connection.commit()
connection.close()
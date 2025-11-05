import sqlite3

conn = sqlite3.connect("pets.db")

cursor = conn.cursor()

try:
    cursor.execute("""
        DROP TABLE pet
    """)
    conn.commit()
except:
    pass

cursor.execute("""
    CREATE TABLE pet (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        kind TEXT,
        noise TEXT,
        food TEXT
    )
""")
conn.commit()


cursor.execute("""
    INSERT INTO pet (name, kind)
    VALUES ("dorothy", "dog")
""")

cursor.execute("""
    INSERT INTO pet (name, kind)
    VALUES ("sandy", "cat")
""")

cursor.execute("""
    INSERT INTO pet (name, kind)
    VALUES ("whiskers", "hamster")
""")

conn.commit()

cursor = conn.cursor()

result = cursor.execute("select * from pet")
rows = cursor.fetchall()
for row in rows:
    print([row])

data = []
for row in rows:
    (id, name, kind, noise, food) = row
    print(name, kind)
    item = {
        "id":id,
        "name":name,
        "kind":kind,
        "noise":noise,
        "food":food
    }
    data.append(item)
    print(data)

data = [
    {
        "id":id,
        "name":name,
        "kind":kind,
        "noise":noise,
        "food":food
    }
    for id, name, kind, noise, food in rows
]

print(data)

rows = cursor.execute("select * from pet").fetchall()
data = [
    {
        "id":id,
        "name":name,
        "kind":kind,
        "noise":noise,
        "food":food
    }
    for id, name, kind, noise, food in rows
]
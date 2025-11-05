import sqlite3

def setup_database(name):

    conn = sqlite3.connect(name)

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

    # setup KIND table

    try:
        cursor.execute("""
            DROP TABLE kind
        """)
        conn.commit()
    except:
        pass

    cursor.execute("""
        CREATE TABLE kind (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kind_name TEXT NOT NULL,
            noise TEXT,
            food TEXT
        )
    """)
    conn.commit()


    cursor.execute("""
        INSERT INTO kind (kind_name, noise, food)
        VALUES ("dog", "arf", "dogfood")
    """)

    cursor.execute("""
        INSERT INTO kind (kind_name, noise, food)
        VALUES ("cat", "meow", "catfood")
    """)

    cursor.execute("""
        INSERT INTO kind (kind_name, noise, food)
        VALUES ("fish", "blub", "fishfood")
    """)

    cursor.execute("""
        INSERT INTO kind (kind_name, noise, food)
        VALUES ("hamster", "squeak", "hamsterchow")
    """)

    conn.commit()

if __name__ == "__main__":
    setup_database("pets.db")


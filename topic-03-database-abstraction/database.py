import sqlite3

connection = None


def initialize(database_file):
    global connection
    connection = sqlite3.connect(database_file, check_same_thread=False)
    connection.row_factory = sqlite3.Row


def get_pets():
    cursor = connection.cursor()
    cursor.execute("""select * from pets""")
    pets = cursor.fetchall()
    pets = [dict(pet) for pet in pets]
    for pet in pets:
        print(pet)
    return pets


def get_pet(id):
    cursor = connection.cursor()
    cursor.execute(f"""select * from pets where id = ?""", (id,))
    rows = cursor.fetchall()
    try:
        (id, name, xtype, age, owner) = rows[0]
        data = {"id": id, "name": name, "type": xtype, "age": age, "owner": owner}

        return data
    except:
        return "Data not found."


def create_pet(data):
    try:
        data["age"] = int(data["age"])
    except:
        data["age"] = 0
    cursor = connection.cursor()
    cursor.execute(
        """insert into pets(name, age, type, owner) values (?,?,?,?)""",
        (data["name"], data["age"], data["type"], data["owner"]),
    )
    connection.commit()


def test_create_pets():
    pass


def update_pet(id, data):
    try:
        data["age"] = int(data["age"])
    except:
        data["age"] = 0
    cursor = connection.cursor()
    cursor.execute(
        """update pets set name=?, age=?, type=?, owner=? where id=?""",
        (data["name"], data["age"], data["type"], data["owner"], id),
    )
    connection.commit()


def delete_pet(id):
    cursor = connection.cursor()
    cursor.execute(f"""delete from pets where id = ?""", (id,))
    connection.commit()


def setup_test_database():
    initialize("test_pets.db")
    cursor = connection.cursor()
    cursor.execute(
        """
        create table if not exists pets (
            id integer primary key autoincrement,
            name text not null,
            type text not null,
            age integer,
            owner text
        )
    """
    )
    connection.commit()
    pets = [
        {"name": "dorothy", "type": "dog", "age": 9, "owner": "greg"},
        {"name": "suzy", "type": "mouse", "age": 9, "owner": "greg"},
        {"name": "casey", "type": "dog", "age": 9, "owner": "greg"},
        {"name": "heidi", "type": "cat", "age": 15, "owner": "david"},
    ]
    for pet in pets:
        create_pet(pet)
    pets = get_pets()
    assert len(pets) == 4


def test_get_pets():
    print("testing get_pets")
    pets = get_pets()
    assert type(pets) is list
    assert len(pets) > 0
    assert type(pets[0]) is dict
    pet = pets[0]
    print(pet)
    for field in ["id", "name", "type", "age", "owner"]:
        assert field in pet, f"Field {field} missing from {pet}"
    assert type(pet["id"]) is int
    assert type(pet["name"]) is str


if __name__ == "__main__":
    setup_test_database()
    test_get_pets()
    test_create_pets()
    print("done.")

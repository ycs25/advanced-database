import sqlite3
from setup_pets_database import setup_database

# remember to $ pip install flask

connection = sqlite3.connect("pets.db", check_same_thread=False)

def retrieve_pets():
    cursor = connection.cursor()
    rows = cursor.execute("select * from pet").fetchall()
    pet_data = [
        {
            "id":str(id),
            "name":name,
            "kind":kind,
            "noise":noise,
            "food":food
        }
        for id, name, kind, noise, food in rows
    ]
    return pet_data

def test_retrieve_pets():
    print("testing retrieve_pets...")
    data = retrieve_pets()
    assert type(data) == list
    assert type(data[0]) == dict
    for field in ["id","name","kind","noise","food"]:
        assert field in data[0]
        # print([data[0][field]])
        # print(type(data[0][field]))
        # print(field, data[0])
        # print([data[0][field]])
        # print([type(data[0][field])])
        if data[0][field]:
            assert type(data[0][field]) == str

def retrieve_pet(id):
    cursor = connection.cursor()
    id = int(id)
    row = cursor.execute("select * from pet where id = ?", (id,)).fetchone()
    pet_item = {
        "id":str(row[0]),
        "name":row[1],
        "kind":row[2],
        "noise":row[3],
        "food":row[4]
    }
    return pet_item

def test_retrieve_pet():
    print("testing retrieve_pet...")
    pets = retrieve_pets()
    expected_pet = pets[0]
    pet = retrieve_pet(pets[0]["id"])
    assert pet == pets[0]


def create_pet(name, kind, noise, food):
    cursor = connection.cursor()
    cursor.execute("insert into pet (name, kind, noise, food) values (?, ?, ?, ?)", (
            name,
            kind, 
            noise, 
            food))
    connection.commit()

def test_create_pet():
    print("testing create_pet()...")
    create_pet("spot","dog","arf","dogfood")
    data = retrieve_pets()
    found = False
    for item in data:
        if item["name"] == "spot":
            found = True
            assert item["kind"] == "dog"
            assert item["noise"] == "arf"
            assert item["food"] == "dogfood"
    assert found

def update_pet(id, name, kind, noise, food):
    cursor = connection.cursor()
    cursor.execute("update pet set name = ?, kind = ?, noise = ?, food = ? where id = ?", (
            name,
            kind, 
            noise, 
            food, 
            id))
    connection.commit()

def test_update_pet():
    print("testing update_pet()...")
    data = retrieve_pets()
    pet = data[0]
    update_pet(pet["id"],"suzy",pet["kind"],pet["noise"],pet["food"])
    data = retrieve_pets()
    pet = data[0]
    assert pet["name"] == "suzy"

def delete_pet(id):
    cursor = connection.cursor()
    cursor.execute("delete from pet where id = ?", (id,))
    connection.commit()

def test_delete_pet():
    print("testing delete pet()...")
    old_data = retrieve_pets()
    pet = old_data[0]
    delete_pet(pet["id"])
    data = retrieve_pets()
    for i in range(0,len(data)):
        for field in ["id","name","kind"]:
            assert data[i][field] == old_data[i+1][field]

if __name__ == "__main__":
    setup_database("test_pets.db")
    connection = sqlite3.connect("test_pets.db", check_same_thread=False)
    test_retrieve_pets()
    test_retrieve_pet()
    test_create_pet()
    test_update_pet()
    test_delete_pet()
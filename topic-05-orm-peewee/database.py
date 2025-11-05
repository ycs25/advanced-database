from peewee import *

# Initialize database connection
db = None

# Define models
class Kind(Model):
    kind_name = CharField()
    food = CharField()
    noise = CharField()

    class Meta:
        database = db


class Pet(Model):
    name = CharField()
    age = IntegerField()
    owner = CharField()
    kind = ForeignKeyField(Kind, backref="pets")

    class Meta:
        database = db


def initialize(database_file):
    global db, Kind, Pet
    db = SqliteDatabase(database_file)

    Kind._meta.database = db
    Pet._meta.database = db

    db.connect()
    db.create_tables([Pet, Kind])

def test_initialize():
    print("test initialize...")
    initialize("test_pets.db")
    assert db != None


def get_pets():
    pets = Pet.select().join(Kind)
    return list(pets)

def test_get_pets():
    print("test get_pets...")
    kind = Kind(kind_name = "dog",food="dog_food",noise="bark")
    kind.save()
    pet = Pet(name="Dorothy",age=10,owner="Greg",kind=kind)
    pet.save()
    pets = get_pets()
    assert type(pets) is list
    assert type(pets[0]) is Pet
    assert pets[0].name == "Dorothy"

def get_kinds():
    kinds = Kind.select()
    return list(kinds)


def test_get_kinds():
    print("test get_kinds...")
    kind = Kind(kind_name="dog", food="dog_food", noise="bark")
    kinds = get_kinds()
    assert type(kinds) is list
    assert type(kinds[0]) is Kind
    assert kinds[0].kind_name == "dog"

def get_pet_by_id(id):
    # pet = Pet.get_by_id(id)
    pet = Pet.get_or_none(Pet.id == id)
    return pet

def test_get_pet_by_id():
    print("test get_pet_by_id...")
    pet = get_pet_by_id(1)
    assert type(pet) is Pet
    assert pet.id == 1
    pet = get_pet_by_id(3451)
    assert pet == None


def get_kind_by_id(id):
    # kind = Kind.get_by_id(id)
    kind = Kind.get_or_none(Kind.id == id)
    return kind


def test_get_kind_by_id():
    print("test get_kind_by_id...")
    kind = get_kind_by_id(1)
    assert type(kind) is Kind
    assert kind.id == 1
    kind = get_kind_by_id(3451)
    assert kind == None


if __name__ == "__main__":
    test_initialize()
    test_get_pets()
    test_get_kinds()
    test_get_pet_by_id()
    test_get_kind_by_id()
    print("done.")


# def create_pet(data):
#     try:
#         data["age"] = int(data["age"])
#     except:
#         data["age"] = 0
#     cursor = connection.cursor()
#     cursor.execute(
#         """insert into pet(name, age, kind_id, owner) values (?,?,?,?)""",
#         (data["name"], data["age"], data["kind_id"], data["owner"]),
#     )
#     connection.commit()

# def create_kind(data):
#     cursor = connection.cursor()
#     cursor.execute(
#         """insert into kind(name, food, sound) values (?,?,?)""",
#         (data["name"], data["food"], data["sound"]),
#     )
#     connection.commit()

# def test_create_pet():
#     pass


# def update_pet(id, data):
#     try:
#         data["age"] = int(data["age"])
#     except:
#         data["age"] = 0
#     cursor = connection.cursor()
#     cursor.execute(
#         """update pet set name=?, age=?, type=?, owner=? where id=?""",
#         (data["name"], data["age"], data["type"], data["owner"], id),
#     )
#     connection.commit()

# def update_kind(id, data):
#     cursor = connection.cursor()
#     cursor.execute(
#         """update kind set name=?, food=?, sound=? where id=?""",
#         (data["name"], data["food"], data["sound"], id),
#     )
#     connection.commit()

# def delete_pet(id):
#     cursor = connection.cursor()
#     cursor.execute(f"""delete from pet where id = ?""", (id,))
#     connection.commit()

# def delete_kind(id):
#     cursor = connection.cursor()
#     cursor.execute(f"""delete from kind where id = ?""", (id,))
#     connection.commit()

# def setup_test_database():
#     initialize("test_pets.db")
#     cursor = connection.cursor()
#     cursor.execute("drop table pet")
#     cursor.execute("drop table kind")
#     cursor.execute(
#             """
#             create table if not exists kind (
#                 id integer primary key autoincrement,
#                 name text not null,
#                 food text,
#                 sound text
#             )
#             """
#         )
#     connection.commit()
#     cursor.execute(
#         """
#             insert
#                 into kind(name, food, sound)
#                 values (?,?,?)
#             """,
#         ("dog", "dogfood", "bark"),
#     )
#     cursor.execute(
#         """
#             insert
#                 into kind(name, food, sound)
#                 values (?,?,?)
#             """,
#         ("cat", "catfood", "meow"),
#     )
#     connection.commit()
#     cursor = connection.cursor()
#     cursor.execute(
#         """
#         create table if not exists pet (
#             id integer primary key autoincrement,
#             name text not null,
#             kind_id integer,
#             age integer,
#             owner text
#         )
#     """
#     )
#     connection.commit()
#     pets = [
#         {"name": "dorothy", "kind_id": 1, "age": 9, "owner": "greg"},
#         {"name": "suzy", "kind_id": 1, "age": 9, "owner": "greg"},
#         {"name": "casey", "kind_id": 2, "age": 9, "owner": "greg"},
#         {"name": "heidi", "kind_id": 2, "age": 15, "owner": "david"},
#     ]
#     for pet in pets:
#         create_pet(pet)
#     pets = get_pets()
#     assert len(pets) == 4

# def test_get_pets():
#     print("testing get_pets")
#     pets = get_pets()
#     assert type(pets) is list
#     assert len(pets) > 0
#     assert type(pets[0]) is dict
#     pet = pets[0]
#     print(pet)
#     for field in ["id", "name", "kind_id", "age", "owner"]:
#         assert field in pet, f"Field {field} missing from {pet}"
#     assert type(pet["id"]) is int
#     assert type(pet["name"]) is str

# def test_get_kinds():
#     print("testing get_kinds")
#     kinds = get_kinds()
#     assert type(kinds) is list
#     assert len(kinds) > 0
#     assert type(kinds[0]) is dict
#     kind = kinds[0]
#     for field in ["id", "name", "food", "sound"]:
#         assert field in kind, f"Field {field} missing from {kind}"
#     assert type(kind["id"]) is int
#     assert type(kind["name"]) is str

# if __name__ == "__main__":
#     setup_test_database()
#     test_get_pets()
#     test_get_kinds()
#     test_create_pet()
#     print("done.")

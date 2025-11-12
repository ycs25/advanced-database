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
    db = SqliteDatabase(database_file, pragmas={'foreign_keys': 1})

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
    kind = Kind(kind_name = "dog",food="dog_food",noise="bark")
    kind.save()
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
    kind = Kind(kind_name = "dog",food="dog_food",noise="bark")
    kind.save()
    pet = Pet(name="Dorothy",age=10,owner="Greg",kind=kind)
    pet.save()

    found_pet = get_pet_by_id(pet.id)
    missing_pet = get_pet_by_id(3451)

    assert type(found_pet) is Pet
    assert found_pet.id == pet.id
    assert found_pet.name == "Dorothy"
    assert missing_pet == None


def get_kind_by_id(id):
    # kind = Kind.get_by_id(id)
    kind = Kind.get_or_none(Kind.id == id)
    return kind


def test_get_kind_by_id():
    print("test get_kind_by_id...")
    kind = Kind(kind_name = "dog",food="dog_food",noise="bark")
    kind.save()

    found_kind = get_kind_by_id(kind.id)
    missing_kind = get_kind_by_id(3451)

    assert type(found_kind) is Kind
    assert found_kind.id == kind.id
    assert found_kind.kind_name == "dog"
    assert missing_kind == None

def create_kind(data):
    Kind.create(kind_name = data["kind_name"], food = data["food"], noise = data["noise"])

def test_create_kind():
    print("test create_kind(data)...")
    data = {"kind_name": "cat", "food": "fish", "noise": "meow"}
    create_kind(data)

    found_kind = Kind.get(Kind.kind_name == "cat")
    assert type(found_kind) is Kind
    assert found_kind.food == "fish"
    assert found_kind.noise == "meow"

def create_pet(data):
    try:
        data["age"] = int(data["age"])
    except:
        data["age"] = 0

    kind = Kind.get_or_none(Kind.id == data["kind_id"])
    if kind:
        Pet.create(name = data["name"], age = data["age"], owner = data["owner"], kind = kind)

def test_create_pet():
    print("test create_pet(data)...")
    kind = Kind(kind_name = "dog",food="dog_food",noise="bark")
    kind.save()

    data = {"name": "Buddy", "age": 5, "owner": "Alice", "kind_id": 1}
    create_pet(data)

    found_pet = Pet.get(Pet.name == "Buddy")
    assert type(found_pet) is Pet
    assert found_pet.age == 5
    assert found_pet.owner == "Alice"
    assert found_pet.kind.kind_name == "dog"

def update_kind(id, data):
    kind = Kind.get_or_none(Kind.id == id)
    if kind:
        kind.kind_name = data.get("name", kind.kind_name)
        kind.food = data.get("food", kind.food)
        kind.noise = data.get("noise", kind.noise)
        kind.save()

def test_update_kind():
    print("test update_kind(id, data)...")
    kind = Kind(kind_name = "dog",food="dog_food",noise="bark")
    kind.save()

    data = {"kind_name": "canine", "food": "premium_dog_food"}
    update_kind(kind.id, data)

    updated_kind = Kind.get(Kind.id == kind.id)
    assert updated_kind.kind_name == "canine"
    assert updated_kind.food == "premium_dog_food"
    assert updated_kind.noise == "bark"

def update_pet(id, data):
    try:
        data["age"] = int(data["age"])
    except:
        data["age"] = 0
    
    pet = Pet.get_or_none(Pet.id == id)
    if pet:
        pet.name = data.get("name", pet.name)
        pet.age = data.get("age", pet.age)
        pet.owner = data.get("owner", pet.owner)
        if "kind_id" in data:
            kind = Kind.get_or_none(Kind.id == data["kind_id"])
            if kind:
                pet.kind = kind
        pet.save()

def test_update_pet():
    print("test update_pet(id, data)...")
    kind1 = Kind(kind_name = "dog",food="dog_food",noise="bark")
    kind1.save()
    kind2 = Kind(kind_name = "cat",food="cat_food",noise="meow")
    kind2.save()

    pet = Pet(name="Buddy",age=5,owner="Alice",kind=kind1)
    pet.save()

    data = {"name": "Max", "age": 6, "kind_id": kind2.id}
    update_pet(pet.id, data)

    updated_pet = Pet.get(Pet.id == pet.id)
    assert updated_pet.name == "Max"
    assert updated_pet.age == 6
    assert updated_pet.owner == "Alice"
    assert updated_pet.kind.kind_name == "cat"

def delete_pet(id):
    pet = Pet.get_by_id(id)
    pet.delete_instance()

def test_delete_pet():
    print("testing delete_pet...")
    kind = Kind(kind_name = "dog",food="dog_food",noise="bark")
    kind.save()
    pet = Pet(name="Dorothy",age=10,owner="Greg",kind=kind)
    pet.save()

    lost_id = pet.id
    delete_pet(lost_id)

    deleted_pet = Pet.get_or_none(Pet.id == lost_id)
    assert deleted_pet is None

def delete_kind(id):

    try:
        kind = Kind.get_by_id(id)
        kind.delete_instance()
    except IntegrityError:
        raise ValueError(f"Cannot delete '{kind.kind_name}', it is used by one or more pets. ")

def test_delete_kind():
    print("testing delete_kind...")
    kind = Kind(kind_name = "dog",food="dog_food",noise="bark")
    kind.save()

    lost_id = kind.id
    delete_kind(lost_id)

    deleted_kind = Kind.get_or_none(Kind.id == lost_id)
    assert deleted_kind is None

def test_delete_kind_in_use():
    print("test delete_kind (when in-use)...")
    kind = Kind.create(kind_name="dog", food="dog_food", noise="bark")
    pet = Pet.create(name="Dorothy", age=10, owner="Greg", kind=kind)

    try:
        delete_kind(kind.id)
        assert False, "delete_kind() did not raise error as expected"
    except ValueError as e:
        print(str(e))


def test_cleanup():
    print("test cleanup...")
    if db:
        db.drop_tables([Pet, Kind])
        db.close()

if __name__ == "__main__":

    test_initialize()
    test_get_pets()
    test_cleanup()

    test_initialize()
    test_get_kinds()
    test_cleanup()

    test_initialize()
    test_get_pet_by_id()
    test_cleanup()

    test_initialize()
    test_get_kind_by_id()
    test_cleanup()

    test_initialize()
    test_create_kind()
    test_cleanup()

    test_initialize()
    test_create_pet()
    test_cleanup()

    test_initialize()
    test_update_kind()
    test_cleanup()

    test_initialize()
    test_update_pet()
    test_cleanup()

    test_initialize()
    test_delete_pet()
    test_cleanup()

    test_initialize()
    test_delete_kind_in_use()
    test_cleanup()

    test_initialize()
    test_delete_kind()
    test_cleanup()

    print("done.")


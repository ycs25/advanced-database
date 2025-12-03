import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId

load_dotenv()
connection_string = os.environ.get("MONGO_URI")

client = MongoClient(connection_string, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Ping... Successfully linked to MongoDB Atlas!")
except Exception as e:
    print(f"Connection Failed: {e}")

pets_db = client.pets_db

# PETS

# def retrieve_pets():
#     pets_collection = pets_db.pets_collection
#     kind_collection = pets_db.kind_collection
#     pets = list(pets_collection.find())
#     for pet in pets:
#         pet["id"] = str(pet["_id"])
#         del pet["_id"]
#         kind = kind_collection.find_one({"_id": pet["kind_id"]})
#         for tag in ["kind_name", "noise", "food"]:
#             pet[tag] = kind[tag]
#         del pet["kind_id"]
#     return pets

def retrieve_pets():
    pets_collection = pets_db.pets_collection
    
    pipeline = [
        {
            "$lookup": {
                "from": "kind_collection",
                "localField": "kind_id",
                "foreignField": "_id",
                "as": "kind_details"
            }
        },

        {
            "$unwind": "$kind_details"
        },

        {
            "$project": {
                "_id":0,
                "id": {"$toString": "$_id"},
                "name": 1,
                "age": 1,
                "owner": 1,

                "kind_name": "$kind_details.kind_name",
                "noise": "$kind_details.noise",
                "food": "$kind_details.food"
            }
        }
    ]

    result = list(pets_collection.aggregate(pipeline))
    return result

def test_retrieve_pets():
    print("test retrieve_pets")
    pets = retrieve_pets()
    assert type(pets) is list
    print(pets)
    assert type(pets[0]) is dict
    assert type(pets[0]["id"]) is str
    pets[0]["id"] = "1"
    print(pets[0])
    assert pets[0] == {
        "id": "1",
        "name": "Suzy",
        "age": 3,
        "owner": "Greg",
        "kind_name": "Dog",
        "food": "Dog food",
        "noise": "Bark",
    }

def retrieve_pet(id):
    pets_collection = pets_db.pets_collection
    id = ObjectId(id)
    pet = pets_collection.find_one({"_id": id})
    pet["id"] = str(pet["_id"])
    del pet["_id"]
    return pet

def retrieve_pet_2(pet_id):
    pets_collection = pets_db.pets_collection
    oid = ObjectId(pet_id)
    
    pipeline = [
        { "$match": { "_id": oid } }, 
        
        { "$lookup": { "from": "kind_collection", "localField": "kind_id", "foreignField": "_id", "as": "kind_details" } },
        { "$unwind": "$kind_details" },
        { "$project": {
            "_id": 0,
            "id": { "$toString": "$_id" },
            "name": 1,
            "age": 1,
            "kind_name": "$kind_details.kind_name",
            "noise": "$kind_details.noise",
            "food": "$kind_details.food"
        }}
    ]
    try:
        return next(pets_collection.aggregate(pipeline), None)
    except StopIteration:
        return None


def test_retrieve_pet():
    print("test retrieve_pet")
    pets = retrieve_pets()
    id = pets[0]["id"]
    pet = retrieve_pet(id)
    del pet["kind_id"]
    assert pet == {"id": id, "name": "Suzy", "age": 3, "owner": "Greg"}


def create_pet(data):
    pets_collection = pets_db.pets_collection
    data["kind_id"] = ObjectId(data["kind_id"])
    pets_collection.insert_one(data)


def delete_pet(id):
    pets_collection = pets_db.pets_collection
    pets_collection.delete_one({"_id": ObjectId(id)})


def test_create_and_delete_pet():
    kind_collection = pets_db.kind_collection
    kind = kind_collection.find_one({"kind_name": "Dog"})
    example_kind_id = str(kind["_id"])
    print("test create_and_delete_pet")
    pets = retrieve_pets()
    for pet in pets:
        if pet["name"] == "gamma":
            delete_pet(pet["id"])
    data = {"name": "gamma", "age": 12, "kind_id": example_kind_id, "owner": "delta"}
    create_pet(data)
    pets = retrieve_pets()
    found = False
    for pet in pets:
        if pet["name"] == "gamma" and pet["owner"] == "delta":
            assert pet["age"] == 12
            assert pet["kind_name"] == "Dog"
            found = True
            id = pet["id"]
    assert found
    delete_pet(id)
    pets = retrieve_pets()
    found = False
    for pet in pets:
        if pet["name"] == "gamma" and pet["owner"] == "delta":
            found = True
    assert not found

def test_create_and_delete_pet_2():
    print("test create_and_delete_pet")
    pets_collection = pets_db.pets_collection
    kind_collection = pets_db.kind_collection
    kind = kind_collection.find_one({"kind_name": "Dog"})
    if not kind:
        print("Error: 'Dog' kind not found in DB") 
        return

    example_kind_id = str(kind["_id"])
    data = {"name": "test_name", "age": 999, "kind_id": example_kind_id, "owner": "test_owner"}
    created_id = None

    try:
        create_pet(data)
        test_pet = pets_collection.find_one({"name": "test_name"})
        assert test_pet is not None
        created_id = str(test_pet["_id"])
        assert test_pet["age"] == 999
        assert test_pet["owner"] == "test_owner"
        assert str(test_pet["kind_id"]) == example_kind_id
        
        delete_pet(created_id)
        deleted_pet = pets_collection.find_one({"_id": test_pet["_id"]})
        assert deleted_pet is None

    finally:
        if created_id:
            pets_collection.delete_one({"_id": ObjectId(created_id)})

def update_pet(id, data):
    pets_collection = pets_db.pets_collection
    data["kind_id"] = ObjectId(data["kind_id"])
    pets_collection.update_one({"_id": ObjectId(id)}, {"$set": data})


def test_update_pet():
    print("test update_pet")
    pets_collection = pets_db.pets_collection
    # find the reference id
    pet_saved = pets_collection.find_one()
    id = str(pet_saved["_id"])

    # modify the record with the same kind_id
    kind_id = pet_saved["kind_id"]
    data = {"name": "gamma", "age": 12, "kind_id": kind_id, "owner": "delta"}
    update_pet(id, data)

    # check that the update happened
    pet = retrieve_pet(id)
    assert pet["name"] == "gamma"
    assert pet["owner"] == "delta"

    # restore the original data and verify
    update_pet(id, pet_saved)
    pet = retrieve_pet(id)
    assert pet["name"] == "Suzy"
    assert pet["owner"] == "Greg"


# KINDS

def retrieve_kinds():
    kind_collection = pets_db.kind_collection
    kinds = list(kind_collection.find())
    for kind in kinds:
        kind["id"] = str(kind["_id"])
    return kinds


def test_retrieve_kinds():
    print("test retrieve_kinds")
    kinds = retrieve_kinds()
    assert type(kinds) is list
    assert type(kinds[0]) is dict
    assert type(kinds[0]["id"]) is str
    del kinds[0]["_id"]
    del kinds[0]["id"]
    assert kinds[0] == {"kind_name": "Dog", "food": "Dog food", "noise": "Bark"}


def create_kind(data):
    kind_collection = pets_db.kind_collection
    kind_collection.insert_one(data)


def delete_kind(id):
    kind_collection = pets_db.kind_collection
    pets_collection = pets_db.pets_collection
    pets_with_kind = pets_collection.find({"kind_id": ObjectId(id)})
    if list(pets_with_kind):
        return "Cannot delete kind: pets still reference it"

    kind_collection.delete_one({"_id": ObjectId(id)})


def test_create_and_delete_kind():
    print("test create_and_delete_kind")
    data = {"kind_name": "bunny", "food": "carrot", "noise": "hophop"}
    create_kind(data)
    kinds = retrieve_kinds()
    found = False
    for kind in kinds:
        if kind["kind_name"] == "bunny" and kind["food"] == "carrot":
            found = True
            kind_id = kind["id"]
    assert found
    delete_kind(kind_id)
    kinds = retrieve_kinds()
    found = False
    for kind in kinds:
        if kind["kind_name"] == "bunny" and kind["food"] == "carrot":
            found = True
    assert not found


def retrieve_kind(id):
    kind_collection = pets_db.kind_collection
    _id = ObjectId(id)
    kind = kind_collection.find_one({"_id": _id})
    kind["id"] = str(kind["_id"])
    del kind["_id"]
    return kind


def test_retrieve_kind():
    print("test retrieve_kind")
    kinds = retrieve_kinds()
    id = kinds[0]["id"]
    kind = retrieve_kind(id)
    assert kind == {"id": id, "kind_name": "Dog", "food": "Dog food", "noise": "Bark"}


def update_kind(id, data):
    kind_collection = pets_db.kind_collection
    kind_collection.update_one({"_id": ObjectId(id)}, {"$set": data})


def test_update_kind():
    print("test update_kind")
    kinds = retrieve_kinds()
    id = kinds[0]["id"]
    kind_save = retrieve_kind(id)
    data = {"kind_name": "puppy", "food": "Puppy chow", "noise": "Yip"}
    update_kind(id, data)
    kind = retrieve_kind(id)
    assert kind == {
        "id": id,
        "kind_name": "puppy",
        "food": "Puppy chow",
        "noise": "Yip",
    }
    update_kind(id, kind_save)
    kind = retrieve_kind(id)
    assert kind == kind_save

if __name__ == "__main__":
    test_retrieve_kinds()
    test_create_and_delete_kind()
    test_retrieve_kind()
    test_update_kind()
    test_retrieve_pets()
    test_retrieve_pet()
    test_create_and_delete_pet()
    test_update_pet()
    print("done.")

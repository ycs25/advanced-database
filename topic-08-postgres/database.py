"""
PostgreSQL database module for pets application
Adapted from Topic 4 SQLite version
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import os

connection = None


def initialize(host='localhost', database='pets_db', user='pets_app', password=None):
    """Initialize PostgreSQL connection"""
    global connection
    
    # Get password from environment if not provided
    if password is None:
        password = os.environ.get('POSTGRES_PASSWORD', 'petsAppPassword456!')
    
    connection = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        cursor_factory=RealDictCursor  # Return rows as dictionaries
    )
    # PostgreSQL uses autocommit=False by default (transactions)
    connection.autocommit = False


def get_pets():
    """Retrieve all pets with kind information"""
    cursor = connection.cursor()
    cursor.execute("""
        SELECT 
            pet.id, 
            pet.name, 
            pet.age, 
            pet.owner, 
            kind.name as kind_name, 
            kind.food, 
            kind.sound 
        FROM pet 
        JOIN kind ON pet.kind_id = kind.id
        ORDER BY pet.name
    """)
    pets = cursor.fetchall()
    cursor.close()
    return pets


def get_kinds():
    """Retrieve all pet kinds"""
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM kind ORDER BY name")
    kinds = cursor.fetchall()
    cursor.close()
    return kinds


def get_pet(id):
    """Retrieve a single pet by ID"""
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM pet WHERE id = %s", (id,))
    pet = cursor.fetchone()
    cursor.close()
    return pet if pet else {}


def get_kind(id):
    """Retrieve a single kind by ID"""
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM kind WHERE id = %s", (id,))
    kind = cursor.fetchone()
    cursor.close()
    return kind if kind else {}


def create_pet(data):
    """Create a new pet"""
    try:
        data["age"] = int(data.get("age", 0))
    except (ValueError, TypeError):
        data["age"] = 0
    
    cursor = connection.cursor()
    cursor.execute(
        """INSERT INTO pet (name, age, kind_id, owner) 
           VALUES (%s, %s, %s, %s)""",
        (data["name"], data["age"], data["kind_id"], data["owner"])
    )
    connection.commit()
    cursor.close()


def create_kind(data):
    """Create a new kind"""
    cursor = connection.cursor()
    cursor.execute(
        """INSERT INTO kind (name, food, sound) 
           VALUES (%s, %s, %s)""",
        (data["name"], data["food"], data["sound"])
    )
    connection.commit()
    cursor.close()


def update_pet(id, data):
    """Update an existing pet"""
    try:
        data["age"] = int(data.get("age", 0))
    except (ValueError, TypeError):
        data["age"] = 0
    
    cursor = connection.cursor()
    cursor.execute(
        """UPDATE pet 
           SET name = %s, age = %s, kind_id = %s, owner = %s 
           WHERE id = %s""",
        (data["name"], data["age"], data["kind_id"], data["owner"], id)
    )
    connection.commit()
    cursor.close()


def update_kind(id, data):
    """Update an existing kind"""
    cursor = connection.cursor()
    cursor.execute(
        """UPDATE kind 
           SET name = %s, food = %s, sound = %s 
           WHERE id = %s""",
        (data["name"], data["food"], data["sound"], id)
    )
    connection.commit()
    cursor.close()


def delete_pet(id):
    """Delete a pet"""
    cursor = connection.cursor()
    cursor.execute("DELETE FROM pet WHERE id = %s", (id,))
    connection.commit()
    cursor.close()


def delete_kind(id):
    """Delete a kind (will fail if pets reference it due to foreign key)"""
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM kind WHERE id = %s", (id,))
        connection.commit()
    except psycopg2.IntegrityError as e:
        connection.rollback()
        raise Exception(f"Cannot delete kind: pets still reference it") from e
    finally:
        cursor.close()


# Testing functions
def setup_test_database():
    """Set up test database with sample data"""
    initialize(database='test_pets_db')
    
    cursor = connection.cursor()
    
    # Drop and recreate tables
    cursor.execute("DROP TABLE IF EXISTS pet CASCADE")
    cursor.execute("DROP TABLE IF EXISTS kind CASCADE")
    
    cursor.execute("""
        CREATE TABLE kind (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            food VARCHAR(100),
            sound VARCHAR(50)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE pet (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            kind_id INTEGER NOT NULL,
            age INTEGER,
            owner VARCHAR(100),
            FOREIGN KEY (kind_id) REFERENCES kind(id) ON DELETE RESTRICT
        )
    """)
    
    connection.commit()
    
    # Insert test data
    cursor.execute(
        "INSERT INTO kind (name, food, sound) VALUES (%s, %s, %s)",
        ("dog", "dogfood", "bark")
    )
    cursor.execute(
        "INSERT INTO kind (name, food, sound) VALUES (%s, %s, %s)",
        ("cat", "catfood", "meow")
    )
    connection.commit()
    
    pets = [
        {"name": "dorothy", "kind_id": 1, "age": 9, "owner": "greg"},
        {"name": "suzy", "kind_id": 1, "age": 9, "owner": "greg"},
        {"name": "casey", "kind_id": 2, "age": 9, "owner": "greg"},
        {"name": "heidi", "kind_id": 2, "age": 15, "owner": "david"},
    ]
    
    for pet in pets:
        create_pet(pet)
    
    cursor.close()


def test_get_pets():
    print("Testing get_pets...")
    pets = get_pets()
    assert type(pets) is list
    assert len(pets) > 0
    assert type(pets[0]) is dict
    pet = pets[0]
    print(f"Sample pet: {pet}")
    
    required_fields = ["id", "name", "age", "owner", "kind_name"]
    for field in required_fields:
        assert field in pet, f"Field {field} missing from {pet}"
    
    print("✓ get_pets test passed")


def test_get_kinds():
    print("Testing get_kinds...")
    kinds = get_kinds()
    assert type(kinds) is list
    assert len(kinds) > 0
    assert type(kinds[0]) is dict
    kind = kinds[0]
    
    required_fields = ["id", "name", "food", "sound"]
    for field in required_fields:
        assert field in kind, f"Field {field} missing from {kind}"
    
    print("✓ get_kinds test passed")


if __name__ == "__main__":
    # Note: You need to create test_pets_db first:
    # psql -U postgres -c "CREATE DATABASE test_pets_db;"
    # psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE test_pets_db TO pets_app;"
    
    print("Setting up test database...")
    setup_test_database()
    
    print("\nRunning tests...")
    test_get_pets()
    test_get_kinds()
    
    print("\n✓ All tests passed!")

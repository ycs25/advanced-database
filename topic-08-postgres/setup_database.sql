-- PostgreSQL setup script for pets database
-- Topic 4 adaptation for PostgreSQL

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS pet CASCADE;
DROP TABLE IF EXISTS kind CASCADE;

-- Create kind table (pet types)
CREATE TABLE kind (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    food VARCHAR(100),
    sound VARCHAR(50)
);

-- Create pet table with foreign key to kind
CREATE TABLE pet (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    kind_id INTEGER NOT NULL,
    age INTEGER CHECK (age >= 0),
    owner VARCHAR(100),
    CONSTRAINT fk_kind
        FOREIGN KEY (kind_id) 
        REFERENCES kind(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- Create indexes for better query performance
CREATE INDEX idx_pet_kind_id ON pet(kind_id);
CREATE INDEX idx_pet_owner ON pet(owner);

-- Insert sample pet kinds
INSERT INTO kind (name, food, sound) VALUES
    ('dog', 'dogfood', 'bark'),
    ('cat', 'catfood', 'meow'),
    ('bird', 'seeds', 'chirp'),
    ('fish', 'flakes', 'bubble');

-- Insert sample pets
INSERT INTO pet (name, kind_id, age, owner) VALUES
    ('Dorothy', 1, 9, 'Greg'),
    ('Suzy', 1, 9, 'Greg'),
    ('Casey', 2, 9, 'Greg'),
    ('Heidi', 2, 15, 'David'),
    ('Tweety', 3, 2, 'Alice'),
    ('Nemo', 4, 1, 'Bob');

-- Verify the data
SELECT 'Kinds:' as table_name;
SELECT * FROM kind;

SELECT 'Pets:' as table_name;
SELECT * FROM pet;

SELECT 'Pets with Kind Info:' as query_name;
SELECT 
    pet.id, 
    pet.name, 
    pet.age, 
    pet.owner, 
    kind.name AS kind_name,
    kind.food,
    kind.sound
FROM pet
JOIN kind ON pet.kind_id = kind.id
ORDER BY pet.name;

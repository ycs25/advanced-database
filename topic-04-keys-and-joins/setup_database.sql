pragma foreign_keys = 1;

drop table pet;
drop table kind;

create table if not exists kind (
    id integer primary key autoincrement,
    name text not null,
    food text,
    sound text
);

insert 
    into kind(name, food, sound) 
    values ('dog','dogfood','bark');
insert 
    into kind(name, food, sound) 
    values ('cat','catfood','meow');

create table if not exists pet (
    id integer primary key autoincrement,
    name text not null,
    kind_id integer not null,
    age integer,
    owner text,
    foreign key (kind_id) references kind(id)
      on delete RESTRICT
      on update CASCADE 
);

insert 
    into pet(name, kind_id, age, owner) 
    values ('dorothy',1,9,'greg');
insert 
    into pet(name, kind_id, age, owner) 
    values ('suzy',1,9,'greg');
insert 
    into pet(name, kind_id, age, owner) 
    values ('casey',1,9,'greg');
insert 
    into pet(name, kind_id, age, owner) 
    values ('heidi',1,9,'greg');

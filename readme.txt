How to Run: python run.py
do not forget to create .env file and add:
    GMAIL=gmail
    PASSWORD=password
    DB_HOST=host
    DB_DATABASE=database
    DB_USER=user
    DB_PASSWORD=password
    DB_PORT=port


create 3 tables first for DB

create table users(
    id serial,
    name varchar,
    surname varchar,
    username varchar unique,
    gmail varchar unique,
    password varchar,
    superuser bool
);

create table books(
    id serial,
    name varchar unique,
    author varchar,
    category varchar,
    description varchar,
    unit int
);

create table ownedbooks(
    id serial,
    user_id int,
    book_id int
);
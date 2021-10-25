CREATE TABLE "Users" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "first_name" varchar,
  "last_name" varchar,
  "email" varchar,
  "bio" varchar,
  "username" varchar,
  "password" varchar,
  "created_on" date,
  "active" bit
);

insert into 'Users' values (null, 'erin', 'truman', 'erin@truman.com',"i am the queen of css!", 'cssQueen', '123', 'Wed Sep 15 2021 10:10:47', 0) 
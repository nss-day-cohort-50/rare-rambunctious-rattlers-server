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




CREATE TABLE "Posts" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "title" varchar,
  "publication_date" varchar,
  "content" varchar,
  "user_id" INTEGER,
  "category_id" INTEGER,
  FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`category_id`) REFERENCES `Categories`(`id`)
);


CREATE TABLE "Categories" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);

insert into 'Posts' values (null, 'Thanks, Trey', '10/25/21', 'Your CSS is p cool, too', 1, 1) 

SELECT *
FROM Users


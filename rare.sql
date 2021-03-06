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
CREATE TABLE "Tags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);

insert into 'Posts' values (null, 'David S. Pumpkins', '09/27/21', 'it fall', 1, 1); 

insert into 'Categories' values (null, 'David S. Pumpkins'); 

SELECT 
            p.id,
            p.title,
            p.publication_date,
            p.content,
            p.user_id,
            p.category_id,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.created_on,
            u.active,
            c.label
        from Posts p
        left join Users u
            on p.user_id = u.id
        left join Categories c
            on c.id = p.category_id


SELECT * from Posts

UPDATE publication_date 
  WHERE id=1 


  UPDATE Posts SET publication_date = "2021-08-21"
WHERE id = 4;

CREATE TABLE "Comments" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "subject" varchar,
  "content" varchar,
  "user_id" integer,
  "post_id" integer,
  foreign key('user_id') references 'Users'('id'),
  foreign key('post_id') references 'Posts'('id')
)

insert into 'Comments' values (null, 'python', 'i am so bad at python i dream of snakes made of byte strings squeezing ribcage', 1, 1, '09/27/21'); 

alter table 'Comments' rename column 'creationg_date' to 'creation_date'

delete from 'Comments'
where id = 1
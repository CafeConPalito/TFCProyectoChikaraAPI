create schema if not exists chikara;

create table if not exists user(
id_user INT auto_increment not null,
first_name varchar(150) not null,
first_last_name varchar(150) not null,
second_last_name varchar(150),
birthdate date not null,

primary key (id_user)

)
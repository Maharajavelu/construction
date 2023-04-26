-- Create table for builder
create table builder(id int primary key auto_increment, username varchar(50) not null, email varchar(100) not null, hashed_password varchar(100) not null, hashed_conpassword varchar(100) not null, companyname varchar(100) not null, industry varchar(100) not null, location varchar(100) not null, phone bigint(10) not null);


--Create table for users

create table users(id int primary key auto_increment, username varchar(50) not null, email varchar(100) not null, hashed_password varchar(100) not null, hashed_conpassword varchar(100) not null, location varchar(50) not null, phone bigint(10) not null);
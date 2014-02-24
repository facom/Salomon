create database salomon;
create user 'salomon'@'localhost' identified by '123';
grant all privileges on salomon.* to 'salomon'@'localhost';
flush privileges;

CREATE database WateringSystem;
create user 'nshakya'@'%' IDENTIFIED BY 'plantypi';
grant all on *.* to 'nshakya'@'%';
flush privileges;

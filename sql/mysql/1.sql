use test;
show tables;
desc t2;
create trigger trig_one
before insert
on t2 for each row
insert into t2 values(select id from inserted ,select)
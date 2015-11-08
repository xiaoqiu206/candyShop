-- sqlite3语法
create table push_log(
    id integer primary key,    
    event varchar(50),
    local_data varchar(500) null,
    push_data varchar(500) null,
    response_status char(10) null,
    response_data text default null,
    log_time datetime default(datetime(current_timestamp,'localtime'))
);

insert into log(event, local_data,push_data,response_data)
values('sending orders', 'tid:123', 'asdfafsd', 'sadfaf');

select * from log;


-- mysql语法
create table push_log(
    id integer primary key,    
    event varchar(50),
    local_data varchar(500) null,
    push_data varchar(500) null,
    response_status char(10) null,
    response_data text default null,
    log_time timestamp default CURRENT_TIMESTAMP
);
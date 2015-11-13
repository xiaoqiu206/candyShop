-- sqlite3语法
create table push_log(
    id integer primary key,    
    event varchar(50),
    local_data varchar(500) default null,
    push_data varchar(500) default null,
    response_status char(10) default null,
    response_data text default null,
    log_time datetime default(datetime(current_timestamp,'localtime'))
);


-- mysql语法
create table push_log(
    id integer primary key,    
    event varchar(50) default null,
    local_data varchar(500) default null,
    push_data varchar(500) default null,
    response_status char(10) default null,
    response_data longtext default null,
    log_time timestamp default CURRENT_TIMESTAMP
);
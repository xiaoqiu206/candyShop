create table log(
    id integer primary key,    
    event char(10),
    local_data varchar(100) null,
    push_data varchar(100) null,
    response_status char(10),
    response_data text default null,
    log_time datetime default(datetime(current_timestamp,'localtime'))
);

insert into log(event, local_data,push_data,response_data)
values('sending orders', 'tid:123', 'asdfafsd', 'sadfaf');

select * from log;
select * from stations;
select * from directions limit 10;

-- 根据起点和终点查找direction_id
-- start_id = 10
-- end_id = 13
select direction_id from directions where station_id = (
    select
        case 13>10 when true then max(station_id) else min(station_id) end
    from stations where line_id = (
        select line_id  from stations where station_id = 10
    )
);


-- 查找所有的换乘站
select * from stations where is_transfer=1 order by station_name;


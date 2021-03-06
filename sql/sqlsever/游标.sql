declare @tname nvarchar(50)
declare @cname nvarchar(50)

declare @sql nvarchar(500)

declare c_search cursor for
	select t.name, c.name 
	from sysobjects t 
		inner join syscolumns c on t.id=c.id 
	where t.type='U' and c.xtype in(56,167,175,231,239)
	order by t.name
	
open c_search
fetch next from c_search into @tname,@cname
while @@FETCH_STATUS=0
begin
	set @sql='select '+ @cname+ ' from '+ @tname +' where convert(varchar(100),'+ @cname+') like'+ '''%123%'''
	fetch next from c_search into @tname,@cname
	--print @sql
	EXECUTE sp_executesql @sql
end

close c_search
deallocate c_search
/*
select * from syscolumns 

select * from sysobjects where xtype='U'

select
 t.name, c.name 
from sysobjects t inner join syscolumns c on t.id = c.id
where t.xtype='U' */

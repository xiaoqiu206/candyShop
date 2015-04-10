USE [HBSERVER]
GO
/****** Object:  Trigger [dbo].[PrintResult]    Script Date: 01/10/2015 11:05:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER TRIGGER [dbo].[PrintResult] ON [dbo].[RecordIndex] 
FOR  UPDATE,INSERT
AS
declare @nFinish varchar(10)
declare @nfid int
declare @nPrint int
declare @strWx varchar(10)
declare @nUpdate char
declare @strPp varchar(10)

select @nFinish=IsFinish, @nfid=Fid, @nUpdate=IsUpdate, @nPrint=IsPrint  from INSERTED
if update(IsFinish) and @nFinish='1'
WAITFOR DELAY '00:00:05' --这行是新加的,测试如果不通过,删除这行,在执行,就可以还原了,时间可以自己修改,现在的时间是5秒,
begin
--插入到打印中
             if ((@nPrint <> 1) or (@nPrint is null)) and ((@nUpdate<>'T' ) or (@nUpdate is null))
             begin
                          select @strWx=hb_flag from vehiclechange where fid=@nFid
                          if @strWx='1' return
		insert INTO FinishPrint(fid) values(@nfid)
           	              insert INTO FinishShowResult(fid) values(@nfid)
 		insert INTO FinishUpdate(fid) values(@nfid)
	end
END

# coding=utf-8
'''
注意事项:
1. paramiko是第三方包,需要另外安装,如果是Python2.7.9以上或者python3.x,在命令行pip install paramiko可以安装  
2. 只能上传文件,不能上传目录
3. 远程路径名要加上文件名,不能只写目录
'''
import paramiko

username = 'root'
password = 'xxxxxxxx'

hostname = '121.40.249.48'
port = 22

t = paramiko.Transport((hostname, port))
t.connect(username=username, password=password)

sftp = paramiko.SFTPClient.from_transport(t)

sftp.put("C:/CODE/old-code/pycode/thread.py", "/home/qiuyang/thread")

t.close()

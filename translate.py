import localizable
import datetime
import os
import os.path

now = datetime.datetime.now()
recordPath = '/Users/XXX/Desktop/record'+now.strftime('%Y-%m-%d %H:%M:%S')
projPath = "/Users/XXX/files"
files = 0;
replaceTimes = 0;

os.mkdir(recordPath) 
for parent,dirnames,filenames in os.walk(projPath): 
	for filename in filenames:
		if filename.endswith(".h") or filename.endswith(".m"):
			filePath = os.path.join(parent,filename);
			rt = localizable.LocalizableFile(filePath,recordPath);
			if rt>0:
				print("filePath:%s %d处改动"%(filePath,rt))
				files = files + 1;
				replaceTimes = replaceTimes + rt;

print("修改了%d个文件，有%d处改动，日志地址：%s"%(files,replaceTimes,recordPath))


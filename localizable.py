# -*- coding: utf-8 -*-
import re
from opencc import OpenCC
openCC = OpenCC('s2hk') 
openCCS = OpenCC('hk2s')
arr = []
arrConst = []
def readFile(path):
	f = open(path,'r');
	content = f.readlines();
	f.close()
	return content;

def writeFile(path,content):
	f = open(path,'w')
	f.write(content);		
	f.close();

#以下语句不处理
#DKImageWithNames 
#//
##NSLog
def shouldIgnore(string):
	regs = ['DKImageWithNames',
	'^[ ]*//[ ]*',
	'^[ ]*NSLog\(@\"[ ]*'];
	for reg in regs:
		if re.search(reg,string):
			return True;
	regsShouldRecord = ['const[ ]*',
	'^[ ]*NSAssert[ ]*',
	'imageNamed[ ]*\:[ ]*'];
	for reg in regsShouldRecord:
		if re.search(reg,string):
			arrConst.append(string);
			return True;
	return False;

#判断是否已经处理过了，为true则需要处理，为false则已经处理过了
def haveReplace(string):
	regs = ['NSLocalizedString[ ]*\([ ]*$',
	'NSLocalizedStringWithDefaultValue[ ]*\([ ]*$',
	'NSLocalizedStringFromTable[ ]*\([ ]*$',
	'NSLocalizedStringFromTableInBundle[ ]*\([ ]*$',
	'localizedStringForKey[ ]*\:[ ]*$',
	'STTLocalizedString[ ]*\([ ]*$'];
	for reg in regs:
		if re.search(reg,string):
			return False;	
	return True;

def handleString(string,comment):
	result = re.search(r'@"[^\n"]*[\u4E00-\u9FA5][^\n"]*"',string);
	if result:
		if shouldIgnore(string):
			return string;
		stringBefore = string[:result.span()[0]]; 
		stringAfter = string[result.span()[1]:];
		stringMiddle = result.group(0);
		stringHK = openCC.convert(stringMiddle)
		stringResult = str();
		if haveReplace(stringBefore):
			stringReplace = "STTLocalizedString(%s)"%(stringHK);
			stringResult = stringBefore+stringReplace+stringAfter;
			addToLocalizable(stringHK,stringMiddle);
			return handleString(stringResult,comment);
		else:
			#继续处理后面的字符串
			stringAfter = handleString(stringAfter,comment);
			stringResult = stringBefore+stringHK+stringAfter;
			return stringResult;
	else:
		return string;	

def appendRecord(content,path):
	f = open(path,'a')
	f.write(content);		
	f.close();

def addToLocalizable(hkStr,sStr):
	hkStr = hkStr[1:];
	sStr = openCCS.convert(sStr[1:]);
	if arr.count((hkStr,sStr)) == 0:
		arr.append((hkStr,sStr))

def saveLocalizableFile(replaceRecord):
	if len(arr) == 0:
		return;
	content = str();
	for (hk,s) in arr:
		content = content + "%s = %s;\n"%(hk,s)
	f = open(replaceRecord,'w')
	f.write(content);		
	f.close();

def saveConstFile(replaceRecord):
	if len(arrConst) == 0:
		return;
	content = str();
	for s in arrConst:
		content = content + "%s\n"%(s)
	f = open(replaceRecord,'w')
	f.write(content);		
	f.close();


def LocalizableFile(filePath,recordPath):
	arr = [];
	arrConst = [];
	content = readFile(filePath);
	result = str();
	replaceRecord = str();
	times = 0;
	for i in range(0,len(content)):
		line = content[i];
		arr = filePath.split('/')
		comment = "%s rownumber:%d"%(arr[len(arr)-1],i+1)
		lineHandled = handleString(line,comment);
		if line != lineHandled:
			times = times+1;
			replaceRecord = replaceRecord+filePath+'\n'+str(times)+'.'+'rownumber:%d'%(i+1)+'\n'+ "before:"+line+"\n"+"after:"+lineHandled + "--------------------------------------------------------------------------------------\n"
		result = result+lineHandled
	if replaceRecord:
		appendRecord(replaceRecord+'\n',recordPath+'/changeLog');
		saveLocalizableFile(recordPath+'/file.strings')
		saveConstFile(recordPath+'/手动处理')
		# writeFile(filePath,result);
	return times;	
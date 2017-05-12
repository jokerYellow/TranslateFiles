# TranslateFiles
适用于 iOS 的国际化，也可扩展延伸。扫描文件夹下的文件，将简体转换为繁体，生成转换日志、strings文件以及需要手动转换的日志。
# translate.py
在 translate.py 里设置文件夹路径和日志路径。这个文件会扫描需要翻译的文件，目前的规则是扫描 **.h** 文件和 **.m** 文件，如需扫描其它文件，请自行处理。

# localizable.py
在 localizable.py 里设置正则规则以及字符串替换的规则。

1.  在 localizable.py 下有个注释，不屏蔽的话，会对文件进行改动，建议先看看日志没有问题再取消屏蔽。

```
# writeFile(filePath,result);
```

2.  设置字符串替换规则，当前的替换规则为`STTLocalizedString`
在这里设置字符串替换规则。

```
stringReplace = "STTLocalizedString(%s)"%(stringHK);
```

3.  在这个函数里加上字符串替换规则的正则，不然会导致死循环。

```
def shouldHandle(string):
```

4. optional：在这个函数里添加需要手动处理的正则，目前已经包含常量、断言、以及`[UIImage imageNamed:@"XXX"] `。
 
```
def shouldIgnore(string):
```

5.  然后直接执行，执行完毕之后记得查看日志，以及在时机成熟的时候，进行写操作。

```
python3.5 translate.py
```

6. 希望能帮助到有需要的人。




# HeyDB Docs
> pip install HeyDB  
HeyDB是一个轻量化内嵌式NoSQL的数据库  
具体数据存储结构:

    /Bucket(Folder)
        Page(hdb文件)
            Key
            Data  
## API文档
+ 使用class Bucket创建一个数据库会话
```python
import HeyDB
db=HeyDB.Bucket()
```
可选参数:  
path: Bucket的位置(默认为./database)  
**若指定path不存在则抛出dbError异常**
+ 使用open()打开或创建Page  
```python
import HeyDB
db=HeyDB.Bucket()
db.open("Page的名称")
```
必选参数:  
name: Page的名称  
可选参数:  
length: Page创建时生成随机密钥的长度(默认为2的16次方)  
default_key: Page创建时自定义密钥  
+ 使用delpage()删除Page
```python
import HeyDB
db=HeyDB.Bucket()
db.delpage("Page的名称")
```
可选参数:  
name: Page名称(若为空则删除当前会话Page)  
**若Page不存在则抛出dbError异常**
+ 使用find()或find_one()查找数据
```python
import HeyDB
db=HeyDB.Bucket()
db.open("Page的名称")
db.find("数据的键")
```
可选参数:  
key: 匹配数据的值(可为String List Dict)  
page_key: 自定义密钥  
当key为String时:  
返回数据中拥有key该键的数据  
当key为List时:  
返回数据中数据与List键全部匹配的数据  
当key为Dict时:  
返回数据中拥有此键值对的数据  
find_one()为返回第一条  
find()为返回全部  
+ 使用insert()写入数据
```python
import HeyDB
db=HeyDB.Bucket()
db.open("Page的名称")
db.insert({"key":"value"})
```
可选参数:  
data: 需要写入的数据(可为List Dict)  
page_key: 自定义密钥  
当data为List时:  
按照顺序写入其中Dict  
当data为Dict时:  
写入此Dict
+ 使用delete()或delete_one()删除数据
```python
import HeyDB
db=HeyDB.Bucket()
db.open("Page的名称")
db.delete({"key":"value"})
```
可选参数:  
key: 匹配数据的值(可为 Dict)  
page_key: 自定义密钥
删除数据中匹配key的数据   
delete_one()为删除第一条  
delete()为删除全部  
+ 使用update()或update_one()更新数据
```python
import HeyDB
db=HeyDB.Bucket()
db.open("Page的名称")
db.update({"key":"value1"},{"key":"value2"})
```
可选参数:  
key: 匹配数据的值  
data: 更新数据的值  
page_key: 自定义密钥  
将data插入或更改到匹配key的数据  
若匹配匹配不到数据则不做修改  
update_one()为更改第一条  
update()为更改全部  
+ 使用dblist获取当前会话全部Page
```python
import HeyDB
db=HeyDB.Bucket()
db.dblist
```
返回一个当前会话Page.hdb的列表
## 注意事项
Key的值决定单个数据的长度(默认为65536)  
进行任何读写删除修改操作时Page不存在依旧会抛出dbError异常  
dblist变量仅在会话创建时更新

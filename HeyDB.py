import os
import random
import json
class dbError(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self)
        self.ErrorInfo = ErrorInfo

    def __str__(self):
        return self.ErrorInfo
class Bucket:
    def __init__(self,path="./database",cache=False):
        """
        :param path: bucket路径
        :param cache: 是否使用缓存
        """
        self.path=path
        if not os.listdir("./").count("database") and path=="./database":
            os.mkdir("./database")
        elif not os.path.isdir(path):
            raise dbError("Bucket路径不存在")
        file_list=os.listdir(path)
        for i in file_list:
            if not i.find(".hdb")==len(i)-4:
                file_list.remove(i)
        self.dblist=file_list
        self.cache_type=cache

    def random_key(self,length):
        """
        :param length: 随机生成密钥的长度
        :return: 密钥
        """
        k=""
        if length<=57:
            k="".join(random.sample("""qwertyuiop[]\\asdfghjkl;'"zxcvbnm,./{}|:<>?!@#$%^&*()_+-=`~""",length))
        else:
            for i in range(length//57):
                k+="".join(random.sample("""qwertyuiop[]\\asdfghjkl;'"zxcvbnm,./{}|:<>?!@#$%^&*()_+-=`~""",57))
            k+="".join(random.sample("""qwertyuiop[]\\asdfghjkl;'"zxcvbnm,./{}|:<>?!@#$%^&*()_+-=`~""", length%57))
        return k

    def encode(self,s,k):
        """
        :param s: 需要加密的字符
        :param k: 密钥
        :return: 加密后字符
        """
        encry_str = ""
        for i, j in zip(s, k):
            # i为字符，j为秘钥字符
            temp = str(ord(i) + ord(j)) + '&'  # 加密字符 = 字符的Unicode码 + 秘钥的Unicode码
            encry_str = encry_str + temp
        return encry_str

    def decode(self,p,k):
        """
        :param p: 需要解密的字符
        :param k: 密钥
        :return: 解密后字符
        """
        dec_str = ""
        for i, j in zip(p.split("&")[:-1], k):
            # i 为加密字符，j为秘钥字符
            temp = chr(int(i) - ord(j))  # 解密字符 = (加密Unicode码字符 - 秘钥字符的Unicode码)的单字节字符
            dec_str = dec_str + temp
        return dec_str
    def open(self,name,length=2**16,default_key=""):
        """
        :param name: Page的名称
        :param length: 加密密钥长度,默认为2的16次方(密钥长度决定单条数据长度)
        :param default_key: 自定义加密密钥
        :return: 若存在Page则返回True,反而则创建并返回False
        """
        if os.path.isfile(self.path + "\\" + name + ".hdb"):
            self.page=self.path + "\\" + name + ".hdb"
            return True
        else:
            with open(self.path + "\\" + name + ".hdb","w")as f:
                if default_key:
                    f.write(default_key+"\n")
                else:
                    f.write(self.random_key(length)+"\n")
            self.page=self.path + "\\" + name + ".hdb"
            return False
    def delpage(self,name=""):
        """
        :param name: Page名称,若为空则删除当前Page
        :return: None
        """
        if name:
            if os.path.isfile(self.path + "\\" + name + ".hdb"):
                os.remove(self.path + "\\" + name + ".hdb")
            else:
                raise dbError("无此Page")
        elif self.page:
            os.remove(self.page)
        else:
            raise dbError("未指定Page")
    def find_one(self,key="",page_key=""):
        """
        :param key: 若为Str则匹配键,若为List则匹配所有键,若为Dict则匹配所有键值对
        :param page_key: 自定义加密密钥
        :return: 有结果则返回第一条数据dict 无则返回None
        """
        if os.path.isfile(self.page):
            if key:
                with open(self.page, "r") as f:
                    if not page_key:
                        page_key=f.readline()
                    encode_data = f.read().splitlines()
                    for i in encode_data:
                        data=json.loads(self.decode(i, page_key))
                        if type(key) is type("string"):
                            if key in data:
                                return data
                        elif type(key) is type(["list"]):
                            if set(data.keys()).intersection(set(key)) == set(key):
                                return data
                        elif type(key) is type({"dict": "dict"}):
                            for k in key.keys():
                                if not data.get(k) == key[k]:
                                    break
                            else:
                                return data

            else:
                with open(self.page,"r")as f:
                    if not page_key:
                        page_key=f.readline()
                    encode_data = f.read().splitlines()
                    return json.loads(self.decode(encode_data[0], page_key))
        else:
            raise dbError("Page不存在")
    def find(self, key="", page_key=""):
        """
        :param key: 若为Str则匹配键,若为List则匹配所有键,若为Dict则匹配所有键值对
        :param page_key: 自定义加密密钥
        :return: 有结果则返回全部数据list 无则返回None
        """
        if os.path.isfile(self.page):
            if key:
                with open(self.page, "r") as f:
                    if not page_key:
                        page_key = f.readline()
                    encode_data = f.read().splitlines()
                    result=[]
                    for i in encode_data:
                        data = json.loads(self.decode(i, page_key))
                        if type(key) is type("string"):
                            if key in data:
                                result.append(data)
                        elif type(key) is type(["list"]):
                            if set(data.keys()).intersection(set(key))==set(key):
                                result.append(data)
                        elif type(key) is type({"dict":"dict"}):
                            for k in key.keys():
                                if not data.get(k)==key[k]:
                                    break
                            else:
                                result.append(data)
                    return result

            else:
                with open(self.page, "r") as f:
                    if not page_key:
                        page_key = f.readline()

                    encode_data = f.read().splitlines()
                    data=[]
                    for i in encode_data:
                        data.append(json.loads(self.decode(i, page_key)))
                    return data
        else:
            raise dbError("Page不存在")
    def insert(self,data,page_key=""):
        """
        :param data: 若为list写入其中全部dict 若为dict则写入此dict
        :param page_key: 自定义加密密钥
        :return: None
        """
        if os.path.isfile(self.page):
            with open(self.page,"r")as r:
                if not page_key:
                    page_key = r.readline()
            if type(data) is type([]):
                with open(self.page,"a")as f:
                    encode_data=""
                    for i in data:
                        encode_data+=self.encode(json.dumps(i),page_key)+"\n"
                    f.write(encode_data)
            elif type(data) is type({}):
                with open(self.page, "a") as f:
                    f.write(self.encode(json.dumps(data), page_key)+"\n")
        else:
            raise dbError("Page不存在")
    def delete_one(self,key,page_key=""):
        """
        :param key: 要删除数据中包含的键值对
        :param page_key: 自定义加密密钥
        :return: 删除成功返回True
        """
        if os.path.isfile(self.page):
            with open(self.page, "r") as f:
                if not page_key:
                    page_key = f.readline()
                encode_data = f.read().splitlines()
                for i in encode_data:
                    data = json.loads(self.decode(i, page_key))
                    if type(key) is type({"dict": "dict"}):
                        for k in key.keys():
                            if not data.get(k) == key[k]:
                                break
                        else:
                            encode_data.remove(i)
                            with open(self.page,"w")as w:
                                encode_data.insert(0,page_key[:len(page_key)-2])
                                w.write("\n".join(encode_data)+"\n")
                            return True
        else:
            raise dbError("Page不存在")
    def delete(self,key,page_key=""):
        """
        :param key: 要删除数据中包含的键值对
        :param page_key: 自定义加密密钥
        :return: None
        """
        if os.path.isfile(self.page):
            with open(self.page, "r") as f:
                if not page_key:
                    page_key = f.readline()
                encode_data = f.read().splitlines()
                remove_list=[]
                for i in encode_data:
                    data = json.loads(self.decode(i, page_key))
                    if type(key) is type({"dict": "dict"}):
                        for k in key.keys():
                            if not data.get(k) == key[k]:
                                break
                        else:
                            remove_list.append(i)
                for i in remove_list:
                    encode_data.remove(i)
                with open(self.page, "w") as w:
                    encode_data.insert(0, page_key[:len(page_key) - 2])
                    w.write("\n".join(encode_data) + "\n")
        else:
            raise dbError("Page不存在")
    def update_one(self,key,new_data,page_key=""):
        """
        :param key: 匹配数据的键值对
        :param new_data: 修改的键值对
        :param page_key: 自定义加密密钥
        :return: 更改成功返回True
        """
        if os.path.isfile(self.page):
            with open(self.page, "r") as f:
                if not page_key:
                    page_key = f.readline()
                encode_data = f.read().splitlines()
                for i in encode_data:
                    data = json.loads(self.decode(i, page_key))
                    for k in key.keys():
                        if not data.get(k) == key[k]:
                            break
                    else:
                        data.update(new_data)
                        encode_data.insert(encode_data.index(i), self.encode(json.dumps(data), page_key))
                        encode_data.pop(encode_data.index(i))
                        with open(self.page, "w") as w:
                            encode_data.insert(0, page_key[:len(page_key) - 2])
                            w.write("\n".join(encode_data) + "\n")
                        return True
        else:
            raise dbError("Page不存在")

    def update(self,key,new_data,page_key=""):
        """
        :param key: 匹配数据的键值对
        :param new_data: 修改的键值对
        :param page_key: 自定义加密密钥
        :return: None
        """
        if os.path.isfile(self.page):
            with open(self.page, "r") as f:
                if not page_key:
                    page_key = f.readline()
                encode_data = f.read().splitlines()
                for i in encode_data:
                    data = json.loads(self.decode(i, page_key))
                    for k in key.keys():
                        if not data.get(k) == key[k]:
                            break
                    else:
                        data.update(new_data)
                        encode_data.insert(encode_data.index(i), self.encode(json.dumps(data), page_key))
                        encode_data.pop(encode_data.index(i))
                with open(self.page, "w") as w:
                    encode_data.insert(0, page_key[:len(page_key) - 2])
                    w.write("\n".join(encode_data) + "\n")
        else:
            raise dbError("Page不存在")



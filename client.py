import copy
from unittest import case
from server import Server 
from utils import decrypt, encrypt
import hashlib

class Client:

    def __init__(self, key):
        self.key = key
        self.isSetup = False
        self.emm = Server()
        self.updata = {}
        self.temp_data = {}
        
    def setup_server(self):
        if self.isSetup:
            print("Server has been setup!")
            return
        self.emm.setup(self.temp_data)
        self.emm.padding()
        self.emm.enc(self.key)
        self.isSetup = True
        # 清空temp_data
        self.temp_data = {}
    
    def rebuild_server(self):
        self.isSetup = False
        # 下载数据
        self.temp_data = copy.deepcopy(self.emm.data)
        # 逐项解密
        for key in self.temp_data:
            self.temp_data[key] = [decrypt(item, self.key).decode('utf-8') for item in self.temp_data[key]]
        # 剔除填充元素
        self.temp_data[key] = [item for item in self.temp_data[key] if item.split(',')[0] != 'key_padding']
        # 融合更新
        for key in self.updata:
            for up in self.updata[key]:
                op = up[0]
                val = up[1:]
                if op == 'I': 
                    self.insert(key, val)
                elif key in self.updata:
                    if op == 'D':
                        self.delete(key, val)
                    elif op == 'U':
                        old_val = up.split(',')[0][1:]
                        new_val = up.split(',')[1]
                        self.update(key, old_val, new_val)

        # 上传填充加密
        self.emm.rebuild(self.temp_data)
        self.emm.padding()
        self.emm.enc(self.key)
        # 清空updata和temp_data
        self.updata = {}
        self.temp_data = {}
        self.isSetup = True

    def insert(self, key, values):
        if not self.isSetup:
            hash_key = hashlib.sha256(key.encode('utf-8')).hexdigest()[0:16]    # 只截取16位
            if hash_key not in self.temp_data:
                self.temp_data[hash_key] = []
            self.temp_data[hash_key].append(key + ',' + values)
        else:
            if key  not in self.updata:
                self.updata[key] = []
            self.updata[key].append('I' + values)
    
    def delete(self, key, value):
        if not self.isSetup:
            # 删除data中对应项
            hash_key = hashlib.sha256(key.encode('utf-8')).hexdigest()[0:16]
            self.temp_data[hash_key].remove(key + ',' + value)
        else:
            if key  not in self.updata:
                self.updata[key] = []
            self.updata[key].append('D' + value)
    
    def update(self, key, old_value, new_value):
        if not self.isSetup:
            hash_key = hashlib.sha256(key.encode('utf-8')).hexdigest()[0:16]
            index = self.temp_data[hash_key].index(key + ',' +old_value)
            self.temp_data[hash_key][index] = key + ',' + new_value
        else:
            if key  not in self.updata:
                self.updata[key] = []
            self.updata[key].append( 'U' + old_value + ',' + new_value)
    
    def query(self, key):
        ret = []
        hash_key = hashlib.sha256(key.encode('utf-8')).hexdigest()[0:16]
        if self.isSetup:
            
            ret = self.emm.query(hash_key)
            # 将ret中元素逐个解密
            for i in range(len(ret)):
                ret[i] = decrypt(ret[i], self.key)
        else:
            if hash_key in self.temp_data:
                ret = self.temp_data[hash_key]

        query_ret = []
        for r in ret:
            # 以 _ 为标志切割r, 前一部分为key，后一部分为value
            if type(r) == bytes:
                r = r.decode('utf-8')
            if r.split(',')[0] == key:
                query_ret.append(r.split(',')[1])
        # 解析更新
        retup = []
        if key in self.updata:
            retup = self.updata[key]

        if key in self.updata:
            for up in self.updata[key]:
                
                op = up[0]
                val = up[1:]
                if op == 'I':  
                    query_ret.append(val)
                elif op == 'D':
                        query_ret.remove(val)
                elif op == 'U':
                    old_val = up.split(',')[0][1:]
                    new_val = up.split(',')[1]
                    index = query_ret.index(old_val)
                    query_ret[index] = new_val
        return query_ret, ret, retup
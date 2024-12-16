import copy
import utils

class Server:
    
    def __init__(self):
        self.data = {}

    # 初始化, 传入数据
    def setup(self, data):
        # 获取data字典的value数组的最大长度
        self.data = copy.deepcopy(data)
        self.l = max([len(i) for i in data.values()])
    
    def padding(self):
        padding_index = 0
        # 将data字典每个value数组的长度用随机数补齐为l
        for key in self.data:
            this_len = len(self.data[key])
            if this_len < self.l:
                for i in range(this_len, self.l):
                    self.data[key].append( "key_padding," + str(padding_index))
                    padding_index += 1

    def enc(self, password):
        # 加密data字典的value数组
        for key in self.data:
            if len(self.data[key]) != self.l:
                print('未填充!')
            for i in range(self.l):
                self.data[key][i] = utils.encrypt(self.data[key][i], password)

    def query(self, key):
        # 查询data字典中key对应的value数组
        ret = []
        if key in self.data:
            ret = copy.deepcopy(self.data[key]) # 注意需要深拷贝
        return ret
    
    def rebuild(self, new_data):
        # 重建data字典
        self.data = {}
        self.data = copy.deepcopy(new_data)
        self.l = max([len(i) for i in new_data.values()])


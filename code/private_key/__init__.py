def read_propertier(path) -> dict:
    rs = {}
    try:
        with open(path, encoding='utf-8') as f:
            while True:
                content = f.readline()
                if len(content) == 0:
                    break
                else:
                    v = content.split('=')
                    if len(v) == 2:
                        rs[v[0].strip()] = v[1].strip()
    except FileExistsError as e :
        print(e)
    except FileNotFoundError as e:
        print(e)
    
    return rs

class Account() :
    '''
    保存metemask账户的信息
    '''

    def __init__(self, args) -> None:
        self.__address = args.get('address')
        self.__key = args.get('key')

    @property
    def address(self):
        return self.__address
    @property
    def key(self):
        return self.__key
## 读取配置文件信息
prop = read_propertier(r'code\private_key\key.properties')
account = Account(prop)
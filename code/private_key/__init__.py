import utils.utils_file as u_file

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
prop = u_file.read_propertier(r'code\private_key\key.properties')
account = Account(prop)
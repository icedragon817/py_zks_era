## 链路枚举信息
class ChainInfo() :
    __all = {}

    def __init__(self, name, rpc) -> None:
        self.__name = name
        self.__rpc = rpc

    @property
    def rpc(self):
        return self.__rpc

    @classmethod
    def add_instance(cls, name, rpc):
        cls.__all[name] = ChainInfo(name, rpc)
    
    @classmethod
    def get_rpc(cls, name):
        for i, v in cls.__all.items():
            if i == name :
                return v.rpc

def add_chain(name, rpc):
    ChainInfo.add_instance(name, rpc)

def get_chain(name):
    return ChainInfo.get_rpc(name)

add_chain('zk_dev', 'https://zksync-era-testnet.blockpi.network/v1/rpc/public')
add_chain('goerli', 'https://goerli.infura.io/v3/')
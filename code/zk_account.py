'''
存放账户信息
'''
import private_key as pk
import utils.utils_chain as uc
import config

from eth_account import Account
from eth_account.signers.local import LocalAccount
from zksync2.module.module_builder import ZkSyncBuilder
from web3 import Web3
class Env():
    key = pk.account.key
    account: LocalAccount = Account.from_key(key)
    address = account.address

    def __init__(self) -> None:
        ## 默认测试网络
        # self.test()
        self.main()
    
    ## 测试网络
    def test(self):
        self.env = 'test'
        self.zk_url = 'https://zksync-era-testnet.blockpi.network/v1/rpc/public'
        self.sdk = ZkSyncBuilder.build(self.zk_url)
        self.default_eth = 'goerli'
        self.eth_web3 = Web3(Web3.HTTPProvider(uc.get_chain(self.default_eth)))
        config.debug = True

    ## 主网
    def main(self):
        self.env = 'main'
        self.zk_url = 'https://mainnet.era.zksync.io'
        self.sdk = ZkSyncBuilder.build(self.zk_url)
        self.default_eth = 'eth'
        self.eth_web3 = Web3(Web3.HTTPProvider(uc.get_chain(self.default_eth)))
        config.debug = False
    
    def set_env(self, info):
        if info == 'test':
            self.test()
        else:
            self.main()
    @property
    def info(self):
        return f'网络:{self.env}, rpc:{self.zk_url}, defalut:{self.default_eth}, main_contract:{self.sdk.zksync.zks_main_contract()}'

## 环境变量
env = Env()

## 账户信息
# my_key = pk.account.key
# my_account = Account.from_key(my_key)

# zk_url = 'https://mainnet.era.zksync.io'

# ## 测试网络
# zk_dev_url = 'https://zksync-era-testnet.blockpi.network/v1/rpc/public'
# goerli_url = 'https://goerli.infura.io/v3/'


# ## 加载sdk
# sdk = ZkSyncBuilder.build(zk_url)
# zk_web = ZkSyncBuilder.build(zk_url)

# from web3 import Web3
# sdk = Web3(Web3.HTTPProvider(zk_dev_url)) 
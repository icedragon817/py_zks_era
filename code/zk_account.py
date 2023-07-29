'''
存放账户信息
'''
import private_key as pk

from eth_account import Account
from zksync2.module.module_builder import ZkSyncBuilder

## 账户信息
my_key = pk.account.key
my_account = Account.from_key(my_key)

# zk_url = 'https://testnet.era.zksync.dev' # 测试网络

## 测试网络
zk_dev_url = 'https://zksync-era-testnet.blockpi.network/v1/rpc/public'
goerli_url = 'https://goerli.infura.io/v3/'


## 加载sdk
sdk = ZkSyncBuilder.build(zk_dev_url)

# from web3 import Web3
# sdk = Web3(Web3.HTTPProvider(zk_dev_url))
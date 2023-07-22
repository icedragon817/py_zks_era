'''
存放账户信息
'''
import private_key as pk

from eth_account import Account
from zksync2.module.module_builder import ZkSyncBuilder

## 账户信息
my_key = pk.account.key
my_account = Account.from_key(my_key)

zk_url = 'https://testnet.era.zksync.dev'

## 加载sdk
sdk = ZkSyncBuilder.build(zk_url)
import private_key as pk
import help_info as hi

from zksync2.module.module_builder import ZkSyncBuilder
from zksync2.core.types import EthBlockParams
ZKSYNC_PROVIDER = "https://zksync2-testnet.zksync.dev"

my_account = pk.account.address
use_cnt = {}
## 注册
def register(op, info=None):
    if use_cnt.get(op) == None:
        use_cnt[op] = 0
        hi.HelpInfo.register(op, info)
    def decorator(func):
        def wrapper(*args, **kw):
            use_cnt[op] += 1
            return func(*args, **kw)
        return wrapper
    return decorator

register('-1', '查询余额， 参数1：账户地址（默认自身）')
@register('-1')
def check_balance(acc=my_account):
    '''
    查询余额
    参数：账户地址（默认自己地址）
    '''
    acc = input('请输入账户地址，默认当前账户')
    acc = acc or my_account
    try:
        zksync_web3 = ZkSyncBuilder.build(ZKSYNC_PROVIDER)
        zk_balance = zksync_web3.zksync.get_balance(acc, EthBlockParams.LATEST.value)
        print(f"Balance: {zk_balance}")
    except Exception as e:
        print('调用失败', e)
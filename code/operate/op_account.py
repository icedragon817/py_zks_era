import operate as op
import zk_account as zk_acc

from zksync2.core.types import EthBlockParams
from zksync2.signer.eth_signer import PrivateKeyEthSigner

## 查询余额操作
op.register('-1', '查询余额， 参数1: 账户地址（默认自身）')
@op.register('-1')
def check_balance(acc=zk_acc.my_account.address):
    '''
    查询余额
    参数：账户地址（默认自己地址）
    '''
    sdk = zk_acc.sdk
    acc = input('请输入账户地址，默认当前账户')
    acc = acc or zk_acc.my_account.address
    try:
        zk_balance = sdk.zksync.get_balance(acc, EthBlockParams.LATEST.value)
        print(f"Balance: {zk_balance}")
    except Exception as e:
        print('调用失败', e)

## 生成签名
op.register('-2', '生成签名')
@op.register('-2')
def generate_sign():
    chain_id = zk_acc.sdk.zksync.chain_id
    try:
        signer = PrivateKeyEthSigner(zk_acc.my_account, chain_id)
        # _sign = signer.sign_typed_data()
        print(signer)
    except Exception as e:
        print('调用失败', e)
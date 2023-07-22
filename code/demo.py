import private_key as pk
import help_info as hi
import operate as op
import logging
## 日志默认是WARNING 需要调整级别
logging.basicConfig(level=logging.INFO)

## 账户信息
my_account = pk.account.address
my_key = pk.account.key
# print(my_key)

## 加载sdk
from zksync2.module.module_builder import ZkSyncBuilder

sdk = ZkSyncBuilder.build("https://testnet.era.zksync.dev")

### 各类操作 通过传递的参数区分
def operate(cmd):
    if cmd == '-1' :
        op.check_balance()
    pass

if __name__ == "__main__":
    while True:
        cmd = input('请输入指令, 帮助请输入"help" or "-h" >>> ').strip()
        if cmd == 'help' or cmd == "-h":
            print(hi.HelpInfo.print())
        else:
            operate(cmd)
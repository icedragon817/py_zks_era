import zk_account as acc
import utils.utils_chain as uc
import help_info as hi
import operate as op
from operate import op_account as op_acc
import logging
## 日志默认是WARNING 需要调整级别
logging.basicConfig(level=logging.INFO)

### 各类操作 通过传递的参数区分
def operate(cmd) -> bool:
    if cmd == '-1' :
        op_acc.check_balance()
    elif cmd == '-2':
        target_addr = input('请输入要转账的地址>>>')
        amount = float(input('请输入数量>>>'))
        op_acc.transfer_eth(target_addr, amount)
    elif cmd == '-3':
        amount = float(input('请输入数量>>>'))
        print(op_acc.deposit(amount))
    elif cmd == '-4':
        amount = float(input('请输入数量>>>'))
        print(op_acc.withdraw(amount))
    elif cmd == '0':
        bridge_addresses = acc.sdk.zksync.zks_get_bridge_contracts()
        print(bridge_addresses)
    elif cmd == 'exit' or cmd == '-e' :
        return True

if __name__ == "__main__":
    while True:
        result = False
        cmd = input('请输入指令, 帮助"help"，退出"exit" >>> ').strip()
        if cmd == 'help' or cmd == "-h":
            print(hi.HelpInfo.print())
        else:
            try:
                result = operate(cmd)
            except Exception as e:
                print('调用失败: ', e)
        
        if result: 
            print(op.exit())
            confirm = input("是否确定退出(Y/N) >>> ").lower()
            if confirm == 'y' or confirm == 'yes' :
                break
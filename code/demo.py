import zk_account as acc
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
        op_acc.generate_sign()
    elif cmd == 'exit' or cmd == '-e' :
        return True

if __name__ == "__main__":
    while True:
        result = False
        cmd = input('请输入指令, 帮助"help"，退出"exit" >>> ').strip()
        if cmd == 'help' or cmd == "-h":
            print(hi.HelpInfo.print())
        else:
            result = operate(cmd)
        
        if result: 
            print(op.exit())
            confirm = input("是否确定退出(Y/N) >>> ").lower()
            if confirm == 'y' or confirm == 'yes' :
                break
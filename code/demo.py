import zk_account as acc
import utils.utils_chain as uc
import help_info as hi
import operate as op

from eth_account import Account
import logging
## 日志默认是WARNING 需要调整级别
logging.basicConfig(level=logging.INFO)

### 各类操作 通过传递的参数区分
def operate(cmd) -> bool:
    account = acc.my_account
    if cmd == '-1' :
        address = input('请输入账户地址，默认当前账户>>>').strip()
        address = address or account.address
        op.base_operate(cmd, account, address)
    elif cmd == '-2':
        target_addr = input('请输入要转账的地址>>>')
        amount = float(input('请输入数量>>>'))
        op.base_operate(cmd, account, target_addr, amount)
    elif cmd == '-3':
        amount = float(input('请输入数量>>>'))
        op.base_operate(cmd, account, amount)
    elif cmd == '-4':
        amount = float(input('请输入数量>>>'))
        op.base_operate(cmd, account, amount)
    elif cmd == '-com':
        ## 组合操作账户key，默认当前账户
        key = input('操作账户key，默认当前配置账户 >>>').strip()
        ## 操作文件路径
        op_file = input('操作文件路径，默认相对路径code\csv\operate.csv >>>').strip()
        op.senior_operate(cmd, key, op_file)
        print('操作结束，具体日志记录在D：\\eth\operate.log')
    elif cmd == '-batch':
        ## 批量操作 key_file 文件路径
        keys_file = input('账号列表路径，默认相对路径code\csv\keys.csv >>>').strip()
        ## 操作文件路径
        op_file = input('操作文件路径，默认相对路径code\csv\operate.csv >>>').strip()
        op.senior_operate(cmd, keys_file, op_file)
        print('操作结束，具体日志记录在D：\\eth\operate.log')
    elif cmd == 'exit' or cmd == '-e' :
        return True
    else: 
        op.base_operate(cmd, account)

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
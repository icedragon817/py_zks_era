from zk_account import env
import help_info as hi
import operate as op
import config

from eth_account import Account
import logging
import traceback
## 日志默认是WARNING 需要调整级别
logging.basicConfig(level=logging.INFO)

### 各类操作 通过传递的参数区分
def operate(cmd) -> bool:
    account = env.account
    if cmd == '-1' :
        address = input('请输入账户地址，默认当前账户>>>').strip()
        chain = input('请输入链路，默认ERA链>>>').strip()
        address = address or account.address
        op.base_operate(cmd, account, address=address, chain=chain)
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
    elif cmd == '-5':
        path = input('sol或者json文件路径>>>')
        op.base_operate(cmd, account, path=path)
    elif cmd == '-com':
        ## 组合操作账户key，默认当前账户
        key = input('操作账户key，默认当前配置账户 >>>').strip()
        ## 操作文件路径
        op_file = input(f'操作文件路径，默认相对路径{config.op_file_path} >>>').strip()
        log_path = op.senior_operate(cmd, key, op_file)
        print(f'操作结束，具体日志记录在{log_path}')
    elif cmd == '-batch':
        ## 批量操作 key_file 文件路径
        keys_file = input(f'账号列表路径，默认相对路径{config.keys_file_path} >>>').strip()
        ## 操作文件路径
        op_file = input(f'操作文件路径，默认相对路径{config.op_file_path} >>>').strip()
        log_path = op.senior_operate(cmd, keys_file, op_file)
        print(f'操作结束，具体日志记录在{log_path}')
    elif cmd == '-random':
        ## 批量操作 key_file 文件路径
        keys_file = input(f'账号列表路径，默认相对路径{config.keys_file_path} >>>').strip()
        ## 操作文件路径
        op_file = input(f'配置文件路径，默认相对路径{config.random_config_file} >>>').strip()
        log_path, task_id = op.senior_operate(cmd, keys_file, op_file)
        print(f'操作结束，具体日志记录在{log_path}, task_id:{task_id}')
    elif cmd == 'test':
        op.senior_operate(cmd)
        pass
    elif cmd == 'main':
        env.main()
        pass
    elif cmd == 'env':
        env_info = input('输入环境>>>')
        env.set_env(env_info)
        print(env.info)
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
                # if config.debug:
                    ## Debug模式 打印具体错误，便于排除
                    print(traceback.format_exc())
                # else:
                #     print('调用失败: ', e)
        
        if result: 
            print(op.exit())
            confirm = input("是否确定退出(Y/N) >>> ").lower()
            if confirm == 'y' or confirm == 'yes' :
                break
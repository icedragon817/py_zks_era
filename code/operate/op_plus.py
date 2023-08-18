## 高阶操作

import operate as op
import config
import zk_account as zk_acc
import utils.utils_file as u_file
import utils.utils_thread as u_thread
from eth_account import Account

import time
## 指令对象
class Op_cmd():
    _args = ()

    def __init__(self, *params) -> None:
        self._cmd = params[0]
        if len(params) > 1 :
            self._args = params[1:]
    
    @property
    def cmd(self):
        return self._cmd
    @property
    def args(self) -> tuple:
        return self._args
## 批量操作
op.register('-batch', '批量操作， 需准备账号key列表和操作指令集')
@op.register('-batch')
def batch(keys_file, op_file):
    '''
    批量操作
    参数：keys_file 存储账号private_key的csv文件路径
    参数：op_file 存储操作指令文件路径，操作指令即是 -1, -2等简单操作的指令集合
    '''
    keys_file = keys_file or config.keys_file_path
    op_file = op_file or config.op_file_path
    ## 读取keys文件,获得账户列表
    accounts = u_file.read_csv_to_arr(keys_file)
    ## 开始写日志文件
    log_path = f'{config.op_log_pix}-{int(time.time())}.log'
    u_file.write_op_log(log_path, 'w', 'batch operate start ====>>\n')
    ## 遍历账户列表，开启多线程，执行组合操作
    u_thread.batch_execute(accounts, combine, op_file, log_path, 'a')
    return log_path

## 组合操作
op.register('-com', '组合操作， 操作指令集文件')
@op.register('-com')
def combine(key, op_file, log_path=None, f_mode='w'):
    '''
    组合操作
    参数：key 操作账户，默认当前账户key
    参数：op_file 存储操作指令文件路径，操作指令即是 -1, -2等简单操作的指令集合
    '''
    key = key or zk_acc.my_key
    op_file = op_file or config.op_file_path
    ## 获取账号对象
    account = Account.from_key(key)
    ## 开始写日志
    if log_path == None:
        log_path = f'{config.op_log_pix}-{int(time.time())}.log'
    
    log_info = f'account:{account.address} start operate ===>\n'
    u_file.write_op_log(log_path, f_mode, log_info)
    ## 读取指令集文件，获取指令列表
    cmds = u_file.read_csv_to_arr(op_file, cls=Op_cmd)
    ## 遍历执行指令
    for info in cmds:
        print(f'操作指令{info.cmd}')
        rs = op.base_operate(info.cmd, account, *info.args)
        u_file.write_op_log(log_path, 'a', f'account:{account.address}, cmd:{info.cmd}, {rs}\n')
    
    return log_path


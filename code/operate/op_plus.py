## 高阶操作

import operate as op
import zk_account as zk_acc
import utils.utils_file as u_file
import threading
from eth_account import Account

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
    keys_file = keys_file or r'code\csv\keys.csv'
    op_file = op_file or r'code\csv\operate.csv'
    ## 读取keys文件,获得账户列表
    accounts = u_file.read_csv_to_arr(keys_file)
    ## 遍历账户列表，开启多线程，执行组合操作
    t_list = []
    for key in accounts:
        print(f'开始操作，key:{key}')
        ## 开启新线程，进行组合操作
        t = threading.Thread(target=combine, name="combine", args=(key, op_file))
        t.start()
        t_list.append(t)
    
    for t in t_list:
        t.join()

## 组合操作
op.register('-com', '组合操作， 操作指令集文件')
@op.register('-com')
def combine(key, op_file):
    '''
    组合操作
    参数：key 操作账户，默认当前账户key
    参数：op_file 存储操作指令文件路径，操作指令即是 -1, -2等简单操作的指令集合
    '''
    key = key or zk_acc.my_key
    op_file = op_file or r'code\csv\operate.csv'
    print(op_file)
    ## 获取账号对象
    account = Account.from_key(key)
    ## 读取指令集文件，获取指令列表
    cmds = u_file.read_csv_to_arr(op_file, cls=Op_cmd)
    ## 遍历执行指令
    for info in cmds:
        print(f'操作指令{info.cmd}')
        op.base_operate(info.cmd, account, *info.args)
    pass


## 高阶操作
from zk_account import env
import operate as op
from operate import op_task
import config
import utils.utils_file as u_file
import utils.utils_thread as u_thread
from eth_account import Account

import time

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
    key = key or env.key
    op_file = op_file or config.op_file_path
    ## 获取账号对象
    account = Account.from_key(key)
    ## 开始写日志
    if log_path == None:
        log_path = f'{config.op_log_pix}-{int(time.time())}.log'
    
    log_info = f'account:{account.address} start operate ===>\n'
    u_file.write_op_log(log_path, f_mode, log_info)
    ## 读取指令集文件，获取指令列表
    cmds = u_file.read_csv_to_arr(op_file, cls=op.Op_cmd)
    ## 遍历执行指令
    for info in cmds:
        print(f'操作指令{info.cmd}')
        rs = op.base_operate(info.cmd, account, *info.args)
        u_file.write_op_log(log_path, 'a', f'account:{account.address}, cmd:{info.cmd}, {rs}\n')
    
    return log_path

## 批量随机操作
op.register('-random', '随机操作， 操作指令集文件')
@op.register('-random')
def op_random(keys_file, config_file):
    '''
    批量随机操作
    在随机时间点选取随机账号执行随机操作
    例如：账号[1,2,3], 时间点[0-24]，操作[1,2,3,4]
    以小时为单位，每小时执行异常
    - 先确定当前时间段随机执行的账号
    - 多线程执行，每个账号随机确认具体的执行时间，然后等待具体时间点到达
    - 到达执行时间，随机选取操作执行
    - 执行结束，线程销毁等待下一个时间周期
    参数: keys_file 存储账号private_key的csv文件路径
    参数: config_file 具体配置，包含参数(时间段，总操作次数，随机账号数，操作金额，随机操作池)
    '''
    ## 创建任务对象并启动
    keys_file = keys_file or config.keys_file_path
    task = op_task.Task(keys_file, config_file)
    ## 执行逻辑在task对象的run函数处理
    task.run()
    return task.log_path, task.id

## 查询任务信息
op.register('-a_task', '查询所有任务， 参数: taskid')
@op.register('-a_task')
def task_info():
    '''
    查询任务信息
    查询当前正在进入的任务信息
    参数: task_id, 执行任务时会返回，也可以通过a_task指令查询
    '''
    ## 查找任务对象
    tasks = op_task.Task.get_all_task()
    ## 输出任务信息
    for task in tasks :
        task: op_task.Task
        print(f'task:{task.id} {task.status}, start in {task.start_time}')

## 查询任务信息
op.register('-i_task', '查询任务信息， 参数: taskid')
@op.register('-i_task')
def task_info(task_id):
    '''
    查询任务信息
    查询当前正在进入的任务信息
    参数: task_id, 执行任务时会返回，也可以通过a_task指令查询
    '''
    ## 查找任务对象
    task: op_task.Task = op_task.Task.get_task(task_id)
    ## 输出任务信息
    print(task.info)
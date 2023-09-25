import time

import config
import utils.utils_file as u_file
import utils.utils_thread as u_thread
import utils.utils_random as u_random
import utils.utils_time as u_time
from eth_account import Account

import operate as op
class Task():
    '''
    调度任务
    保存调度信息
    '''
    tasks: dict = {}
    __config: dict = None
    
    __id: int = 0
    __keys: list = None
    __start: int = 0
    __end: int = 24
    __account_num: list = None
    __op_pools: list = None
    __op_weights: list = None
    __days: int = 1
    __interval: int = 1
    
    __log: str = None
    __status: int = 0
    __start_ts: int = None

    ## 执行主线程
    __main_t: u_thread.MyThread = None

    def __init__(self, keys_file, config_file=None) -> None:
        self.__id = self.id_increment()
        ## 读取配置
        config_file = config_file or config.random_config_file
        self.__config = u_file.read_propertier(config_file)
        print(self.__config)
        ## 赋值
        self.__keys = u_file.read_csv_to_arr(keys_file)
        self.__start, self.__end = eval(self.__config.get('period'))
        ## 操作对象
        self.__account_num = eval(self.__config.get('account_num'))
        self.__op_pools = eval(self.__config.get('op_pools'))
        self.__op_weights = eval(self.__config.get('op_weights'))
        ## 执行间隔
        self.__interval = int(self.__config.get('interval'))
        self.__days = int(self.__config.get('days'))
        pass

    def run(self):
        self.__start_ts = int(time.time())
        self.__log = f'{config.op_log_pix}-{self.__start_ts}.log'
        self.__status = 1
        print(self.info)
        ## 写入开始日志
        self.log(f'task:{self.__id} start ====>>\n')
        ## 开启新线程准备执行，具体逻辑在线程中操作
        self.__main_t = u_thread.MyThread(target=self.__action)
        self.__main_t.start()
        # self.__main_t.join()
        # self.__main_t.print_err()
        ## 添加进任务管理池
        self.add_task(self)

    ## 输出任务信息
    @property
    def info(self) -> str:
        info = f'id:{self.id}, status:{self.status}\n'
        info += f'start_time: {self.start_time}\n'
        if self.__main_t:
            info += f'{self.__main_t.info}'
        return info

    def __action(self):
        ## 确定执行天数
        days = 0
        print(f'action, {self.id}, day:{days}, total:{self.__days}')
        ## 大周期, 以执行天为单位
        while days < self.__days:
            ## 确定执行周期
            ## 写入开始日志
            self.log(f'task:{self.__id} day {days+1} start ====>>\n', 'a')
            ## 小周期, 每个执行天按执行间隔执行
            index = 1
            while True:
                ## 当前时间已过结束时间，当日任务结束
                ts_end = u_time.calculate_ts(self.__end)
                print(f'ts_end:{ts_end}')
                if ts_end <= 0:
                    break
                ## 确定执行间隔
                ## 计算还有多久到达执行时间点
                ts_start = u_time.calculate_ts(self.__start)
                ### 最后1分钟避免时间冲突不执行任务,所有从[1, 3540]之间选择
                interval = self.__interval - 60
                
                print(f'ts_start:{ts_start}, interval:{interval}')
                ## 如果起始时间已过，计算并等待下一个执行时间点
                if ts_start <= 0:
                    ## 超过的时间 / 时间间隔 = 已过几个执行周期
                    ts = -1 * ts_start
                    ## 例如 超过100秒，时间周期60 下一个时间到达 = 60 - (100 % 60) = 20
                    ts_start = self.__interval - ts % self.__interval
                    
                    print(f'new ts_start:{ts_start}')
                    pass
                
                print(f'task:{self.__id}: {index} time after {ts_start} secs ....\n')
                self.log(f'task:{self.__id}: {index} time after {ts_start} secs ....\n','a')
                ## 睡眠等待
                u_time.sleep(ts_start, 10)
                ## 获取本执行周期的随机账号列表
                account_num = u_random.r_int(self.__account_num[0], self.__account_num[1])
                keys = u_random.r_list(self.__keys, u_random.r_int(1,account_num))
                ## 每个被选取到的账号开启新线程进入执行逻辑
                u_thread.batch_execute(keys, self.__do, interval)
                index += 1
                ## 所有账户执行完成后，判断本日是否已完成所有执行周期
                is_over = False
                if is_over:
                    break
                pass
            ## 当然执行任务结束，执行日期增加1天
            days += 1
            u_thread.update_thread_info({'days': days})
            ## 写入结束日志
            self.log(f'task:{self.__id} day {days} end <====\n', 'a')
            ## 等待到第二天凌晨开启下一轮
            next_day_ts = u_time.calculate_ts(hour=24)
            time.sleep(next_day_ts)
        ## 任务执行结束
        self.remove_task(self.id)
        ## 写入结束日志
        self.log(f'task:{self.__id} over <====\n')
        pass

    def __do(self, key, interval):
        ## 随机选取执行时间点
        ### 最后1分钟避免时间冲突不执行任务,所有从[1, 3540]之间选择
        ts = interval
        if interval > 0:
            ts = u_random.r_int(0, interval)
        
        self.log(f'task:{self.__id}: key:{key[0:6]}... action after {ts} secs ....\n', 'a')
        ## 睡眠等待
        if ts and ts > 0:
            time.sleep(ts)
        ## 随机选择待执行的操作
        # op_num = u_random.r_int(1, len(self.__op_pools))
        ## 每个执行周期随机操作1到5次(暂时只操作1次)
        op_num = u_random.r_int(1,1)
        op_cmds = u_random.r_list_by_weight(self.__op_pools, op_num, self.__op_weights)
        ## 开始执行
        account = Account.from_key(key)
        ## 遍历执行指令, 写日志
        for cmd in op_cmds:
            print(f'操作指令{cmd}')
            ## 构建参数
            amount = float(self.__config.get('amount'))
            target_addr = str(self.__config.get('target_addr'))
            op_cmd = op.cmd_instance(cmd, account, target_addr=target_addr, amount=amount)
            rs = op_cmd.execute()
            self.log(f'account:{account.address}, cmd:{cmd}, {rs}\n', 'a')
        pass
    
    def log(self, s, m='w'):
        print(s)
        u_file.write_op_log(self.__log, m, s)
    
    @classmethod
    @u_thread.sync_operate()
    def id_increment(cls):
        cls.__id += 1
        return cls.__id
    
    @classmethod
    def add_task(cls, task):
        cls.tasks[task.id] = task

    @classmethod
    def remove_task(cls, task_id):
        del cls.tasks[task_id]
    
    @classmethod
    def get_task(cls, id):
        return cls.tasks[id]
    
    @classmethod
    def get_all_task(cls):
        return cls.tasks
    
    @property
    def id(self):
        return self.__id
    
    @property
    def log_path(self):
        return self.__log
    
    @property
    def status(self):
        if self.__status == 0:
            return 'init'
        elif self.__status == 1:
            return 'running'
        
    @property
    def start_time(self):
        return u_time.format_ts(self.__start_ts)
    pass
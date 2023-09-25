import threading
import traceback

## 同步锁
lock = threading.Lock()

## 自定义线程，增加异常捕获
class MyThread(threading.Thread):
    exception = None
    def run(self) -> None:
        try:
            super().run()
        except Exception as e:
            self.exception = e
            print(traceback.format_exc())

    def print_err(self):
        if self.exception is not None:
            print(traceback.format_exc())
            # self.exception.with_traceback()
        pass
    @property
    def info(self):
        return self._info
    
    @info.setter
    def info(self, info) :
        self._info= info

## 线程池大小
thread_pool_size = 100
def batch_execute(infos:list, func, *arg):
    index = 0
    exceptions = []
    while True:
        t_list = []
        ## 避免同时执行过多，按线程池大小分批执行
        for info in infos[thread_pool_size*index: thread_pool_size*(index+1)]:
            print(f'开始操作，key:{info}')
            args = (info, *arg)
            t = MyThread(target=func, args=args)
            t_list.append(t)
            t.start()
        
        for t in t_list:
            t.join()
            if t.exception:
                exceptions.append(t.exception)
        index += 1
        if index * thread_pool_size > len(infos):
            break
    pass

## 更新线程信息
def update_thread_info(info):
    current_thread: MyThread = threading.current_thread()
    current_thread.info = info

## 同步操作
def sync_operate():
    def decorator(func):
        def wrapper(*args, **kw):
            lock.acquire()
            rs = func(*args, **kw)
            lock.release()
            return rs
        return wrapper
    return decorator
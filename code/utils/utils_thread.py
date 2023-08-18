import threading

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


## 线程池大小
thread_pool_size = 100
def batch_execute(infos:list, func, *arg):
    index = 0
    exceptions = []
    while True:
        t_list = []
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
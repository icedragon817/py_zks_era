## 时间工具类
import time
### 计算到当日整点的秒数，不传计算到下一个整点
def calculate_ts(hour=None):
    now = time.localtime()
    ## 未传递时间，默认下一个小时
    if hour == None:
        hour = now.tm_hour + 1
    # if now.tm_hour > hour:
    #     return 0
    h = hour - now.tm_hour - 1
    m = (60 - now.tm_min) - 1 #距离开始还剩多少分钟
    s = (60 - now.tm_sec) #距离开始还剩多少秒
    return h * 3600 + m * 60 + s

### 格式化输出时间戳
def format_ts(ts):
    timeArray = time.localtime(ts)
    return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

def ts():
    return int(time.time())
### 睡眠，为保证活跃，每隔一段时间输出一次
def sleep(ts, interval):
    print(f'About to sleep for {ts} seconds')
    t, ext = int(ts / 10), ts % 10
    if t > 0:
        for i in range(t):
            time.sleep(interval)
            print(f'sleep {(i+1)*interval} sec')
            pass
        pass
    if ext > 0:
        time.sleep(ext)
    pass
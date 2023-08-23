## 时间工具类
import time
### 计算到当日整点的秒数，不传计算到下一个整点
def calculate_ts(hour=None):
    now = time.localtime()
    ## 未传递时间，默认下一个小时
    if hour == None:
        hour = now.tm_hour + 1
    if now.tm_hour > hour:
        return 0
    h = hour - now.tm_hour - 1
    m = (60 - now.tm_min) - 1 #距离开始还剩多少分钟
    s = (60 - now.tm_sec) #距离开始还剩多少秒
    return h * 3600 + m * 60 + s

### 格式化输出时间戳
def format_ts(ts):
    timeArray = time.localtime(ts)
    return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
## 随机工具库
import random

## 从list中随机n个数据组成新的list返回
def r_list(source: list, n: int) -> list:
    if len(source) <= n:
        return source.copy()
    else:
        return random.sample(source, n)
    
## 随机数字
def r_int(min, max) -> int:
    if min >= max:
        return min
    return random.randint(min, max)
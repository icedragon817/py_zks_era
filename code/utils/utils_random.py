## 随机工具库
import random

## 从list中随机n个数据组成新的list返回
def r_list(source: list, n: int) -> list:
    if len(source) <= n:
        return source.copy()
    else:
        return random.sample(source, n)
    
## 从list中随机n个数据组成新的list返回, 通过权重
def r_list_by_weight(source: list, n: int, weight: list =None) -> list:
    source_len = len(source)
    if weight is None or len(weight) < source_len :
        weight = [1,1,1,1]
        pass
    ## 根据权重组成新的随机池
    r_pool = []
    for i in range(source_len):
        source_w = weight[i]
        source_v = source[i]
        if source_w > 0:
            for _ in range(source_w):
                r_pool.append(source_v)
    print(r_pool)
    ## 从池子中随机取数据，组成新list
    rs = []
    for i in range(n):
        rs.append(random.choice(r_pool))
        pass

    return rs
    
## 随机数字
def r_int(min, max) -> int:
    if min >= max:
        return min
    return random.randint(min, max)
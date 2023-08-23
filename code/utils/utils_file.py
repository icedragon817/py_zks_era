from utils.utils_thread import sync_operate

## 读取csv转换成list
def read_csv_to_arr(path, cls=None) -> list:
    rs = []
    read_csv(path, csv_to_list, rs, cls)
    return rs

## 读取csv转换成set
def read_csv_to_set(path, cls=None) -> list:
    rs = set()
    read_csv(path, csv_to_set, rs, cls)
    return rs

## 读取csv
def read_csv(path, func, *params):
     ## 读取文件
    try:
        with open(path, encoding='utf-8') as f:
            while True:
                content = f.readline().strip()
                func(*params, content)
                if len(content) == 0:
                    break
    except FileExistsError as e :
        print(e)
    except FileNotFoundError as e:
        print(e)
    pass

## 写操作日志(需上锁操作)
@sync_operate()
def write_op_log(path, mode, s):
    try:
        ## open 文件时必须指定需要的操作，不知道默认读操作
        ## mode w 表示可以写入 
        ## mode a 表示追加内容
        # 文件不存在，会创建文件，文件存在会重新写入
        with open(path, mode=mode, encoding='utf-8') as f:
            # 写入内容
            f.write(s)
    except FileExistsError as e :
        print(e)

# csv数据转list
def csv_to_list(rs: list, cls, context):
    obj = toCls(context, cls)
    if obj:
        rs.append(toCls(context, cls))

# csv数据转set
def csv_to_set(rs: set, cls, context):
    obj = toCls(context, cls)
    if obj:
        rs.add(toCls(context, cls))

## str转对象
def toCls(s: str, cls):
    if(len(s.strip()) == 0):
        return
    if cls == None:
        return s
    ls = s.split(',')
    if len(ls) == 0:
        return
    return cls(*ls)

## 读配置文件
def read_propertier(path) -> dict:
    rs = {}
    try:
        with open(path, encoding='utf-8') as f:
            while True:
                content = f.readline()
                if len(content) == 0:
                    break
                else:
                    v = content.split('=')
                    if len(v) == 2:
                        rs[v[0].strip()] = v[1].strip()
    except FileExistsError as e :
        print(e)
    except FileNotFoundError as e:
        print(e)
    
    return rs
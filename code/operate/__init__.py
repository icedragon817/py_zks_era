import private_key as pk
import help_info as hi

use_cnt = {}
## 注册
def register(op, info=None):
    if use_cnt.get(op) == None:
        use_cnt[op] = 0
        hi.HelpInfo.register(op, info)
    def decorator(func):
        def wrapper(*args, **kw):
            use_cnt[op] += 1
            return func(*args, **kw)
        return wrapper
    return decorator

## 退出操作
def exit():
    info = '你即将退出脚本，本次操作：\n' + '...' * 3 + '\n'
    op_info = ''
    for k, v in use_cnt.items():
        if v > 0:
            op_info += f'cmd: {k}, cnt: {v} 次\n'
    if len(op_info) == 0 :
        op_info += '你没有进行任何操作'
    
    info += op_info
    return info

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

from operate import op_account as op_acc, op_contract,op_plus, op_test
### 各类基础操作 通过传递的参数区分
## 数字指令为基础操作
def base_operate(cmd, account, *params, **key) -> bool:
    if not cmd:
        return
    print(f'recive cmd: {cmd}')
    if cmd == '-1' :
        address = key.get('address')
        if address is None:
            address = account.address
        return op_acc.check_balance(address, key.get('chain'))
    elif cmd == '-2':
        target_addr, amount = params[0], params[1]
        return op_acc.transfer_eth(account, target_addr, amount)
    elif cmd == '-3':
        amount = params[0]
        rs = op_acc.deposit(account, amount)
        print(rs)
        return rs
    elif cmd == '-4':
        amount = params[0]
        rs = op_acc.withdraw(account, amount)
        print(rs)
        return rs
    elif cmd == '-5':
        rs = op_contract.deploy(account, key.get('path'))
        print(rs)
        return rs
    elif cmd == '0':
        # bridge_addresses = acc.sdk.zksync.zks_get_bridge_contracts()
        # print(bridge_addresses)
        pass

### 各类高级操作 通过传递的参数区分
## 数字指令为基础操作
def senior_operate(cmd, *params) -> bool:
    if cmd == '-com' :
        return op_plus.combine(params[0], params[1])
    elif cmd == '-batch':
        return op_plus.batch(params[0], params[1])
    elif cmd == '-random':
        return op_plus.op_random(params[0], params[1])
    elif cmd == 'test':
        ## test code
        return op_test.do_test()
    else:
        pass

## 指令对象
class Op_cmd():
    _args = ()

    def __init__(self, account, cmd, *args, **keys) -> None:
        self._cmd = cmd
        self._args = args
        self._keys = keys
        self._account = account
    
    @property
    def cmd(self):
        return self._cmd
    @property
    def args(self) -> tuple:
        return self._args
    
    def execute(self):
        return base_operate(self._cmd, self._account, *self.args, **self._keys)

## 根据指令构造指令对象
def cmd_instance(cmd, account, **key) -> Op_cmd:
    args = (cmd,)
    if cmd == '-1':
        pass
    elif cmd == '-2':
        args = (key.get('target_addr'), key.get('amount'))
    elif cmd == '-3':
        args = (key.get('amount'),)
    elif cmd == '-4':
        args = (key.get('amount'),)
    
    return Op_cmd(account, cmd, *args, **key)
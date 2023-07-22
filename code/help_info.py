class HelpInfo():

    _info = {}
    ## 打印help info
    @classmethod
    def print(cls) -> str:
        info = '\n'
        for k, v in cls._info.items():
            info += '\t' + k + ' : ' + v + '\n'
        return info
        

    ## 注册执行方法
    @classmethod
    def register(cls, cmd, info):
        cls._info[cmd] = info
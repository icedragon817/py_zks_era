# zks era 撸毛脚本

## 使用方式
### 下载

通过`github`下载

### 配置环境
* 打开powershell
* 切换虚拟环境
* 运行demo.py
## 准备 Prepare
### python 安装
版本：**3.10.11** [downlown](https://www.python.org/downloads/release/python-31011/)

**踩坑** 
- 3.11版本无法安装pysha3包
- 3.6版本直接搜索不到包

**升级pip 23.2**
```bash
python -m pip install --upgrade pip
```

**安装依赖包**

`pip install zksync2`

**安装过程中出现问题**
```
Building wheels for collected packages: pysha3
  Building wheel for pysha3 (pyproject.toml) ... error
  error: subprocess-exited-with-error

  │ exit code: 1
  ╰─> [9 lines of output]
      running bdist_wheel
      running build
      running build_py
      creating build
      creating build\lib.win-amd64-cpython-310
      copying sha3.py -> build\lib.win-amd64-cpython-310
      running build_ext
      building '_pysha3' extension
      error: Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/
      [end of output]

  note: This error originates from a subprocess, and is likely not a problem with pip.
  ERROR: Failed building wheel for pysha3
Failed to build pysha3
ERROR: Could not build wheels for pysha3, which is required to install pyproject.toml-based projects
```

原因：未安装C++编译器，无法编译

解决方案：

下载 [`Microsoft C++ Build Tools`](https://visualstudio.microsoft.com/visual-cpp-build-tools/) 并安装。

安装过程中切换`单个组件`，勾选`Window 10 SDK`

安装好之后启动，然后重新运行 `pip` 安装命令。

### 创建Metamask钱包

#### 安装Chrome插件
[下载地址](https://chrome.google.com/webstore/detail/metamask/nkbihfbeogaeaoehlefnkodbefgpgknn)

备好 **密码** 和 **助记词**

查看 **账户地址** 和 **private key**

### 了解区块链

#### 概念

**网络**
**钱包**

## 开发 Develop

### 程序入口

demo.py，死循环执行操作指令，直到收到`exit`指令

```python
if __name__ == "__main__":
    while True:
        result = False
        cmd = input('请输入指令, 帮助"help"，退出"exit" >>> ').strip()
        if cmd == 'help' or cmd == "-h":
            print(hi.HelpInfo.print())
        else:
            result = operate(cmd)
        
        if result: 
            print(op.exit())
            confirm = input("是否确定退出(Y/N) >>> ").lower()
            if confirm == 'y' or confirm == 'yes' :
                break
```

### 操作路由

通过操作指令判断执行方法：

- help: 指引，提示操作指令
- exit: 退出脚本
- -1：  查询余额，提供账户地址可以查询其他账户余额
- -2:   生成签名
- ... 待完善

### Sdk接入

#### 账户相关操作

账户相关操作：`operate/op_account.py`

**查询余额** : `sdk.zksync.get_balance`

... TODO ...
#### 交易相关操作

... TODO ...
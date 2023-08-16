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

**网络**：可以提供一系列合约应用。也叫链路(`chain`)。

目前使用： [`zkSync Era Mainnet`](https://explorer.zksync.io)

**钱包**：作为区块链中存储数字货币的账户。

**合约Dapp**：部署在网络上的应用，遵从网络的协议，提供交互服务。

关于合约的编写及部署：参考文档 [Ether智能合约](Ether 智能合约.md)

**交互行为**

- 单链路交互
    - 转账：把一个钱包上的数字货币转到另一个钱包上。
    - 合约部署：在网络上部署合约
    - 合约交换：通过合约把不同数字货币转换成其他数字货币，例如：ETH -> USDT [Dapp](https://syncswap.xyz/)
    - 合约交互：存钱 借钱  还钱 取钱。通过第三方合约实现类似金融服务。[`Dapp`](https://app.eralend.com/)
- 跨链路交互
    - 提币：把一个链路的的数字货币转移到另一个链路上。

**交易**：本质上链路上的所有交互行为都是一笔或多笔交易。每一笔交易需要一定的数字货币作为手续费。

- **转账**: 在同一网络上将数字货币转移到另一个账户的交易行为。

- **提币\充币**: 本质是两笔交易，先在A网络将个人账户的数字货币转账官方账户，再由B网络的官方账户转账到个人账户。


## 开发 Develop

### 了解 Web3

#### Web3 对象
Web3对象用于与区块链交互的对象。包`web3`-`main.py`, 创建方式：
```python
from web3 import Web3

## rpc地址可以在链路信息中获取到
rpc = 'https://rpc.ankr.com/eth_goerli'
w3 = Web3(Web3.HTTPProvider(rpc))
```

`Web3`类属性及方法: 
- `provider`
- `normalize_values`
- `middleware_onion`: 中间件集合
- `client_version`
- `ens`
- `is_connected()`

##### zksyc2 对象
`zksyc2`是`era`网络封装的sdk，把Web3对象进行了一定的封装，添加了模块`zksync`，使用方式用提供方式创建：
```python
from zksync2.module.module_builder import ZkSyncBuilder

sdk = ZkSyncBuilder.build(zk_dev_url)
```

`zksync`模块提供的功能可以去`from zksync2.module.zksync_module import ZkSync`模块中去查看。

#### Eth 对象
`Eth`类位于`web3.eth`包，具体属性和方法：
- `accounts`
- `hashrate`
- `block_number`
- `chain_id`: 链路ID
- `coinbase`
- `gas_price`: 基础燃料价格
- `max_priority_fee`
- `mining`
- `syncing`
- `fee_history()`
- `call()`
- `estimate_gas()`
- `get_transaction()`
- `get_raw_transaction()`
- `get_raw_transaction_by_block()`
- `send_transaction()`
- `send_raw_transaction()`: 发送原始交易
- `get_block()`: 从RPC上获取某个区块的信息
- `get_balance()`: 查看余额
- `get_code()`
- `get_logs()`
- `get_transaction_count()`: 取得交易次数
- `get_transaction_receipt()`: 获取交易收据信息
- `wait_for_transaction_receipt()`: 等待获取交易收据，参数: `transaction_hash: 交易hash`、`timeout: 超时时间s`、`poll_latency: 轮询间隔`
- `get_proof_munger()`
- `replace_transaction()`
- `modify_transaction()`
- `contract()`: 生成并返回合约对象，[Contract](#Contract ETH合约对象)

##### ZkSync 对象

`ZkSync`是一个继承`Eth`的类，包`zksync2.module.zksync_module`

`ZkSync`类拓展属性及方法: 
- `zks_estimate_fee()`: [aaa](#EthereumProvider eth供应者)
- `zks_main_contract()`
- `zks_get_confirmed_tokens()`
- `zks_get_token_price()`
- `zks_l1_chain_id()`
- `zks_get_all_account_balances()`
- `zks_get_bridge_contracts()`: 获取桥接合同信息, RPC point `zks_getBridgeContracts`
- `zks_get_l2_to_l1_msg_proof()`
- `zks_get_log_proof()`
- `zks_get_testnet_paymaster_address()`
- `eth_estimate_gas()`: `zks_era`链上的燃料数量,总费用`eth_estimate_gas` * `gas_price`
- `get_l2_transaction_from_priority_op()`
- `get_priority_op_response()`
- `wait_for_transaction_receipt()`: 等待获取交易收据, 与父类一样
- `wait_finalized()`: 等待最终回执数据 (比上一个方法多一个等待退出的条件)

静态方法: 
- `get_l2_hash_from_priority_op()`: 通过`l1转账交易凭证`和`合约对象`获取`L2的存款交易hash`

#### EthereumProvider eth供应者

该类为zksync2库封装，位于包`zksync2.provider.eth_provider`，提供`era`链路和其他链路交换`Eth`的方法。

类中定义：L1代表`era`链路，L2代表其他链路。

构造参数：
- `zksync_web3`: 经过`zksyc2`封装的`Web3`对象。[Zksyc2](#zksyc2 对象)
- `eth_web3`: L1链路`Web3`对象。[Web3](#web3-对象)
- `l1_account`: 账户对象

主要属性和方法：
- `main_contract`: 链路的交易合约。[ZkSyncContract](#ZkSyncContract)对象
- `l1_bridge`: L1桥接对象。[L1Bridge](#L1Bridge)
- `address`: 账户地址
- `get_l1_balance()`: 查询L1账户余额。
- `l2_token_address()`
- `get_base_cost()`
- `approve_erc20()`
- `deposit()`: 从其他链路往`era`链路充币，调用`L1Bridge`的`deposit`方法
- `request_execute()`
- `finalize_withdrawal()`
- `is_withdrawal_finalized()`


#### 其他对象
##### Contract ETH合约对象
Eth的合约对象，一般通过类方法`factory`构造

构造参数：
- `address`: 合约地址

属性:
- `address`: 合约地址
- `functions`: 合约方法，通常配置在abi文件中
- `caller`
- `events`
- `fallback`
- `receive`
##### ZkSyncContract 


`zks era`链上的合约对象，位于包`zksync2.manage_contracts.zksync_contract`

属性及方法：
- `address`: 合约地址
- `accept_governor()`
- `cancel_upgrade_proposal()`
- `commit_blocks()`
- `execute_blocks()`
- `execute_upgrade()`
- `facet_address()`
- `facet_addresses()`

##### L1Bridge

`zks era`链上的桥接对象，位于包`zksync2.manage_contracts.l1_bridge`

构造参数:
- `contract_address`: 桥接合约地址
- `web3`: L1链路的web3对象
- `eth_account`: eth账户对象
- `abi`: 可选。ABI代表应用程序二进制接口，是描述约定变量和函数、名称和类型的json。默认会读取包`zksync2.manage_contracts.contract_abi`下的`IL1Bridge.json`的`key=abi`的值

主要属性和方法:
- `address`: 桥接合约地址
- `deposit()`: 通过桥接合约充值数字货币，返回RPC 节点`eth_getTransactionReceipt`数据
- `finalize_withdrawal()`: 完成最终提款操作

##### TxBase 交易参数封装对象
提供交易操作调用参数的封装。位于包`zksync2.transaction.transaction_builders`。

属性及方法: 
- `tx`: 封装好的所有参数
- `tx712()`: 将参数封装成`EIP712`格式并返回。

子类:
- `TxFunctionCall`: 函数调用
- `TxCreateContract`: 创建合约
- `TxCreateAccount`: 创建账户
- `TxWithdraw`: 提款
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
- -2：  转账
- -3:   往`era`网络充值ETH
- -4:   从`era`网络提取ETH
- ... 待完善

### Sdk接入

#### 账户相关操作

<div id='test'>
账户相关操作：`operate/op_account.py`

**查询余额** : `sdk.zksync.get_balance`

... TODO ...
#### 交易相关操作

... TODO ...
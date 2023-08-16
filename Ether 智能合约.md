# Ether 智能合约

## 概述

所谓智能合约，就是一种运行在区块链上的程序。



以太坊提供了一个EVM（Ethereum Virtual Machine）虚拟机来执行智能合约的字节码，并且，和普通程序相比，为了消除程序运行的不确定性，智能合约有很多限制，例如，不支持浮点运算（因为浮点数有不同的表示方法，不同架构的CPU运行的浮点计算精度都不同），不支持随机数，不支持从外部读取输入等等。

我们需要一种高级语言来编写智能合约，然后编译成EVM的字节码。最常用的开发智能合约的语言是以太坊专门为其定制的[Solidity](https://docs.soliditylang.org/)语言。

一个智能合约被编译后就是一段EVM字节码，将它部署在以太坊的区块链时，会根据部署者的地址和该地址的nonce分配一个合约地址，合约地址和账户地址的格式是没有区别的，但合约地址没有私钥，也就没有人能直接操作该地址的合约数据。要调用合约，唯一的方法是调用合约的公共函数。

这也是合约的一个限制：合约不能主动执行，它只能被外部账户发起调用。如果一个合约要定期执行，那只能由线下服务器定期发起合约调用。

此外，合约作为地址，可以接收Ether，也可以发送Ether。合约内部也可以存储数据。合约的数据存储在合约地址关联的存储上，这就使得合约具有了状态，可以实现比较复杂的逻辑，包括存款、取款等。

合约在执行的过程中，可以调用其他已部署的合约，前提是知道其他合约的地址和函数签名，这就大大扩展了合约的功能。



## 编写合约代码

### 准备工作

#### Vscode插件

#### Nodejs安装



### Solidity 语法

[官方文档](https://docs.soliditylang.org/en/latest/introduction-to-smart-contracts.html)

#### Demo

```solidity
// SPDX-License-Identifier: GPL-3.0

pragma solidity =0.8.7;

contract Vote {

    event Voted(address indexed voter, uint8 proposal);

    mapping(address => bool) public voted;

    uint256 public endTime;

    uint256 public proposalA;
    uint256 public proposalB;
    uint256 public proposalC;

    constructor(uint256 _endTime) {
        endTime = _endTime;
    }

    function vote(uint8 _proposal) public {
        require(block.timestamp < endTime, "Vote expired.");
        require(_proposal >= 1 && _proposal <= 3, "Invalid proposal.");
        require(!voted[msg.sender], "Cannot vote again.");
        voted[msg.sender] = true;
        if (_proposal == 1) {
            proposalA ++;
        }
        else if (_proposal == 2) {
            proposalB ++;
        }
        else if (_proposal == 3) {
            proposalC ++;
        }
        emit Voted(msg.sender, _proposal);
    }

    function votes() public view returns (uint256) {
        return proposalA + proposalB + proposalC;
    }
}
```



#### 代码结构

- 声明版权（可选）；
- 声明编译器版本；
- 以contract关键字编写一个合约；
- 可以包含若干成员变量；
- 可以在构造函数中对成员变量初始化（可选）；
- 可以编写只读方法；
- 可以编写写入方法；
- 可以声明Event并在写入方法中触发。

#### 数据类型

Solidity支持整型（细分为uint256、uint128、uint8等）、bytes32类型、映射类型（相当于Java的Map）、布尔型（true或false）和特殊的`address`类型表示一个以太坊地址。

所有的成员变量都默认初始化为`0`或`false`（针对bool）或空（针对mapping）。

#### 逻辑语法

##### 基础语法

- `contract` 关键字定义合约
- `constructor` 构造方法
- `function` 定义函数
  - `public`/`private`表示函数是否允许外部调用
  - `view`：表示是否只读函数，只读函数不改变合约内部属性，调用不消耗交易费。
  - `return`：返回值属性

##### 事件

合约可以定义事件（Event），我们在Vote合约中定义了一个`Voted`事件：

```solidity
contract Vote {
    // Voted事件，有两个相关值:
    event Voted(address indexed voter, uint8 proposal);

    ...
}
```

只定义事件还不够，触发事件必须在合约的写函数中通过`emit`关键字实现。当调用`vote()`写方法时，会触发`Voted`事件：

```solidity
contract Vote {
    ...

    function vote(uint8 _proposal) public {
        ...
        emit Voted(msg.sender, _proposal);
    }

    ...
}
```

事件可用来通知外部感兴趣的第三方，他们可以在区块链上监听产生的事件，从而确认合约某些状态发生了改变。

##### 验证

`require()`可以断言一个条件，如果断言失败，将抛出错误并中断执行。

常用的检查包括几类：

参数检查：

```solidity
// 参数必须为1,2,3:
require(_proposal >= 1 && _proposal <= 3, "Invalid proposal.");
```

条件检查：

```solidity
// 当前区块时间必须小于设定的结束时间:
require(block.timestamp < endTime, "Vote expired.");
```

调用方检查：

```solidity
// msg.sender表示调用方地址:
require(!voted[msg.sender], "Cannot vote again.");
```

以太坊合约具备类似数据库事务的特点，如果中途执行失败，则整个合约的状态保持不变，不存在修改某个成员变量后，后续断言失败导致部分修改生效的问题：

```solidity
function increment() {
    // 假设a,b均为成员变量:
    a++;
    emit AChanged(a);
    // 如果下面的验证失败，a不会被更新，也没有AChanged事件发生:
    require(b < 10, 'b >= 10');
    b++;
}
```

即合约如果执行失败，其状态不会发生任何变化，也不会有任何事件发生，仅仅是调用方白白消耗了一定的Gas。

#### 合约执行流程

当一个合约编写完成并成功编译后，我们就可以把它部署到以太坊上。合约部署后将自动获得一个地址，通过该地址即可访问合约。

把`contract Vote {...}`看作一个类，部署就相当于一个实例化。如果部署两次，将得到两个不同的地址，相当于实例化两次，两个部署后的合约对应的成员变量是完全独立的，互不影响。

构造函数在部署合约时就会立刻执行，且仅执行一次。合约部署后就无法调用构造函数。

任何外部账户都可以发起对合约的函数调用。如果调用只读方法，因为不改变合约状态，所以任何时刻都可以调用，且不需要签名，也不需要消耗Gas。但如果调用写入方法，就需要签名提交一个交易，并消耗一定的Gas。

在一个交易中，只能调用一个合约的一个写入方法。无需考虑并发和同步的问题，因为以太坊交易的写入是严格串行的。

## 部署



## 访问


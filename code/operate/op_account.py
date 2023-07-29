import operate as op
import zk_account as zk_acc
import utils.utils_chain as uc

from zksync2.core.types import EthBlockParams
from zksync2.signer.eth_signer import PrivateKeyEthSigner
from zksync2.core.types import ZkBlockParams
from zksync2.transaction.transaction_builders import TxFunctionCall, TxWithdraw
from zksync2.provider.eth_provider import EthereumProvider
from zksync2.manage_contracts.zksync_contract import ZkSyncContract
from zksync2.core.types import Token

from eth_typing import HexStr, HexAddress
from eth_account.signers.local import LocalAccount
from eth_utils import to_checksum_address

from web3 import Web3
from web3.middleware import geth_poa_middleware

## 查询余额操作
op.register('-1', '查询余额， 参数1: 账户地址（默认自身）')
@op.register('-1')
def check_balance(acc=zk_acc.my_account.address):
    '''
    查询余额
    参数：账户地址（默认自己地址）
    '''
    sdk = zk_acc.sdk
    acc = input('请输入账户地址，默认当前账户>>>')
    acc = acc or zk_acc.my_account.address
    zk_balance = sdk.zksync.get_balance(acc, EthBlockParams.LATEST.value)
    print(f"Balance: {zk_balance}")

## 转账ETH
op.register('-2', '转账ETH 参数1: 地址, 参数2: 数量')
@op.register('-2')
def transfer_eth(
    address: HexAddress,
    amount: float
) -> bytes:
    sdk: Web3 = zk_acc.sdk
    account: LocalAccount = zk_acc.my_account
    # 获取链路 ID
    chain_id = sdk.zksync.chain_id

    # 生成签名工具
    signer = PrivateKeyEthSigner(account, chain_id)

    # Get nonce of ETH address on zkSync network
    nonce = sdk.zksync.get_transaction_count(
        account.address, ZkBlockParams.COMMITTED.value
    )

    # 交易费用 单价
    gas_price = sdk.zksync.gas_price

    # 转账调用参数
    tx_func_call = TxFunctionCall(
        chain_id=chain_id,
        nonce=nonce,
        from_=account.address,
        to=to_checksum_address(address),
        value=sdk.to_wei(amount, "ether"),
        data=HexStr("0x"),
        gas_limit=0,  # UNKNOWN AT THIS STATE
        gas_price=gas_price,
        max_priority_fee_per_gas=100_000_000,
    )

    # 交易费用预估
    estimate_gas = sdk.zksync.eth_estimate_gas(tx_func_call.tx)
    print(f"Fee for transaction is: {estimate_gas * gas_price}")

    # 使用 EIP-712 格式
    tx_712 = tx_func_call.tx712(estimate_gas)

    # 生成签名信息
    signed_message = signer.sign_typed_data(tx_712.to_eip712_struct())

    # 加密签名信息
    msg = tx_712.encode(signed_message)

    # 发送ETH
    tx_hash = sdk.zksync.send_raw_transaction(msg)
    print(f"发起转账成功, 交易 hash : {tx_hash.hex()}")

    # 等待返回
    tx_receipt = sdk.zksync.wait_for_transaction_receipt(
        tx_hash, timeout=240, poll_latency=0.5
    )
    print(f"交易状态: {tx_receipt['status']}")

    # Return the transaction hash of the transfer
    return tx_hash

## 其他链充币到era链 L1 -> L2
op.register('-3', 'eth充币 L1 -> L2 参数1: L1网络, 参数2: 数量')
@op.register('-3')
def deposit(amount, chain:str ='goerli') -> tuple[HexStr, HexStr]:
    
    ## 获取目标链provider
    sdk: Web3 = zk_acc.sdk
    account = zk_acc.my_account
    chain_rpc = uc.get_chain(chain)
    eth_web3 = Web3(Web3.HTTPProvider(chain_rpc))
    eth_provider = EthereumProvider(sdk, eth_web3, account)

    # L1网络的提款操作
    print("Executing deposit transaction on L1 network")
    l1_tx_receipt = eth_provider.deposit(token=Token.create_eth(),
                                         amount=Web3.to_wei(amount, 'ether'),
                                         gas_price=eth_web3.eth.gas_price)

    # 判断状态
    if not l1_tx_receipt["status"]:
        raise RuntimeError("Deposit transaction on L1 network failed")

    # 在 L1 网络上获取 ZkSync 合约
    zksync_contract = ZkSyncContract(sdk.zksync.main_contract_address, eth_web3, account)

    # 获取 L2 网络上存款交易的哈希值
    l2_hash = sdk.zksync.get_l2_hash_from_priority_op(l1_tx_receipt, zksync_contract)

    # 等待L2网络充值交易完成（5-7分钟）
    print("Waiting for deposit transaction on L2 network to be finalized (5-7 minutes)")
    l2_tx_receipt = sdk.zksync.wait_for_transaction_receipt(transaction_hash=l2_hash,
                                                                        timeout=360,
                                                                        poll_latency=10)

    # 从 L1 和 L2 网络返回存款交易哈希
    return l1_tx_receipt['transactionHash'].hex(), l2_tx_receipt['transactionHash'].hex()

## era链提币到其他链 L2 -> L1
op.register('-4', 'eth提币 L1 -> L2 参数1: L1网络, 参数2: 数量')
@op.register('-4')
def withdraw(amount, chain:str ='goerli') -> tuple[HexStr, HexStr]:
    
    ## 获取目标链provider
    sdk: Web3 = zk_acc.sdk
    account = zk_acc.my_account
    chain_rpc = uc.get_chain(chain)
    eth_web3 = Web3(Web3.HTTPProvider(chain_rpc))
    eth_web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    eth_provider = EthereumProvider(sdk, eth_web3, account)

    # 创建提款交易
    withdraw = TxWithdraw(web3=sdk,
                              token=Token.create_eth(),
                              amount=Web3.to_wei(amount, 'ether'),
                              gas_limit=0,  # unknown
                              account=account)
    # 估算交易费用(单价)
    estimated_gas = sdk.zksync.eth_estimate_gas(withdraw.tx)

    # 预估燃料费用
    tx = withdraw.estimated_gas(estimated_gas)

    # 签署交易
    signed = account.sign_transaction(tx)

    # 将交易广播到网络
    tx_hash = sdk.zksync.send_raw_transaction(signed.rawTransaction)
    l2_tx_receipt = sdk.zksync.wait_finalized(tx_hash, timeout=240, poll_latency=0.5)
    l1_tx_receipt = eth_provider.finalize_withdrawal(l2_tx_receipt["transactionHash"])

    # 从 L1 和 L2 网络返回存款交易哈希
    return l1_tx_receipt['transactionHash'].hex(), l2_tx_receipt['transactionHash'].hex()


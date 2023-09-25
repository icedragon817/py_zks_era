import config
import utils.utils_file as u_file
from zk_account import env
from solcx import compile_standard, install_solc
# import solcx
import json

from pathlib import Path
from web3 import Web3

from eth_account.signers.local import LocalAccount
from zksync2.manage_contracts.contract_encoder_base import ContractEncoder
from zksync2.core.types import EthBlockParams
from zksync2.signer.eth_signer import PrivateKeyEthSigner
from zksync2.transaction.transaction_builders import TxCreateContract

## era链 合约类
class Zk_contract():
    ## 合约名称
    web3: Web3 = env.sdk
    ## 合约名称
    __name: str = None
    ## 合约地址
    __address: str = None
    ## sol文件路径
    __sol_path: str = None
    ## json文件路径
    __json_path: str = None
    ## 状态 0 初始化 1 已编译 2 已部署
    __status: int = 0
    ## abi
    __bytecode: bytes = None
    __abi = None
    
    ## 构造方法 自定义部署的合约不需要参数
    def __init__(self, address=None, bytecode=None, abi=None) -> None:
        self.__address = address
        self.__bytecode = bytecode
        self.__abi = abi
        pass
    ## 编译
    def compile(self, path: Path, solc_version='0.8.19'):
        self.__sol_path = path
        self.__name = path.name
        sol_str = u_file.read_to_str(path)
        ## 安装编译器
        install_solc(solc_version)
        ## 编译
        params = {
            "language": "Solidity",
            "sources": {self.__name: {"content": sol_str}},
            "settings": {
                "outputSelection": {
                    "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                }
            },
        }
        compiled_sol = compile_standard(params, solc_version=solc_version)
        # compiled_sol = solcx.compile_files(path, output_values=['abi', 'bin', 'metadata'])

        ## 写入编译好的json文件
        json_path = config.contract_complie_path + '\\' + self.__name
        with open(json_path, "w") as file:
            json.dump(compiled_sol, file)

        self.__json_path = Path(json_path)
        ## 字节码和abi
        print(compiled_sol)
        # ['Incrementer.sol:Incrementer']['abi']
        # key = self.__name + ':'
        for _, v in compiled_sol.items():
            contract = self.web3.eth.contract(abi=v['abi'], bytecode=v['bin'])
            self.__bytecode = contract.bytecode
            self.__abi = contract.abi
            break
        # self.__bytecode = compiled_sol["contracts"][self.__name]["SimpleStorage"]["evm"]["bytecode"]
        # self.__abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

        return self.__json_path

    ## 部署
    def deploy(self, zk_web3: Web3, account: LocalAccount, compiled_contract: Path):
        chain_id = zk_web3.zksync.chain_id
        # 签名工具 用于生成交易签名
        signer = PrivateKeyEthSigner(account, chain_id)

        # 获取随机数，使用账号交易次数
        nonce = zk_web3.zksync.get_transaction_count(account.address, EthBlockParams.PENDING.value)
        if self.__abi is None:
            # Get contract ABI and bytecode information
            storage_contract = ContractEncoder.from_json(zk_web3, compiled_contract)[0]
            self.__bytecode = storage_contract.bytecode
            self.__abi = storage_contract.abi
        print(self.abi)
        print(self.bytecode)
        # 燃料价格
        gas_price = zk_web3.zksync.gas_price
        # 创建合约部署交易
        create_contract = TxCreateContract(
            web3=zk_web3,
            chain_id=chain_id,
            nonce=nonce,
            from_=account.address,
            gas_limit=0,  # UNKNOWN AT THIS STATE
            gas_price=gas_price,
            bytecode=self.__bytecode,
        )
        # 交易总燃料
        estimate_gas = zk_web3.zksync.eth_estimate_gas(create_contract.tx)
        # 转换为 EIP-712 格式
        tx_712 = create_contract.tx712(estimate_gas)
        # 生成签名信息
        signed_message = signer.sign_typed_data(tx_712.to_eip712_struct())
        # 将签名信息使用 EIP-712 编码
        msg = tx_712.encode(signed_message)
        # 合约部署
        tx_hash = zk_web3.zksync.send_raw_transaction(msg)
        # 等待部署结果
        tx_receipt = zk_web3.zksync.wait_for_transaction_receipt(
            tx_hash, timeout=240, poll_latency=0.5
        )
        contract_address = tx_receipt["contractAddress"]

        print(f"Deployed contract address: {contract_address}")
        self.__address = contract_address

    ## 调用合约方法
    def m_call(self):
        pass

    ##属性方法
    @property
    def address(self):
        return self.__address
    @property
    def sol_path(self):
        return self.__sol_path
    @property
    def json_path(self):
        return self.__json_path
    @property
    def status(self):
        return self.__status
    @property
    def bytecode(self):
        return self.__bytecode
    @property
    def abi(self):
        return self.__abi
    pass
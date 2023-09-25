from zk_account import env
import operate as op
from operate import zk_contract
from pathlib import Path

from eth_account.signers.local import LocalAccount
from eth_typing import HexAddress
from web3 import Web3

## 合约部署
op.register('-5', '合约部署, 参数1: 账户地址（默认自身）')
@op.register('-5')
def deploy(account: LocalAccount, path: str) -> HexAddress:
    """Deploy compiled contract on zkSync network using create() opcode

    :param zk_web3:
        Instance of ZkSyncBuilder that interacts with zkSync network

    :param account:
        From which account the deployment contract tx will be made

    :param compiled_contract:
        Compiled contract source.

    :return:
        Address of deployed contract.
    """
    sdk: Web3 = env.sdk
    ## 创建合约对象
    contract = zk_contract.Zk_contract()
    f_path = Path(path)
    ## 如果尚未编译，先编译
    if f_path.name.split('.')[-1] == 'sol':
        f_path = contract.compile(f_path)
    ## 部署
    contract.deploy(sdk, account, f_path)




# if __name__ == "__main__":
#     # Set a provider
#     PROVIDER = "https://zksync2-testnet.zksync.dev"

#     # Byte-format private key
#     PRIVATE_KEY = bytes.fromhex(os.environ.get("PRIVATE_KEY"))

#     # Connect to zkSync network
#     zk_web3 = ZkSyncBuilder.build(PROVIDER)

#     # Get account object by providing private key of the sender
#     account: LocalAccount = Account.from_key(PRIVATE_KEY)

#     # Provide a compiled JSON source contract
    contract_path = Path("solidity/storage/build/combined.json")

#     # Perform contract deployment
#     deploy_contract(zk_web3, account, contract_path)
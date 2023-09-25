from zksync2.core.types import Token
from web3 import Web3

## 数字货币
class U_token():
    __address: str = None
    
    def __init__(self, address) -> None:
        self.__address = address

    @property
    def address(self):
        return self.__address
    pass

def checksum(address):
    return Web3.to_checksum_address(address)
class Tokens:
    ETH: U_token = U_token(checksum('0x000000000000000000000000000000000000800a'))
    WETH: U_token = U_token(checksum('0x5aea5775959fbc2557cc8789bc1bf90a239d9a91'))
    USDC: U_token = U_token(checksum('0x3355df6d4c9c3035724fd0e3914de96a5a83aaf4'))
    USDT: U_token = U_token(checksum('0x493257fd37edb34451f62edf8d2a0c418852ba4c'))
    
    pass

class DefaultEthGasLimit():
    Default = 1000000
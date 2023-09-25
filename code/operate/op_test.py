from typing import Any
from zksync2.manage_contracts.zksync_contract import ZkSyncContract
from web3.contract.contract import Contract, ContractFunction
from web3 import Web3
from zk_account import env
import utils.utils_file as uf
import utils.utils_time as utime
import solidity.abi.Syscswap as syscswap_abi

import utils.utils_token as ut
import json
from eth_abi.abi import encode


ZERO_ADDRESS = '0x0000000000000000000000000000000000000000'
class Syscswap():
    ## Main
    _WETH = '0x5aea5775959fbc2557cc8789bc1bf90a239d9a91'
    _WETH = '0x5aea5775959fbc2557cc8789bc1bf90a239d9a91'
    _Router = '0x2da10A1e27bF85cEdD8FFb1AbBe97e53391C0295'
    _ClassicPoolFactory = '0xf2DAd89f2788a8CD54625C60b55cD3d2D0ACa7Cb'
    _StablePoolFactory = '0x5b9f21d407F35b10CbfDDca17D5D84b129356ea3'
    _PoolMaster = '0xbB05918E9B4bA9Fe2c8384d223f0844867909Ffb'
    _Vault = '0x621425a1Ef6abE91058E9712575dcc4258F8d091'
    _PoolMaster = '0xbB05918E9B4bA9Fe2c8384d223f0844867909Ffb'
    # ## Test
    # WETH = '0x5aea5775959fbc2557cc8789bc1bf90a239d9a91'
    # Router = '0x2da10A1e27bF85cEdD8FFb1AbBe97e53391C0295'
    # PoolFactory = '0x5b9f21d407F35b10CbfDDca17D5D84b129356ea3'
    # Vault = '0x621425a1Ef6abE91058E9712575dcc4258F8d091'
    # PoolMaster = '0xbB05918E9B4bA9Fe2c8384d223f0844867909Ffb'
    # @property
    # def WETH(self) -> Contract:
    #     address = Web3.to_checksum_address(self._WETH)
    #     pool_abi = uf.read_abi(syscswap_abi, 'WETH.json')
    #     return acc.zk_web.eth.contract(address, abi=pool_abi)
    @property
    def Vault(self) -> Contract:
        address = Web3.to_checksum_address(self._Vault)
        abi = uf.read_abi(syscswap_abi, 'Vault.json')
        return env.sdk.eth.contract(address, abi=abi)
    @property
    def ClassicPoolFactory(self) -> Contract:
        address = Web3.to_checksum_address(self._ClassicPoolFactory)
        abi = uf.read_abi(syscswap_abi, 'ClassicPoolFactory.json')
        return env.sdk.eth.contract(address, abi=abi)
    @property
    def StablePoolFactory(self) -> Contract:
        address = Web3.to_checksum_address(self._StablePoolFactory)
        abi = uf.read_abi(syscswap_abi, 'StablePoolFactory.json')
        return env.sdk.eth.contract(address, abi=abi)
    @property
    def PoolMaster(self) -> Contract:
        address = Web3.to_checksum_address(self._PoolMaster)
        abi = uf.read_abi(syscswap_abi, 'PoolMaster.json')
        return env.sdk.eth.contract(address, abi=abi)
    @property
    def Router(self) -> Contract:
        address = Web3.to_checksum_address(self._Router)
        abi = uf.read_abi(syscswap_abi, 'Router.json')
        return env.sdk.eth.contract(address, abi=abi)
    
    def ClassicPool(self, address) -> Contract:
        abi = uf.read_abi(syscswap_abi, 'ClassicPool.json')
        return env.sdk.eth.contract(address, abi=abi)
    def StablePool(self, address) -> Contract:
        abi = uf.read_abi(syscswap_abi, 'StablePool.json')
        return env.sdk.eth.contract(address, abi=abi)

SwapDapp = Syscswap()
def _method_(contract, method_name: str) -> ContractFunction:
    return getattr(contract.functions, method_name)

import utils.utils_chain as uc
from zk_account import env
def query_eth_balance():
    chain_rpc = uc.get_chain('eth')
    print(chain_rpc)
    print(env.account.address)
    # chain_rpc = 'https://rpc.ankr.com/eth'
    eth_web3 = Web3(Web3.HTTPProvider(chain_rpc))
    
    # add_chain('eth', 'https://mainnet.infura.io/v3/10cd3354bd5a49d5b5b533c1fad56be7')
    # connection = Web3(Web3.HTTPProvider(chain_rpc))
    # print ("Latest Ethereum block number", connection.eth.block_number)
    balance = eth_web3.eth.get_balance(env.account.address)
    print(balance)
## 测试代码
def do_test():
    print('start test')
    do_other_test()
    # do_test_swap()
    # s = '[5,7]'
    # a, b = eval(s)
    # print(b)
    
    # d = [{a : 1, 'b' : 2}] # {}直接创建
    # print(d)

def do_test_swap():
    # query_eth_balance()
    ### step 1 获取交换池合约地址
    pool_factory = SwapDapp.ClassicPoolFactory
    # pool_factory = SwapDapp.StablePoolFactory
    func = _method_(pool_factory, 'getPool')
    eth_address = ut.Tokens.ETH.address
    weth_address = ut.Tokens.WETH.address
    usdc_address = ut.Tokens.USDC.address
    usdt_address = ut.Tokens.USDT.address
    pool_address = func(weth_address, usdc_address).call()
    print(pool_address)
    # func = _method_(SwapDapp.Vault, 'deposit')
    # print(func)
    # rs = func(usdc_address).call()
    v = env.sdk.to_wei(0.01, "ether")
    # print(v)
    # rs = func(eth_address, env.address, v).call()
    # rs = func(eth_address, env.address).call({'amount':v})
    # print(rs)

    # ### step 2 查询交换池储量
    pool = SwapDapp.ClassicPool(pool_address)
    rs = _method_(pool, 'getReserves')().call()
    print(rs)
    swap_data = encode(["address", "address", "uint8"],[weth_address, env.address, 1])
    print(swap_data)
    steps = [{'pool':pool_address,'data':swap_data, 'callback':ZERO_ADDRESS, 'callbackData': '0x'}]
    # v = 100000000
    paths = [{
        'steps': steps,
        'tokenIn': ZERO_ADDRESS,
        'amountIn': v,
    }]
    # step_info = {pool=pool_address}
    # pool_abi = uf.read_to_str(r'code\solidity\abi\Syscswap\BasePoolFactory.json')
    # pool_abi = uf.read_abi(syscswap_abi, 'BasePoolFactory.json')
    # p_abi = eval(pool_abi.replace('true', 'True').replace('false','False'))
    # print(pool_abi)
    # router_contract = ZkSyncContract(zksync_main_contract=Syscswap.Router, eth=env.sdk, account=env.account)
    # print(SwapDapp.Router.address)
    func = _method_(SwapDapp.Router, 'swap')
    deadline = utime.ts()+1800
    print(func, deadline)
    rs = func(paths, 0, deadline).call({'value': v})
    print(rs)
    # a = ['swap'([([('address',bytes,'address',bytes)],'address','uint256')],'uint256','uint256')]
    # router_contract._method_()
    # getattr()
    pass

class Test():
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.args = args
        self.kwds = kwds
        print(f'call me {args} {kwds}')
        return self

    def call(self, *args):
        print(f'old args: {self.args}')
        self.args = args
        print(f'new args: {args}')
        pass
    pass

from web3.types import (
    ABI,
    BlockIdentifier,
    CallOverride,
    EventData,
    TxParams,
)
from typing import cast

def do_other_test():
    # t = Test()
    # t(1,2, c=3).call(3,4)
    # d_start = 14
    # d_end = [1,24,24.5,24,25,25,25,24.5,24.5,25,25.5,26,25.5,22,24.5,24.5,24,25,24.5,25,25,25.5,25.5,24,24,25,26,26,24,24,24,24]
    # extra = [1,3,5,2,1,6,7,4,8,1,1,10,3,11,6,17,-2,3,3,2,0,18,7,8,1,-1,5,1,9,4]
    # t_all, t_ext,t_day = 0,0,0
    # for i in range(len(d_end)):
    #     t_all += (d_end[i]-d_start)
    #     t_day = i
    #     t_ext += extra[i]
    #     # if len(extra) > i:
    #     #     t_ext += extra[i]
    #     #     print(t_ext)
    #     # pass
    # print(f'总天数{t_day},总时长{t_all}小时,额外时间{t_ext}分钟')

    # s = '[3,4]'
    # tlist = eval(s)
    # print(tlist)
    # s = '3,4'
    # ttuple = eval(s)
    # print(ttuple)
    d = {'vv':123,'value':0.1}
    # d = 1
    # dd = cast(TxParams, d)
    # print(f'd:{d} type:{type(d)}, dd:{dd} type:{type(dd)}, ')
    # print(f'd:{d}, type:{type(d)}')
    d1 = cast(str, d)
    ttt(d1)
    ttt(d)
    pass
def ttt(p1: str):
    print(p1)

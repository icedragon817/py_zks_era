from pathlib import Path
contract_path = Path("code/solidity/voted.sol")
print(contract_path)
print(contract_path.name)
print(contract_path._drv)
print(contract_path._root)
print(contract_path._parts)
# print(contract_path.d)
import os
from brownie import network
from brownie.network.account import Account
from brownie.network.contract import Contract
from balsnap import SnapshotAccount, BalSnap

# Constant
MULTICALL2_ADDRESS = "0x5ba1e12693dc8f9c48aad8770482f4739beed696"
WEB3_INFURA_PROJECT_ID = "b14361ade6504e66a79599c2df794c0c"
ETHERSCAN_TOKEN = "D4UBU1ZHYPIZ5PYP38TKNRH79D3WW2X8XZ"

# Set up the brownie network
os.environ["ETHERSCAN_TOKEN"] = ETHERSCAN_TOKEN
os.environ["WEB3_INFURA_PROJECT_ID"] = WEB3_INFURA_PROJECT_ID
network.connect('mainnet')  # ATTENTION: here is mainnet!

# Initialize an Account() instance by providing an address
account = Account('0xF5D6849f0d1D5E84b047F157990cF016c046a433')
# Or just an address
# account = '0xF5D6849f0d1D5E84b047F157990cF016c046a433'

# Initialize an Contract() instance by providing an address
contract = Contract.from_explorer("0x6b175474e89094c44da98b954eedeac495271d0f")  # DAI
# Or just an address as well
# contract = "0x6b175474e89094c44da98b954eedeac495271d0f"

# Build account-contract pair
snapshot_account = SnapshotAccount(account, contract)

# Initialize BalSnap()
balsnap = BalSnap(multicall2_address=MULTICALL2_ADDRESS)
# Add pair
balsnap.add_snapshot_account(snapshot_account)
# Take snapshot
balsnap.snapshot()
# Visualize the result
balsnap.print_table()
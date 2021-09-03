import os
from brownie import network

from balsnap import BalSnap
from utils import create_snapshot_accounts

# Constant
MULTICALL2_ADDRESS = "0x5ba1e12693dc8f9c48aad8770482f4739beed696"
WEB3_INFURA_PROJECT_ID = "b14361ade6504e66a79599c2df794c0c"
ETHERSCAN_TOKEN = "D4UBU1ZHYPIZ5PYP38TKNRH79D3WW2X8XZ"

# Set up the brownie network
os.environ["ETHERSCAN_TOKEN"] = ETHERSCAN_TOKEN
os.environ["WEB3_INFURA_PROJECT_ID"] = WEB3_INFURA_PROJECT_ID
network.connect('mainnet')  # ATTENTION: here is mainnet!

account_1 = "0xF5D6849f0d1D5E84b047F157990cF016c046a433"
account_2 = '0x43CC25B1fB6435d8d893fCf308de5C300a568BE2'

contract_1 = "0x6b175474e89094c44da98b954eedeac495271d0f"  # DAI
contract_2 = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"  # USDC

# create_snapshot_accounts() method will perform cartesian product on accounts
# and contracts and return a SnapshotAccount List. You can only manually create
# this list simplying by instializing SnapshotAccount instance and appending it
# to a list.
snapshot_accounts = create_snapshot_accounts([account_1, account_2],
                                             [contract_1, contract_2])

balsnap = BalSnap(multicall2_address=MULTICALL2_ADDRESS)
balsnap.add_snapshot_accounts(snapshot_accounts)
balsnap.snapshot()
balsnap.print_table()
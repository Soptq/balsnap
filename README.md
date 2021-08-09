# Balsnap

A light-weight python library that help take balance snapshots of multiple tokens and accounts at once.

Features:

* Light-weight: less than 200 lines of code.
* Easy to use and modify: delivered with documentations.
* Fast: using [multicall](https://github.com/makerdao/multicall) to reduce JSON RPC requests.

## Installation

### Pypi

```

```

### Build from source

```

```

## Quick Start

### Simple example

```python
import os
from brownie import network
from brownie.network.account import Account
from brownie.network.contract import Contract
from balsnap import SnapshotAccount, BalSnap

# Constant
MULTICALL2_ADDRESS = "0x5ba1e12693dc8f9c48aad8770482f4739beed696"
WEB3_INFURA_PROJECT_ID = "YOUR_INFURA_ID"
ETHERSCAN_TOKEN = "YOUR_ETHERSCAN_TOKEN"

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

# ... YOUR TRANSACTION

# Take another snapshot
balsnap.snapshot()
# Visualize the result
balsnap.print_table()
```

output:
```
+---------------+--------------------+------------------+---------------------+
|    Account    |      Contract      |     Balance      |         Time        |
+---------------+--------------------+------------------+---------------------+
| 0xF5D6...a433 | DAI(0x6B17...1d0F) | 909.082000603966 | 2021-08-09 22:19:44 |
+---------------+--------------------+------------------+---------------------+

+---------------+--------------------+------------------+---------------------+
|    Account    |      Contract      |     Balance      |         Time        |
+---------------+--------------------+------------------+---------------------+
| 0xF5D6...a433 | DAI(0x6B17...1d0F) | 999.082000603966 | 2021-08-09 23:14:11 |
+---------------+--------------------+------------------+---------------------+
```

### Take multiple snapshots at once

```python
import os
from brownie import network

from balsnap import BalSnap, create_snapshot_accounts

# Constant
MULTICALL2_ADDRESS = "0x5ba1e12693dc8f9c48aad8770482f4739beed696"
WEB3_INFURA_PROJECT_ID = "YOUR_INFURA_ID"
ETHERSCAN_TOKEN = "YOUR_ETHERSCAN_TOKEN"

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
```

output:
```
+---------------+---------------------+-------------------+---------------------+
|    Account    |       Contract      |      Balance      |         Time        |
+---------------+---------------------+-------------------+---------------------+
| 0xF5D6...a433 |  DAI(0x6B17...1d0F) |  909.082000603966 | 2021-08-09 22:26:28 |
| 0xF5D6...a433 | USDC(0xA0b8...eB48) |     45.334263     | 2021-08-09 22:26:29 |
| 0x43CC...8BE2 |  DAI(0x6B17...1d0F) | 3126.039500865128 | 2021-08-09 22:26:28 |
| 0x43CC...8BE2 | USDC(0xA0b8...eB48) |    87564.905951   | 2021-08-09 22:26:29 |
+---------------+---------------------+-------------------+---------------------+
```

### Filter

You can filter some account addresses and contract address when visualizing.

```python
balsnap.print_table(account_address_filtered="0x43CC25B1fB6435d8d893fCf308de5C300a568BE2")
```

output:
```
+---------------+---------------------+-------------------+---------------------+
|    Account    |       Contract      |      Balance      |         Time        |
+---------------+---------------------+-------------------+---------------------+
| 0xF5D6...a433 |  DAI(0x6B17...1d0F) |  909.082000603966 | 2021-08-09 22:26:28 |
| 0xF5D6...a433 | USDC(0xA0b8...eB48) |     45.334263     | 2021-08-09 22:26:29 |
+---------------+---------------------+-------------------+---------------------+
```

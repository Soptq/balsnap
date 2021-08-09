from typing import Union, List
from brownie.network.account import Account
from brownie.network.contract import Contract
from balsnap import SnapshotAccount


def create_snapshot_accounts(accounts: List[Union[Account, str]], contracts: List[Union[Contract, str]]) \
        -> List[SnapshotAccount]:
    """
    Make a cartesian product between a list of accounts and a list of contracts

    Arguments
        ---------
        accounts : List[Union[Account, str]]
            A list of accounts
        contracts : List[Union[Contract, str]]
            A list of contracts

        Returns
        -------
        A list of SnapshotAccount
    """
    snapshot_accounts = []
    for account in accounts:
        for contract in contracts:
            snapshot_accounts.append(SnapshotAccount(account, contract))
    return snapshot_accounts

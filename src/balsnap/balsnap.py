import os, time, datetime

from typing import Union, List

from brownie import multicall
from brownie.network.account import Account
from brownie.network.contract import Contract
from brownie.network.web3 import _resolve_address

from web3 import Web3
from prettytable import PrettyTable

from collections import namedtuple
import warnings

snapshot_record = namedtuple("snapshot_record", ["timestamp", "value"])


class SnapshotAccount:
    """
    This class stores account-contract pair to be later snapshot-ed.
    """

    def __init__(self, account: Union[Account, str], contract: Union[Contract, str]):
        """
        Constructor requires an account input and a contract input.
        :param account: either address string or brownie Account().
        :param contract: either address string or brownie Contract().
        """
        self.account_address: str = _resolve_address(account) if isinstance(account, str) else account.address
        self.contract_address: str = _resolve_address(contract) if isinstance(contract, str) else contract.address

        self.snapshot_records: List[snapshot_record] = []

    def add_balance(self, balance: float):
        """
        Provided a balance, this method will record it.
        :param balance: the balance of the account owning the contract.
        """
        self.snapshot_records.append(snapshot_record(time.time(), balance))


class BalSnap:
    """
    This is the main class of this package. All snapshot logic will be handled here.
    """

    def __init__(self, multicall2_address: str = None):
        """
        Constructor requires a multicall2_address to initialize multicall2.
        and a etherscan_api to pull necessary information of the contract from etherscan.
        :param multicall_address: the multicall2 contract address, can be found at https://github.com/makerdao/multicall
        """
        if multicall2_address is not None and isinstance(multicall2_address, str):
            self.multicall2_address = multicall2_address
        else:
            warnings.warn("multicall contract address is not configured, "
                          "default to mainnet multicall2 contract address: 0x5ba1e12693dc8f9c48aad8770482f4739beed696")
            self.multicall2_address = "0x5ba1e12693dc8f9c48aad8770482f4739beed696"

        self.snapshot_accounts: List[SnapshotAccount] = []
        self.contract_info = {}

    def add_snapshot_account(self, snapshot_account: SnapshotAccount):
        """
        Add a SnapshotAccount instance.
        :param snapshot_account: a SnapshotAccount instance.
        """
        self._add_if_account_not_exists(snapshot_account)

    def add_snapshot_accounts(self, snapshot_accounts: List[SnapshotAccount]):
        """
        Add multiple SnapshotAccount instances at once.
        :param snapshot_accounts: A list of SnapshotAccount instances
        """
        for snapshot_account in snapshot_accounts:
            self._add_if_account_not_exists(snapshot_account)

    def snapshot(self):
        """
        Using multicall2 to snapshot balances of all added snapshot accounts.
        """
        for contract_address in self.contract_info.keys():
            task_snapshot_accounts = [sa for sa in self.snapshot_accounts if sa.contract_address == contract_address]
            with multicall(Web3.toChecksumAddress(self.multicall2_address)):
                for task_snapshot_account in task_snapshot_accounts:
                    task_snapshot_account.add_balance(
                        float(self.contract_info[contract_address]["instance"].balanceOf(
                            task_snapshot_account.account_address
                        )) / (10 ** int(self.contract_info[contract_address]["decimals"]))
                    )

    def print_table(self, abstract_digits: int = 4,
                    account_address_filtered: Union[str, List[str]] = None,
                    contract_address_filtered: Union[str, List[str]] = None):
        """
        Pretty print the snapshot result as a table.
        :param abstract_digits: a int indicates how many digits we will keep for the address. -1 to keep all.
        :param account_address_filtered: a str or a list of str
                to indicate what account addresses to be filtered in the table.
        :param contract_address_filtered: a str or a list of str
                to indicate what contract addresses to be filtered in the table.
        """
        table = PrettyTable()
        table.field_names = ["Account", "Contract", "Balance", "Time"]
        for snapshot_account in self.snapshot_accounts:
            if snapshot_account.snapshot_records[-1].value <= 0:
                continue
            account_address = snapshot_account.account_address
            contract_address = snapshot_account.contract_address

            if account_address_filtered is not None:
                if isinstance(account_address_filtered, str) and account_address == account_address_filtered:
                    return
                if isinstance(account_address_filtered, list) and account_address in account_address_filtered:
                    return

            if contract_address_filtered is not None:
                if isinstance(contract_address_filtered, str) and contract_address == contract_address_filtered:
                    return
                if isinstance(contract_address_filtered, list) and contract_address in contract_address_filtered:
                    return

            table.add_row([self.abstract_address(account_address, digits=abstract_digits),
                           f"{self._get_contract_symbol(contract_address)}({self.abstract_address(contract_address, abstract_digits)})",
                           snapshot_account.snapshot_records[-1].value,
                           self._pretty_datetime(snapshot_account.snapshot_records[-1].timestamp)])
        print(table)

    def _add_if_account_not_exists(self, snapshot_account):
        for _snapshot_account in self.snapshot_accounts:
            if _snapshot_account.account_address == snapshot_account.account_address \
                    and _snapshot_account.contract_address == snapshot_account.contract_address:
                return
        self._retrieve_contract_info_from_chain(snapshot_account)
        self.snapshot_accounts.append(snapshot_account)

    def _retrieve_contract_info_from_chain(self, snapshot_account):
        contract_address = snapshot_account.contract_address
        if contract_address not in self.contract_info:
            self.contract_info[contract_address] = {}
            self.contract_info[contract_address]["instance"] = Contract.from_explorer(contract_address)
            self.contract_info[contract_address]["name"] = self.contract_info[contract_address]["instance"].name()
            self.contract_info[contract_address]["symbol"] = self.contract_info[contract_address]["instance"].symbol()
            self.contract_info[contract_address]["decimals"] = self.contract_info[contract_address][
                "instance"].decimals()

    def _get_contract_name(self, contract_address):
        return self.contract_info[contract_address]["name"]

    def _get_contract_symbol(self, contract_address):
        return self.contract_info[contract_address]["symbol"]

    def _get_contract_decimals(self, contract_address):
        return self.contract_info[contract_address]["decimals"]

    @staticmethod
    def _pretty_datetime(timestamp):
        return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def abstract_address(address, digits=4):
        return address if digits == -1 else f"{address[:digits + 2]}...{address[-digits:]}"

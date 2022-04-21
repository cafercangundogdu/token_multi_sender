import json
import time

from typing import List, Dict, Callable

from web3 import Web3

from config import Config
from utils import load_json_from_file, WalletType


class TokenMultiSender:
    def __init__(self, config: Config, wallet_type: WalletType) -> None:
        self.wallet = None
        self.contract = None
        self.client = None
        self.config = config
        self.abi = None
        self.contract_address = None
        self.addresses = []
        self.events: Dict[str, List[Callable]] = {}
        # pre defined events:
        #   before_transfer
        #   after_transfer

        self._init_client()
        self._init_wallet(wallet_type=wallet_type)
        self._init_abi()
        self._init_contract_address()
        self._init_contract()
        self._init_addresses()

    def _init_addresses(self):
        self.addresses = load_json_from_file(self.config.get_wallet_json_path())

    def _init_contract_address(self):
        self.contract_address = self.config.get_contract_address()

    def _init_client(self):
        chain = Web3(Web3.HTTPProvider(self.config.get_http_provider()))
        if chain.isConnected():
            print("Connected!")
            self.client = chain

        raise Exception("Client not connected!")

    def _init_wallet(self, wallet_type: WalletType):
        if wallet_type == WalletType.PRIVATE_KEY:
            self.wallet = self.client.eth.account.from_key(self.config.get_private_key())
        elif wallet_type == WalletType.MNEMONIC:
            self.client.eth.account.enable_unaudited_hdwallet_features()
            self.wallet = self.client.eth.account.from_mnemonic(self.config.get_mnemonic())
        else:
            raise Exception(f"Wallet type not supported! {wallet_type}")

    def _init_abi(self):
        self.abi = load_json_from_file(self.config.get_abi_path())

    def _init_contract(self):
        self.contract = self.client.eth.contract(
            address=self.client.toChecksumAddress(self.contract_address), abi=self.abi)

    def on(self, name: str, fn: Callable):
        if name not in self.events:
            self.events[name] = []
        self.events[name].append(fn)

    def fire(self, name: str, data):
        if name in self.events:
            for fn in self.events[name]:
                try:
                    fn(data)
                except Exception as e:
                    print(f"Exception when calling event {name} exp {e}")

    def __transfer(self, address: str, amount: int) -> str:
        nonce = self.client.eth.getTransactionCount(self.wallet.address)
        tx = self.contract.functions.transfer(
            self.client.toChecksumAddress(
                address), self.client.toWei(amount, "gwei")
        ).buildTransaction({
            'chainId': self.config.get_chain_id(),
            'gas': self.config.get_gas(),
            'gasPrice': self.client.toWei(10, "gwei"),
            'nonce': nonce
        })
        sign_tx = self.client.eth.account.sign_transaction(
            tx, private_key=self.client.toHex(self.wallet.privateKey))

        return self.client.toHex(
            self.client.eth.send_raw_transaction(sign_tx.rawTransaction))

    def send_all(self):  # TODO: check sender wallet balance
        for address, amount in self.addresses:
            self.fire("before_transfer", {"address": address, "amount": amount})
            tx_hash = self.__transfer(address, amount)
            self.fire("after_transfer", {"address": address, "amount": amount, "tx_hash": tx_hash})
            time.sleep(0.1)

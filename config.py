from typing import Dict


class Config():
    def __init__(self, config_dict: Dict[str, str]):
        self.config = config_dict

    def get_config(self):
        return self.config

    def get_http_provider(self):
        return self.config["HTTP_PROVIDER"]

    def get_chain_id(self):
        return self.config["CHAIN_ID"]

    def get_gas(self):
        return self.config["GAS"]

    def get_abi_path(self):
        return self.config["ABI_PATH"]

    def get_contract_address(self):
        return self.config["CONTRACT_ADDRESS"]

    def get_wallet_json_path(self):
        return self.config["WALLETS_JSON_PATH"]

    def get_private_key(self):
        return self.config["PRIVATE_KEY"]

    def get_mnemonic(self):
        return self.config["MNEMONIC"]
from typing import List

from dotenv import dotenv_values

from config import Config
from token_multi_sender import TokenMultiSender
from utils import WalletType

is_prod = False

print("Token Multi Sender started..")
ans = input(f"TMS is running with {'production' if is_prod else 'dev'} environment! \n\t Are you sure to continue? (yes/no)\n")
if ans != "yes":
    print("exiting..")
    exit()

env_path = ".env" if is_prod else ".env.dev"
config = Config(config_dict=dotenv_values(dotenv_path=env_path))


def on_before_transfer(data: List[str]):
    [address, amount] = data
    print(f"Will send {amount} token to {address}")


def on_after_transfer(data: List[str]):  # TODO: save transferred address
    [address, amount, tx_hash] = data
    print(f"Successfully send {amount} token to {address} transaction hash: {tx_hash}")


def main():
    token_multi_sender = TokenMultiSender(config=config, wallet_type=WalletType.PRIVATE_KEY)
    token_multi_sender.on("before_transfer", on_before_transfer)
    token_multi_sender.on("after_transfer", on_after_transfer)
    token_multi_sender.send_all()


if __name__ == '__main__':
    main()

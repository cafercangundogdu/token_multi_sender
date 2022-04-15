import json
from enum import Enum


class WalletType(Enum):
    PRIVATE_KEY = 1
    MNEMONIC = 2


def load_json_from_file(path):
    with open(path) as f:
        return json.loads(f.read())

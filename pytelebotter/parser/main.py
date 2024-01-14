import base64
import json
import os

import pytelebotter.utils.types


def parse_accounts_config() -> pytelebotter.utils.types.AccountsConfig:
    if not (config := os.getenv("CONFIG_ACCOUNTS")):
        return json.load(open("config_accounts.json"))
    else:
        return json.loads(base64.b64decode(config))

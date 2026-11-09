import json
from account import Account
import os


def account_to_dict(acc):
    return {
        "owner": acc.owner,
        "balance": acc.balance,
        "history": acc.history
        }


def account_from_dict(data):
    acc = Account(data["owner"], data["balance"])
    acc.history = data["history"]
    return acc


def save_accounts(accounts, path):
    serialized_accounts = []
    for acc in accounts:
        serialized_accounts.append(account_to_dict(acc))
    with open(f"{path}.tmp", 'w', encoding="utf-8") as file:
        json.dump(serialized_accounts, file, ensure_ascii=False, indent=2)
    os.replace(f"{path}.tmp", path)


def load_accounts(path):
    accounts = []
    with open(path, 'r', encoding="utf-8") as data_file:
        data = json.load(data_file)
        for acc in data:
            accounts.append(account_from_dict(acc))
    return accounts

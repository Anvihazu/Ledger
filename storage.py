import json
from account import Account
import os



class CorruptedStorage(Exception):
    pass


def account_validation(acc):
    try:
        if type(acc["owner"]) != str:
            raise CorruptedStorage
        if type(acc["balance"]) != int:
            raise CorruptedStorage
        if acc["balance"] < 0:
            raise CorruptedStorage
        if type(acc["history"]) != list:
            raise CorruptedStorage
        if not all(type(i) == str for i in acc["history"]):
            raise CorruptedStorage
    except(KeyError, TypeError):
        raise CorruptedStorage


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
    if not os.path.exists(path):
        return []
    accounts = []
    try:
        with open(path, 'r', encoding="utf-8") as data_file:
            data = json.load(data_file)
            if type(data) != list:
                raise CorruptedStorage
            for acc in data:
                account_validation(acc)
                accounts.append(account_from_dict(acc))
        return accounts
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise CorruptedStorage

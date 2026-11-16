import argparse
import storage
from account import Account
import sys


def find_account(accounts, owner):
    for acc in accounts:
        if acc.owner == owner:
            return acc
    return None


def build_parser():
    parser = argparse.ArgumentParser(description = "Bank CLI")
    subparsers = parser.add_subparsers(dest = "command", required = True)
    create_parser = subparsers.add_parser("create", help = "Create new account")
    create_parser.add_argument("owner", help = "Owner name")
    create_parser.add_argument("--balance", type = int, default = 0, help = "Opening balance")
    balance_parser = subparsers.add_parser("balance", help = "Show balance")
    balance_parser.add_argument("owner", help = "Owner name")
    return parser


def main(argv = None, path = "accounts.json"):
    parser = build_parser()
    args = parser.parse_args(argv)
    accounts = storage.load_accounts(path)
    try:
        if args.command == "create":
            if find_account(accounts, args.owner) is not None:
                print(f"Account with name: {args.owner} already exists!")
                sys.exit(1)  
            new_acc = Account(args.owner, args.balance)
            accounts.append(new_acc)
            storage.save_accounts(accounts, path)
            print(f"Success, account with name: {args.owner} has been created!")
        elif args.command == "balance":
            acc = find_account(accounts, args.owner)
            if acc is None:
                print(f"Account {args.owner} not found!")
                sys.exit(1)
            print(f"{args.owner}, your balance is {acc.balance}.")
    except ValueError:
        print(f"Balance cannot be negative!")
        sys.exit(1)


if __name__ == "__main__":
    main() # pragma: no cover

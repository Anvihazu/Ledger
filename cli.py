import argparse
import sys
from pathlib import Path

import storage
from account import (
    Account,
    BoolAmount,
    FloatAmount,
    InsufficientFunds,
    InvalidReceiver,
    NoneAmount,
    SelfTransfer,
)

ERROR_MESSAGES = {
    InsufficientFunds: "Insufficient funds.",
    SelfTransfer: "Cannot transfer money to yourself.",
    InvalidReceiver: "Invalid receiver account.",
    FloatAmount: "Amount must be an integer, not a float.",
    BoolAmount: "Amount cannot be a boolean.",
    NoneAmount: "Amount cannot be None.",
    TypeError: "Invalid value type.",
    ValueError: "Amount or balance must be positive.",
    storage.CorruptedStorage: "Storage file is corrupted.",
}


def find_account(accounts: list[Account], owner: str) -> Account | None:
    for acc in accounts:
        if acc.owner == owner:
            return acc
    return None


def get_account(accounts: list[Account], owner: str) -> Account:
    for acc in accounts:
        if acc.owner == owner:
            return acc
    print(f"Account '{owner}' not found!", file=sys.stderr)
    sys.exit(1)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Bank CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)
    create_parser = subparsers.add_parser("create", help="Create new account")
    create_parser.add_argument("owner", help="Owner name")
    create_parser.add_argument("--balance", type=int, default=0, help="Opening balance")
    balance_parser = subparsers.add_parser("balance", help="Show balance")
    balance_parser.add_argument("owner", help="Owner name")
    deposit_parser = subparsers.add_parser("deposit", help="Deposit sum")
    deposit_parser.add_argument("owner", help="Owner name")
    deposit_parser.add_argument("amount", type=int, help="Amount to deposit")
    withdraw_parser = subparsers.add_parser("withdraw", help="Withdraw sum")
    withdraw_parser.add_argument("owner", help="Owner name")
    withdraw_parser.add_argument("amount", type=int, help="Amount to withdraw")
    transfer_parser = subparsers.add_parser(
        "transfer", help="Transfer amount between accounts"
    )
    transfer_parser.add_argument("sender", help="Sender name")
    transfer_parser.add_argument("receiver", help="Receiver name")
    transfer_parser.add_argument("amount", type=int, help="Amount to transfer")
    history_parser = subparsers.add_parser("history", help="Account history")
    history_parser.add_argument("owner", help="Owner name")
    return parser


def main(argv: list[str] | None = None, path: Path | str = "accounts.json") -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    accounts = storage.load_accounts(path)
    try:
        if args.command == "create":
            if find_account(accounts, args.owner) is not None:
                print(
                    f"Account with name: {args.owner} already exists!", file=sys.stderr
                )
                sys.exit(1)
            new_acc = Account(args.owner, args.balance)
            accounts.append(new_acc)
            storage.save_accounts(accounts, path)
            print(f"Success, account with name: {args.owner} has been created!")
        elif args.command == "balance":
            acc = get_account(accounts, args.owner)
            print(f"{args.owner}, your balance is {acc.balance}.")
        elif args.command == "deposit":
            acc = get_account(accounts, args.owner)
            acc.deposit(args.amount)
            storage.save_accounts(accounts, path)
            print(f"Deposited {args.amount} to {acc.owner}. New balance: {acc.balance}")
        elif args.command == "withdraw":
            acc = get_account(accounts, args.owner)
            acc.withdraw(args.amount)
            storage.save_accounts(accounts, path)
            print(
                f"Withdrew {args.amount} from {acc.owner}. New balance: {acc.balance}."
            )
        elif args.command == "transfer":
            sender = get_account(accounts, args.sender)
            receiver = get_account(accounts, args.receiver)
            sender.transfer(args.amount, receiver)
            storage.save_accounts(accounts, path)
            print(f"Transferred {args.amount} from {sender.owner} to {receiver.owner}.")
        elif args.command == "history":
            acc = get_account(accounts, args.owner)
            if not acc.history:
                print(f"No transactions found for {acc.owner}.")
            else:
                for operation in acc.history:
                    print(operation)
    except tuple(ERROR_MESSAGES.keys()) as err:
        message = ERROR_MESSAGES.get(type(err), str(err))
        print(f"Error: {message}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()  # pragma: no cover

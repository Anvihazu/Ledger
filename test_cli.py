import pytest

import cli
import storage
from account import Account


@pytest.fixture
def file_path(tmp_path):
    return tmp_path / "accounts.json"


@pytest.fixture
def accounts_file(file_path):
    accounts = [
        Account("Ann", 500),
        Account("Bob", 300),
    ]
    storage.save_accounts(accounts, file_path)
    return file_path


@pytest.fixture
def existing_account(file_path, capsys):
    cli.main(["create", "Dmitriy", "--balance", "300"], path=file_path)
    capsys.readouterr()
    return file_path


# other
@pytest.mark.parametrize(
    "argv, expected_err",
    [
        (["deposit", "Ann", "0"], "positive"),
        (["deposit", "Ann", "-50"], "positive"),
        (["deposit", "Ghost", "200"], "not found"),
        (["withdraw", "Ann", "0"], "positive"),
        (["withdraw", "Ann", "-50"], "positive"),
        (["withdraw", "Ann", "1000"], "Insufficient"),
        (["withdraw", "Ghost", "200"], "not found"),
        (["transfer", "Ann", "Bob", "0"], "positive"),
        (["transfer", "Ann", "Bob", "-50"], "positive"),
        (["transfer", "Ann", "Bob", "1000"], "Insufficient"),
        (["transfer", "Ghost", "Bob", "200"], "not found"),
        (["transfer", "Ann", "Ann", "300"], "yourself"),
        (["transfer", "Ann", "Ghost", "200"], "not found"),
        (["history", "Ghost"], "not found"),
        (["balance", "Ghost"], "not found"),
    ],
)
def test_invalid_cli_operations(argv, expected_err, capsys, accounts_file):
    before_test = accounts_file.read_text(encoding="utf-8")
    with pytest.raises(SystemExit) as excinfo:
        cli.main(argv, path=accounts_file)
    assert excinfo.value.code == 1
    captured_info = capsys.readouterr()
    assert expected_err in captured_info.err
    assert accounts_file.read_text(encoding="utf-8") == before_test


@pytest.mark.parametrize(
    "argv",
    [
        [],
        ["deposit", "Ann", "xyz"],
        ["withdraw", "Ann", "10.5"],
        ["transfer", "Ann", "Bob", "abc"],
    ],
)
def test_argparse_errors(accounts_file, argv):
    with pytest.raises(SystemExit) as excinfo:
        cli.main(argv, path=accounts_file)
    assert excinfo.value.code == 2


def test_corrupted_json(file_path, capsys):
    with open(file_path, "w") as corrupted_file:
        corrupted_file.write("{not json")
    with pytest.raises(SystemExit) as excinfo:
        cli.main(["balance", "Ann"], path=file_path)
    assert excinfo.value.code == 1
    captured_info = capsys.readouterr()
    assert "corrupted" in captured_info.err


# tests for create
def test_valid_create_and_balance_(file_path, capsys):
    cli.main(["create", "Oleg", "--balance", "500"], path=file_path)
    load_result = storage.load_accounts(file_path)
    assert load_result[0].owner == "Oleg"
    assert load_result[0].balance == 500
    captured_info = capsys.readouterr()
    assert "Oleg" in captured_info.out
    cli.main(["balance", "Oleg"], path=file_path)
    captured_info = capsys.readouterr()
    assert "500" in captured_info.out


def test_create_existing_account(existing_account, capsys):
    with pytest.raises(SystemExit) as excinfo:
        cli.main(["create", "Dmitriy", "--balance", "200"], path=existing_account)
    assert excinfo.value.code == 1
    captured_info = capsys.readouterr()
    assert "already exists" in captured_info.err


# tests for balance
def test_create_negative_opening_balance(file_path, capsys):
    with pytest.raises(SystemExit) as excinfo:
        cli.main(["create", "Oleg", "--balance", "-500"], path=file_path)
    assert excinfo.value.code == 1
    assert not file_path.exists()
    captured_info = capsys.readouterr()
    assert "must be positive" in captured_info.err


def test_balance_for_non_existing_acc(file_path, capsys):
    with pytest.raises(SystemExit) as excinfo:
        cli.main(["balance", "Oleg"], path=file_path)
    assert excinfo.value.code == 1
    assert not file_path.exists()
    captured_info = capsys.readouterr()
    assert "not found" in captured_info.err


# test for deposit
def test_valid_deposit(accounts_file, capsys):
    cli.main(["deposit", "Bob", "500"], path=accounts_file)
    captured_info = capsys.readouterr()
    assert "Deposited" in captured_info.out
    load_result = storage.load_accounts(accounts_file)
    assert load_result[1].balance == 800


# test for withdraw
def test_valid_withdraw(accounts_file, capsys):
    cli.main(["withdraw", "Ann", "300"], path=accounts_file)
    captured_info = capsys.readouterr()
    assert "Withdrew" in captured_info.out
    load_result = storage.load_accounts(accounts_file)
    assert load_result[0].balance == 200


# test for transfer
def test_valid_transfer(accounts_file, capsys):
    cli.main(["transfer", "Ann", "Bob", "400"], path=accounts_file)
    captured_info = capsys.readouterr()
    assert "Transferred" in captured_info.out
    load_result = storage.load_accounts(accounts_file)
    assert load_result[0].balance == 100
    assert load_result[1].balance == 700
    assert (load_result[0].balance + load_result[1].balance) == 800
    assert len(load_result[0].history) == 1
    assert len(load_result[1].history) == 1


# tests for history
def test_empty_history(accounts_file, capsys):
    cli.main(["history", "Ann"], path=accounts_file)
    captured_info = capsys.readouterr()
    assert "found for" in captured_info.out
    load_result = storage.load_accounts(accounts_file)
    assert len(load_result[0].history) == 0


def test_history_with_operations(accounts_file, capsys):
    cli.main(["withdraw", "Ann", "300"], path=accounts_file)
    cli.main(["deposit", "Ann", "800"], path=accounts_file)
    load_result = storage.load_accounts(accounts_file)
    capsys.readouterr()
    assert len(load_result[0].history) == 2
    cli.main(["history", "Ann"], path=accounts_file)
    captured_info = capsys.readouterr()
    assert "Deposited" in captured_info.out
    assert "Withdrew" in captured_info.out

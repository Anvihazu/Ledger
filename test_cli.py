import pytest
import cli
import storage


@pytest.fixture
def file_path(tmp_path):
    return tmp_path / "accounts.json"


@pytest.fixture
def existing_account(file_path, capsys):
    cli.main(["create", "Dmitriy", "--balance", "300"], path=file_path)
    capsys.readouterr()
    return file_path


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


def test_create_existing_account(existing_account):
    with pytest.raises(SystemExit) as excinfo:
        cli.main(["create", "Dmitriy", "--balance", "200"], path=existing_account)
    assert excinfo.value.code == 1


# tests for balance
def test_create_negative_opening_balance(file_path):
    with pytest.raises(SystemExit) as excinfo:
        cli.main(["create", "Oleg", "--balance", "-500"], path=file_path)
    assert excinfo.value.code == 1
    assert not file_path.exists()


def test_balance_for_non_existing_acc(file_path):
    with pytest.raises(SystemExit) as excinfo:
        cli.main(["balance", "Oleg"], path=file_path)
    assert excinfo.value.code == 1
    assert not file_path.exists()

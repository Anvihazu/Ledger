import pytest
import account
import storage
import json


@pytest.fixture
def human():
    return account.Account("Name", 500)


@pytest.fixture
def human_2():
    acc = account.Account("Name_2", 300)
    acc.history.append("Deposited 200.")
    return acc


def test_save_load_accounts(tmp_path, human, human_2):
    file_path = tmp_path / "accounts.json"
    accounts = [human, human_2]
    storage.save_accounts(accounts, file_path)
    load_result = storage.load_accounts(file_path)
    assert load_result[0].owner == human.owner
    assert load_result[0].balance == human.balance
    assert load_result[0].history == human.history
    assert load_result[1].owner == human_2.owner
    assert load_result[1].balance == human_2.balance
    assert load_result[1].history == human_2.history


def test_save_leaves_no_temp_file(tmp_path, human, human_2):
    file_path = tmp_path / "accounts.json"
    accounts = [human, human_2]
    storage.save_accounts(accounts, file_path)
    names = []
    for p in tmp_path.iterdir():
        names.append(p.name)
    assert names == ["accounts.json"]

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


def test_load_no_file_return_list(tmp_path):
    file_path = tmp_path / "accounts.json"
    load_result = storage.load_accounts(file_path)
    assert load_result == []


def test_corrupted_json(tmp_path):
    file_path = tmp_path / "accounts.json"
    with open(file_path, 'w') as corrupted_file:
        corrupted_file.write("{not json")
    with pytest.raises(storage.CorruptedStorage):
        storage.load_accounts(file_path)


@pytest.mark.parametrize("broken_acc",  [{"owner": "Oleg","balance": 500,"history": []},
                                        [{"owner": "Oleg", "balance": 500}],
                                        [1, 2 , 3],
                                        [{"owner": 200, "balance": 500, "history": []}],
                                        [{"owner": "Oleg", "balance": "500", "history": []}],
                                        [{"owner": "Oleg", "balance": True, "history": []}],
                                        [{"owner": "Oleg", "balance": 10.5, "history": []}],
                                        [{"owner": "Oleg", "balance": 500, "history": {}}],
                                        [{"owner": "Oleg", "balance": 500, "history": [200]}]])


def test_invalid_load_accounts(tmp_path, broken_acc):
    file_path = tmp_path / "accounts.json"
    with open(file_path, 'w', encoding="utf-8") as corrupted_file:
        json.dump(broken_acc, corrupted_file, ensure_ascii=False, indent=2)
    with pytest.raises(storage.CorruptedStorage):
        storage.load_accounts(file_path)
    with open(file_path, 'r', encoding="utf-8") as corrupted_file:
        check_file = json.load(corrupted_file)
    assert check_file == broken_acc

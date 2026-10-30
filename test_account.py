import account
import pytest


@pytest.fixture
def human():
    return account.Account("Name", 500)


@pytest.fixture
def human_2():
    return account.Account("Name_2", 300)


def balance_sum(human, human_2):
    bal = human.balance
    bal_2 = human_2.balance
    balance_sum = bal + bal_2
    return balance_sum


def test_deposit_valid_amount(human):
    assert human.deposit(200) == 700


def test_deposit_0(human):
    with pytest.raises(ValueError):
        human.deposit(0)
    assert human.balance == 500


def test_deposit_negative_number(human):
    with pytest.raises(ValueError):
        human.deposit(-500)
    assert human.balance == 500


def test_withdraw_valid_amount(human):
    assert human.withdraw(500) == 0


def test_withdraw_0(human):
    with pytest.raises(ValueError):
        human.withdraw(0)
    assert human.balance == 500


def test_withdraw_negative_number(human):
    with pytest.raises(ValueError):
        human.withdraw(-500)
    assert human.balance == 500


def test_withdraw_more_than_balance(human):
    with pytest.raises(account.InsufficientFunds):
        human.withdraw(1000)
    assert human.balance == 500


def test_valid_transfer(human, human_2):
    assert human.balance == 500
    assert human_2.balance == 300
    assert balance_sum(human, human_2) == 800
    human.transfer(328, human_2)
    assert human.balance == 172
    assert human_2.balance == 628
    assert balance_sum(human, human_2) == 800


def test_transfer_to_None(human):
    none_human = None
    assert human.balance == 500
    with pytest.raises(account.TransferToNone):
        human.transfer(300, none_human)
    assert human.balance == 500


def test_overbalance_transfer(human, human_2):
    with pytest.raises(account.InsufficientFunds):
        human.transfer(1000, human_2)
    assert human.balance == 500
    assert human_2.balance == 300


def test_0_transfer(human, human_2):
    with pytest.raises(ValueError):
        human.transfer(0, human_2)
    assert human.balance == 500
    assert human_2.balance == 300


def test_negative_transfer(human, human_2):
    with pytest.raises(ValueError):
        human.transfer(-500, human_2)
    assert human.balance == 500
    assert human_2.balance == 300

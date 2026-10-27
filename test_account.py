import account
import pytest


@pytest.fixture
def human():
    return account.Account("Name", 500)


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

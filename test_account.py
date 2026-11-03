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


# Deposit
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


def test_false_deposit(human):
    with pytest.raises(account.BoolAmount):
        human.deposit(False)
    assert human.balance == 500


def test_true_deposit(human):
    with pytest.raises(account.BoolAmount):
        human.deposit(True)
    assert human.balance == 500


def test_none_deposit(human):
    with pytest.raises(account.NoneAmount):
        human.deposit(None)
    assert human.balance == 500


def test_float_deposit(human):
    with pytest.raises(account.FloatAmount):
        human.deposit(10.5)
    assert human.balance == 500


def test_deposit_successful_history(human):
    assert human.deposit(200) == 700
    assert len(human.history) == 1


def test_deposit_fail_history(human):
    with pytest.raises(ValueError):
        human.deposit(0)
    assert human.balance == 500
    assert len(human.history) == 0


# Withdraw
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


def test_false_withdraw(human):
    with pytest.raises(account.BoolAmount):
        human.withdraw(False)
    assert human.balance == 500


def test_true_withdraw(human):
    with pytest.raises(account.BoolAmount):
        human.withdraw(True)
    assert human.balance == 500


def test_none_withdraw(human):
    with pytest.raises(account.NoneAmount):
        human.withdraw(None)
    assert human.balance == 500


def test_float_withdraw(human):
    with pytest.raises(account.FloatAmount):
        human.withdraw(10.5)
    assert human.balance == 500


def test_withdraw_successful_history(human):
    assert human.withdraw(300) == 200
    assert len(human.history) == 1


def test_withdraw_fail_history(human):
    with pytest.raises(account.FloatAmount):
        human.withdraw(10.5)
    assert human.balance == 500
    assert len(human.history) == 0


# Transfer
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
    with pytest.raises(account.InvalidReceiver):
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


def test_self_transfer(human):
    with pytest.raises(account.SelfTransfer):
        human.transfer(100, human)
    assert human.balance == 500


def test_string_transfer(human, human_2):
    with pytest.raises(account.InvalidReceiver):
        human.transfer(100, "human_2")
    assert human.balance == 500
    assert human_2.balance == 300


def test_number_transfer(human):
    with pytest.raises(account.InvalidReceiver):
        human.transfer(100, 2)
    assert human.balance == 500


def test_false_transfer(human, human_2):
    with pytest.raises(account.BoolAmount):
        human.transfer(False, human_2)
    assert human.balance == 500
    assert human_2.balance == 300


def test_true_transfer(human, human_2):
    with pytest.raises(account.BoolAmount):
        human.transfer(True, human_2)
    assert human.balance == 500
    assert human_2.balance == 300


def test_none_transfer(human, human_2):
    with pytest.raises(account.NoneAmount):
        human.transfer(None, human_2)
    assert human.balance == 500
    assert human_2.balance == 300


def test_float_transfer(human, human_2):
    with pytest.raises(account.FloatAmount):
        human.transfer(10.5, human_2)
    assert human.balance == 500
    assert human_2.balance == 300


def test_transfer_successful_history(human, human_2):
    assert human.balance == 500
    assert human_2.balance == 300
    assert balance_sum(human, human_2) == 800
    human.transfer(500, human_2)
    assert human.balance == 0
    assert human_2.balance == 800
    assert balance_sum(human, human_2) == 800
    assert len(human.history) == 1
    assert len(human_2.history) == 1

def test_transfer_fail_history(human, human_2):
    with pytest.raises(account.NoneAmount):
        human.transfer(None, human_2)
    assert human.balance == 500
    assert human_2.balance == 300
    assert len(human.history) == 0
    assert len(human_2.history) == 0


def test_transfer_overbalance_to_None(human):
    none_human = None
    assert human.balance == 500
    with pytest.raises(account.InvalidReceiver):
        human.transfer(1000, none_human)
    assert human.balance == 500

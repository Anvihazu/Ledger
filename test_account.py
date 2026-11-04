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
@pytest.mark.parametrize("deposit_amount,expected_err", [(0, ValueError),
                                                         (-500, ValueError),
                                                         (False, account.BoolAmount),
                                                         (True, account.BoolAmount),
                                                         (None, account.NoneAmount),
                                                         (10.5, account.FloatAmount),
                                                         ("10", TypeError)])
def test_deposit_invalid_amount(human, deposit_amount, expected_err):
    with pytest.raises(expected_err):
        human.deposit(deposit_amount)
    assert human.balance == 500
    assert len(human.history) == 0


def test_deposit_valid_amount(human):
    assert human.deposit(200) == 700
    assert len(human.history) == 1


# Withdraw
@pytest.mark.parametrize("withdraw_amount,expected_err", [(0, ValueError),
                                                          (-500, ValueError),
                                                          (False, account.BoolAmount),
                                                          (True, account.BoolAmount),
                                                          (None, account.NoneAmount),
                                                          (10.5, account.FloatAmount),
                                                          (1000, account.InsufficientFunds),
                                                          ("10", TypeError)])
def test_withdraw_invalid_amount(human, withdraw_amount, expected_err):
    with pytest.raises(expected_err):
        human.withdraw(withdraw_amount)
    assert human.balance == 500
    assert len(human.history) == 0


def test_withdraw_valid_amount(human):
    assert human.withdraw(500) == 0
    assert len(human.history) == 1


# Transfer
@pytest.mark.parametrize("transfer_amount,expected_err", [(0, ValueError),
                                                          (-500, ValueError),
                                                          (False, account.BoolAmount),
                                                          (True, account.BoolAmount),
                                                          (None, account.NoneAmount),
                                                          (10.5, account.FloatAmount),
                                                          (1000, account.InsufficientFunds),
                                                          ("10", TypeError)])
def test_invalid_transfer(human, human_2, transfer_amount, expected_err):
    with pytest.raises(expected_err):
        human.transfer(transfer_amount, human_2)
    assert human.balance == 500
    assert len(human.history) == 0
    assert human_2.balance == 300
    assert len(human_2.history) == 0


def test_valid_transfer(human, human_2):
    assert human.balance == 500
    assert human_2.balance == 300
    assert balance_sum(human, human_2) == 800
    human.transfer(328, human_2)
    assert human.balance == 172
    assert len(human.history) == 1
    assert human_2.balance == 628
    assert len(human_2.history) == 1
    assert balance_sum(human, human_2) == 800


def test_transfer_to_None(human):
    none_human = None
    assert human.balance == 500
    with pytest.raises(account.InvalidReceiver):
        human.transfer(300, none_human)
    assert human.balance == 500


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


def test_transfer_overbalance_to_None(human):
    none_human = None
    assert human.balance == 500
    with pytest.raises(account.InvalidReceiver):
        human.transfer(1000, none_human)
    assert human.balance == 500

def test_transfer_full_balance(human, human_2):
    assert human.balance == 500
    assert human_2.balance == 300
    assert balance_sum(human, human_2) == 800
    human.transfer(500, human_2)
    assert human.balance == 0
    assert human_2.balance == 800
    assert balance_sum(human, human_2) == 800
    assert len(human.history) == 1
    assert len(human_2.history) == 1

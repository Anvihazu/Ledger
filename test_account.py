import account
import pytest
import random


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
    assert balance_sum(human, human_2) == 800


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


def test_random_transfers_keep_total():
    rng = random.Random(42)
    successful_transfers = 0
    account_1 = account.Account("Name_1", 500)
    account_2 = account.Account("Name_2", 300)
    account_3 = account.Account("Name_3", 200)
    accounts = [account_1, account_2, account_3]
    for _ in range(100):
        sender = rng.choice(accounts)
        receiver = rng.choice(accounts)
        transfer_sum = rng.randint(-50, 700)
        try:
            sender.transfer(transfer_sum, receiver)
            successful_transfers += 1
        except (account.InsufficientFunds, account.SelfTransfer, ValueError):
            pass
        balance_sum = account_1.balance + account_2.balance + account_3.balance
        assert balance_sum == 1000
    assert successful_transfers > 0
    assert len(account_1.history + account_2.history + account_3.history) == successful_transfers * 2
    assert account_1.balance >= 0
    assert account_2.balance >= 0
    assert account_3.balance >= 0

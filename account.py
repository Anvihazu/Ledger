class InsufficientFunds(Exception):
    pass


class FloatAmount(Exception):
    pass


class InvalidReceiver(Exception):
    pass


class SelfTransfer(Exception):
    pass


class BoolAmount(Exception):
    pass


class NoneAmount(Exception):
    pass


class Account:
    def __init__(self, owner, balance: int = 0):
        self.owner = owner
        self.balance = balance


    def deposit(self, amount: int):
        amount_verification(amount)
        self.balance += amount
        return self.balance


    def withdraw(self, amount: int):
        amount_verification(amount)
        withdraw_verification(amount, self.balance)
        self.balance -= amount
        return self.balance


    def transfer(self, amount: int, person):
        amount_verification(amount)
        withdraw_verification(amount, self.balance)
        receiver_verification(self, person)
        self.balance -= amount
        person.balance += amount


def amount_verification(amount):
    if isinstance(amount, str):
        raise TypeError(amount)
    elif amount is None:
        raise NoneAmount
    elif amount <= 0:
        raise ValueError(amount)
    elif isinstance(amount, float):
        raise FloatAmount
    elif isinstance(amount, bool):
        raise BoolAmount
    else:
        return amount


def withdraw_verification(amount, balance):
    if amount > balance:
        raise InsufficientFunds(amount)
    else:
        return amount


def receiver_verification(person, person_2):
    if not isinstance(person_2, Account):
        raise InvalidReceiver(person_2)
    elif person is person_2:
        raise SelfTransfer


# Example:
def main():
    dmitriy = Account("Dmitriy", 1000)
    oleg = Account("Oleg", 500)
    print(f"Dmitriy's balance before: {dmitriy.balance}.")
    print(f"Oleg's balance before: {oleg.balance}.")
    try:
        dmitriy.transfer(200, None)
    except ValueError as err:
        print(f"Invalid amount! Value must be greater than 0, but you provided: {err}!")
    except InsufficientFunds as err:
        print(f"Operation failed! {err} is insufficient for withdrawal.")
    except TypeError as err:
        print(f"Type error! '{err}' is a string.")
    except FloatAmount:
        print("Amount error! The sum must be an integer.")
    except InvalidReceiver as err:
        print(f"Receiver error! '{err}' is not a valid account.")
    except BoolAmount:
        print("Amount error! Boolean values are not allowed!")
    except NoneAmount:
        print("Amount error! None value cannot be used as an amount!")
    except SelfTransfer:
        print("Transfer rejected! You cannot transfer funds to yourself.")
    print(f"Dmitriy's balance after: {dmitriy.balance}.")
    print(f"Oleg's balance after: {oleg.balance}.")


if __name__ == "__main__":
    main()

def amount_verification(amount):
    if isinstance(amount, str):
        raise TypeError(amount)
    elif amount <= 0:
        raise ValueError(amount)
    elif isinstance(amount, float):
        raise FloatNumber
    else:
        return amount


def withdraw_verification(amount, balance):
    if amount > balance:
        raise InsufficientFunds(amount)
    else:
        return amount


def transfer_to_none(person):
    if person == None:
        raise TransferToNone


class InsufficientFunds(Exception):
    pass


class FloatNumber(Exception):
    pass


class TransferToNone(Exception):
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
        transfer_to_none(person)
        self.balance -= amount
        person.balance += amount

# Example:
def main():
    dmitriy = Account("Dmitriy", 1000)
    oleg = Account("Oleg", 500)
    print(f"Баланс Дмитрия до: {dmitriy.balance}.")
    print(f"Баланс Олега до: {oleg.balance}.")
    try:
        dmitriy.transfer(200, None)
    except ValueError as err:
        print(f"Значение суммы должно быть больше 0 а у вас: {err}!")
    except InsufficientFunds as err:
        print(f"{err} - недостаточно для снятия!")
    except TypeError as err:
        print(f"{err} - является строкой!")
    except FloatNumber:
        print("Сумма должна быть целым числом!")
    except TransferToNone:
        print("Нельзя переводить никому")
    print(f"Баланс Дмитрия после: {dmitriy.balance}.")
    print(f"Баланс Олега после: {oleg.balance}.")


if __name__ == "__main__":
    main()

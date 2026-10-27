def amount_verification(amount):
    if isinstance(amount, str):
        raise TypeError(amount)
    elif amount <= 0:
        raise ValueError(amount)
    elif isinstance(amount, float):
        raise FloatNumber

class InsufficientFunds(Exception):
    pass


class FloatNumber(Exception):
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
        if amount > self.balance:
            raise InsufficientFunds(amount)
        self.balance -= amount
        return self.balance


# Tests
def main():
    dmitriy = Account("Dmitriy", 1000)
    try:
        dmitriy.withdraw(2000)
    except ValueError as err:
        print(f"Значение суммы должно быть больше 0 а у вас: {err}!")
    except InsufficientFunds as err:
        print(f"{err} - недостаточно для снятия!")
    except TypeError as err:
        print(f"{err} - является строкой!")
    except FloatNumber:
        print("Сумма должна быть целым числом!")
    print(f"Ваш баланс составляет: {dmitriy.balance}.")


if __name__ == "__main__":
    main()

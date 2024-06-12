from abc import ABC, abstractmethod
from datetime import datetime
import textwrap

class Client:
    def __init__(self, address):
        self.address = address
        self.accounts = []

    def make_transactions(self, account, transaction):
        transaction.register(account)
    
    def account_add(self, account):
        self.accounts.append(account)




class IndividualPerson(Client):
    def __init__(self, name, birth_date, cpf, adress):
        super().__init__(adress)
        self.name = name
        self.birth_date = birth_date
        self.cpf = cpf




class Account:
    def __init__(self, number, client):
        self._balance = 0
        self._number = number
        self._branch = '0001'
        self._client = client
        self._historic = Historic()

    @classmethod
    def new_account(cls, client, number):
        return cls(number, client)
    
    @property
    def balance(self):
        return self._balance
    @property
    def number(self):
        return self._number
    @property
    def branch(self):
        return self._branch
    @property
    def client(self):
        return self._client
    @property
    def historic(self):
        return self._historic

    def withdraw(self, value):
        balance = self.balance
        exceeded_balance = value > balance

        if exceeded_balance:
            print ("you don't have enough balance")
        elif value > 0:
            self._balance -= value
            print('successful withdrawal')
        else:
            print('invalid value')
        return False
    
    def deposit(self, value):
        if value > 0:
            self._balance += value
            print('deposit made successfully')
        else:
            print('invalid value')
            return False
        return True




class CheckingAccount(Account):
    def __init__(self, number, client, limit=500, withdraw_limit=3):
        super().__init__(number, client)
        self.limit = limit
        self.withdraw_limit = withdraw_limit

    def withdraw(self, value):
        withdraw_number = len(
           [transaction for transaction in self.historic.transactions if transaction["type"] == Withdraw.__name__ ]
        )
        exceeded_limit = value > self.limit
        exceeded_withdraw = withdraw_number > self.withdraw_limit

        if exceeded_limit:
            print('the withdrawal amount exceeds the limit')

        elif exceeded_withdraw:
            print('maximum number of withdrawals exceeded')

        else:
            return super().withdraw(value)
        return False
    
    def __str__(self):
        return f"""\
            brach:\t{self.branch}
            C/C:\t\t{self.number}
            Client:\t{self.client.name}
        """




class Historic:

    def __init__(self):
        self._transactions = []
    
    @property
    def transactions(self):
        return self._transactions
    
    def add_transaction(self, transaction):
        self._transactions.append(
            {
                "type": transaction.__class__.__name__,
                "value": transaction.value,
                "date": datetime.now(),
            }
        )




class Transaction(ABC):
    @property
    @abstractmethod
    def value(self):
        pass

    @abstractmethod
    def register(self, account):
        pass




class Withdraw(Transaction):
    def __init__(self, value):
        self._value = value
    
    @property
    def value(self):
        return self._value
    
    def register(self, account):
        transaction_success = account.withdraw(self.value)

        if transaction_success:
            account.historic.add_transaction(self)




class Deposit(Transaction):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value
    
    def register(self, account):
        transaction_success = account.deposit(self.value)

        if transaction_success:
            account.historic.add_transaction(self)






def menu():
    menu = """\n
    ================ MENU ================
    [1]    Deposit
    [2]    Withdraw
    [3]    Statement
    [4]    Add client
    [5]    Add accounts
    [6]    Accounts list
    [Q]    Exit
    => """
    return input(textwrap.dedent(menu))


def filter_clients(cpf, clients):
    filtered_customers = [client for client in clients if client.cpf == cpf]
    return filtered_customers[0] if filtered_customers else None

def recover_customer_account(client):
    if not client.accounts:
        print('client does not have an account')
        return
    
    # FIXME: não permite cliente escolher a conta
    return client.accounts[0]

def deposit(clients):
    cpf = input('CPF: ')
    client = filter_clients(cpf, clients)

    if not client:
        print('client not found')
        return
    
    value = float(input('enter the deposit amount: '))
    transaction = Deposit(value)

    account = recover_customer_account(client)
    if not account:
        return
    
    client.make_transactions(account, transaction)

def withdraw(clients):
    cpf = input('enter CPF: ')
    client = filter_clients(cpf, clients)

    if not client:
        print('client not found')
        return
    value = float(input('enter the value to withdraw: '))
    transaction = Withdraw(value)

    account = recover_customer_account(client)
    if not account:
        return
    
    client.make_transactions(account, transaction)

def display_statement(clients):
    cpf = input('enther the CPF: ')
    client = filter_clients(cpf, clients)

    if not client:
        print('client not found')
        return
    
    account = recover_customer_account(client)
    if not account:
        return
    
    print('----------STATEMENT----------')
    transactions = account.historic.transactions

    statement = ''
    if not transactions:
        statement = 'not found transactions'
    else:
        for transaction in transactions:
            statement += f'\n{transaction["type"]}:R${transaction["value"]:.2f}'

    print(statement)
    print(f"\nbalance:\n\tR$ {account.balance:.2f}")
    print('--------------------')

def add_client(clients):
    cpf = input('enter CPF(only numbers)')
    client = filter_clients(cpf, clients)

    if client:
        print('client alread exists')
        return
    
    name = input('name: ')
    birth_date = input('date of birth(dd-mm-aaaa): ')
    adress = input('adress: ')

    client = IndividualPerson(name=name, birth_date=birth_date, cpf=cpf, adress=adress)
    clients.append(client)

    print('Client created')

def add_account(account_number, clients, accounts):
    cpf = input('enter the CPF: ')
    client = filter_clients(cpf, clients)

    if not client:
        print('client not found')
        return
    
    account = CheckingAccount.new_account(client=client, number=account_number)
    accounts.append(account)
    client.accounts.append(account)
    
    print('created new account')

def accounts_list(accounts):
    for account in accounts:
        print('=' * 100)
        print(textwrap.dedent(str(account)))

def main():
    clients = []
    accounts = []

    while True:
        option = menu()

        if option == '1':
            deposit(clients)

        elif option == '2':
            withdraw(clients)

        elif option == "3":
            display_statement(clients)

        elif option == "4":
            add_client(clients)

        elif option == "5":
            account_number = len(accounts) + 1
            add_account(account_number, clients, accounts)

        elif option == "6":
            accounts_list(accounts)

        elif option == "q":
            break

        else:
            print("invalid option")

main()
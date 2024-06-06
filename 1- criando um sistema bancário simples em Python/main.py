from time import sleep
menu = """

[1] Deposit
[2] Withdraw
[3] Statement
[Q] Quit


"""

def reset():
    sleep(2)
    print()
    print()
    print(menu)

balance = 0
limit = 500
statement = ""
withdrawal_count = 0
WITHDRAWAL_LIMIT = 3

print(menu)

while True:
    option = input("=>Choose your option: ").lower()

    if option == '1':
        new_deposit = float(input(("Choose your deposiit: R$")))
        balance += new_deposit
        statement += f"Deposit: +R$ {new_deposit:.2f}\n"
        print(f'Your balance is now {balance:.2f}R$')
        reset()

        

    elif option == '2':
        withdrawal = float(input('Choose your withdrawal: R$'))
        if WITHDRAWAL_LIMIT == 0:
            print(f'withdrawal limit agreed. You balance is: {balance:.2f}R$')
            reset()

        elif withdrawal > limit:
            print('Your withdrawals limit is R$ 500.00')
            reset()

        elif withdrawal > balance:
            print("You don't have balance")
            print(f'You balance is: {balance:.2f}')
            reset()
        else:
            balance -= withdrawal
            statement += f"Withdrawal: -R$ {withdrawal:.2f}\n"
            WITHDRAWAL_LIMIT -= 1
            print(f'Now your balance is R$ {balance:.2f}')
            print(f'remaining withdrawals: {WITHDRAWAL_LIMIT}')
            reset()
        


    elif option == '3':
        print(f'Your statement {statement}:')
        print(f'Your balance: {balance:.2f}')
        reset()


        

    elif option == 'q':
        print("Exiting the system.")
        break
    else:
        print("Invalid option! Please choose a valid option.")
        print(menu)

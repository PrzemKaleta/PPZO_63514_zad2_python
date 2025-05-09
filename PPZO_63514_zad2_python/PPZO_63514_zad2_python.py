import datetime

class Account:
    def __init__(self, account_number, owner_name, initial_balance=0):
        self.account_number = account_number
        self.owner_name = owner_name
        self.balance = float(initial_balance)
        self.transaction_history = []

    def deposit(self, amount):
        if not isinstance(amount, (int, float)) or amount <= 0:
            print("Błąd: Kwota wpłaty musi być liczbą dodatnią")
            return False

        self.balance += amount
        transaction_obj = Transaction("wpłata", amount, "Wpłata środków")
        self.transaction_history.append(transaction_obj)
        print(f"Wpłacono {amount} PLN na konto o numerze {self.account_number}")
        print(f"Nowe saldo: {self.balance} PLN")
        return True

    def get_balance(self):
        return self.balance

class Bank:
    def __init__(self):
        self.accounts = {}
        self.next_account_number_base = 0

    def generate_account_number(self):
        self.next_account_number_base += 1
        return str(self.next_account_number_base)

    def create_account(self, owner_name, initial_deposit=0):
        account_number = self.generate_account_number()
        try:
            new_account = Account(account_number, owner_name, initial_deposit)
            self.accounts[account_number] = new_account
            
            if initial_deposit > 0:
                initial_transaction = Transaction("wpłata", initial_deposit, "Wpłata początkowa")
                new_account.transaction_history.append(initial_transaction)
            return new_account
        except ValueError as e: 
            print(f"Błąd przy tworzeniu konta: {e}")
            return None 

    def get_account(self, account_number):
        return self.accounts.get(account_number)

class Transaction:
    def __init__(self, transaction_type, amount, description=""):
        self.transaction_type = transaction_type
        self.amount = amount
        self.timestamp = datetime.datetime.now()
        self.description = description

    def __str__(self):
        return (f"{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - "
                f"{self.transaction_type.capitalize()}: {self.amount} PLN - "
                f"{self.description}")

def main():
    
    main_bank = Bank() 

    while True:
        print("\n--- MENU SYSTEMU BANKOWEGO ---")
        print("1. Utwórz nowe konto")
        print("2. Wpłać środki na konto")
        print("0. Wyjdź z systemu")

        user_choice = input("Wybierz opcję (wpisz numer od 0 do 7): ")

        if user_choice == '1':
            print("\n--- Tworzenie nowego konta ---")
            owner_name_input = input("Podaj imię i nazwisko właściciela: ")
            while True:
                try:
                    initial_balance_value = int(input("Podaj kwotę początkowej wpłaty: "))
                    if initial_balance_value < 0:
                        print("Saldo początkowe nie może być ujemne. Spróbuj ponownie")
                        continue 
                    break 
                except ValueError:
                    print("Nieprawidłowa kwota, wpisz liczbę i spróbuj ponownie")
            
            new_account_object = main_bank.create_account(owner_name_input, initial_balance_value)
            if new_account_object: 
                print("Konto zostało pomyślnie utworzone")
                print(f"  Numer konta: {new_account_object.account_number}")
                print(f"  Właściciel: {new_account_object.owner_name}")
                print(f"  Saldo: {new_account_object.balance} PLN")

        elif user_choice == '2':
            print("\n--- Wpłata środków ---")
            account_number_input = input("Podaj numer konta, na które chcesz wpłacić środki: ")
            target_account = main_bank.get_account(account_number_input)
            if target_account: 
                while True:
                    try:
                        amount_value = int(input("Podaj kwotę do wpłaty: "))
                        break 
                    except ValueError:
                        print("Nieprawidłowa kwota, wpisz liczbę i spróbuj ponownie")
                target_account.deposit(amount_value) 
            else:
                print(f"Konto o numerze {account_number_input} nie istnieje")

        elif user_choice == '0':
            break 
        
        else:
            print("Nieprawidłowa opcja, wybierz numer od 0 do 7")
        
        if user_choice != '0': 
            input("\n(Naciśnij Enter aby kontynuować...)")

if __name__ == "__main__":
    main()
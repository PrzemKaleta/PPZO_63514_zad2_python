import datetime

class Account:
    def __init__(self, account_number, owner_name, initial_balance=0):
        self.account_number = account_number
        self.owner_name = owner_name
        self.balance = float(initial_balance)
        self.transaction_history = []

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
                    print("Nieprawidłowa kwota. Wpisz liczbę. Spróbuj ponownie")
            
            new_account_object = main_bank.create_account(owner_name_input, initial_balance_value)
            if new_account_object: 
                print("Konto zostało pomyślnie utworzone")
                print(f"  Numer konta: {new_account_object.account_number}")
                print(f"  Właściciel: {new_account_object.owner_name}")
                print(f"  Saldo: {new_account_object.balance} PLN")

        elif user_choice == '0':
            break 
        
        else:
            print("Nieprawidłowa opcja. Wybierz numer od 0 do 7")
        
        if user_choice != '0': 
            input("\n(Naciśnij Enter aby kontynuować...)")

if __name__ == "__main__":
    main()
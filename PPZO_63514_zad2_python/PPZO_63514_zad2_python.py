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
        print(f"\nWpłacono {amount} PLN na konto o numerze {self.account_number}")
        print(f"Nowe saldo: {self.balance} PLN")
        return True

    def withdraw(self, amount):
        if not isinstance(amount, (int, float)) or amount <= 0:
            print("Błąd: Kwota wypłaty musi być liczbą dodatnią")
            return False

        if self.balance >= amount:
            self.balance -= amount
            transaction_obj = Transaction("wypłata", amount, "Wypłata środków")
            self.transaction_history.append(transaction_obj)
            print(f"\nWypłacono {amount} PLN z konta o numerze {self.account_number}")
            print(f"Nowe saldo: {self.balance} PLN")
            return True
        else:
            print(f"Błąd: Niewystarczające środki na koncie {self.account_number}"
                  f"Saldo: {self.balance} PLN, próba wypłaty: {amount} PLN")
            return False

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

    def transfer(self, from_account_number, to_account_number, amount_to_transfer):
        if not isinstance(amount_to_transfer, (int, float)) or amount_to_transfer <= 0:
            print("Błąd: Kwota przelewu musi być liczbą dodatnią")
            return False

        source_account = self.get_account(from_account_number)
        destination_account = self.get_account(to_account_number)

        if not source_account:
            print(f"Błąd: Konto źródłowe {from_account_number} nie istnieje")
            return False
        if not destination_account:
            print(f"Błąd: Konto docelowe {to_account_number} nie istnieje")
            return False
        if from_account_number == to_account_number:
            print("Błąd: Nie można przelać środków na to samo konto")
            return False

        if source_account.balance >= amount_to_transfer:
            source_account.balance -= amount_to_transfer
            destination_account.balance += amount_to_transfer

            outgoing_transaction = Transaction("przelew wychodzący", amount_to_transfer,
                                               f"Przelew do {destination_account.owner_name} na konto o numerze {to_account_number}")
            source_account.transaction_history.append(outgoing_transaction)

            incoming_transaction = Transaction("przelew przychodzący", amount_to_transfer,
                                               f"Przelew od {source_account.owner_name} ({from_account_number})")
            destination_account.transaction_history.append(incoming_transaction)

            print(f"\nPrzelew {amount_to_transfer} PLN z konta o numerze {from_account_number} "
                  f"na konto o numerze {to_account_number} zakończony pomyślnie")
            print(f"Nowe saldo konta {from_account_number}: {source_account.balance} PLN")
            print(f"Nowe saldo konta {to_account_number}: {destination_account.balance} PLN")
            return True
        else:
            print(f"Błąd: Niewystarczające środki na koncie {from_account_number} "
                  f"do wykonania przelewu w kwocie {amount_to_transfer} PLN")
            return False

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
        print("3. Wypłać środki z konta")
        print("4. Zrób przelew między kontami")
        print("5. Pokaż saldo konta")
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
                print("\nKonto zostało pomyślnie utworzone")
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

        elif user_choice == '3':
            print("\n--- Wypłata środków ---")
            account_number_input = input("Podaj numer konta, z którego chcesz wypłacić środki: ")
            target_account = main_bank.get_account(account_number_input)
            if target_account:
                while True:
                    try:
                        amount_value = int(input("Podaj kwotę do wypłaty: "))
                        break
                    except ValueError:
                        print("Nieprawidłowa kwota. Wpisz liczbę. Spróbuj ponownie")
                target_account.withdraw(amount_value) 
            else:
                print(f"Konto o numerze {account_number_input} nie istnieje")

        elif user_choice == '4':
            print("\n--- Przelew środków ---")
            from_account_number_input = input("Podaj numer konta, z którego chcesz zrobić przelew: ")
            to_account_number_input = input("Podaj numer konta, na które chcesz zrobić przelew: ")
            
            while True:
                try:
                    amount_value = int(input("Podaj kwotę przelewu: "))
                    break
                except ValueError:
                    print("Nieprawidłowa kwota. Wpisz liczbę. Spróbuj ponownie.")
            
            main_bank.transfer(from_account_number_input, to_account_number_input, amount_value)

        elif user_choice == '5':
            print("\n--- Sprawdzanie salda ---")
            account_number_input = input("Podaj numer konta, którego saldo chcesz sprawdzić: ")
            target_account = main_bank.get_account(account_number_input)
            if target_account:
                print(f"Saldo konta {target_account.account_number} ({target_account.owner_name}): "
                      f"{target_account.get_balance()} PLN")
            else:
                print(f"Konto o numerze {account_number_input} nie istnieje.")

        elif user_choice == '0':
            break 
        
        else:
            print("Nieprawidłowa opcja, wybierz numer od 0 do 7")

if __name__ == "__main__":
    main()
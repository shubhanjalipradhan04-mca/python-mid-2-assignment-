import json
import os
from datetime import datetime

BANK_FILE = "bank_accounts.json"

def load_accounts():
    if not os.path.exists(BANK_FILE):
        return {}
    with open(BANK_FILE, "r") as f:
        return json.load(f)

def save_accounts(accs):
    with open(BANK_FILE, "w") as f:
        json.dump(accs, f, indent=4)

def create_account():
    accs = load_accounts()
    acc_num = input("Enter new Account Number: ").strip()
    if acc_num in accs:
        print("Account already exists!")
        return

    pin = input("Set a 4-digit PIN: ").strip()
    acc_type = input("Account Type (Savings/Current): ").strip().capitalize()
    
    accs[acc_num] = {
        "pin": pin,
        "type": acc_type,
        "balance": 0.0,
        "transactions": []
    }
    save_accounts(accs)
    print("Account created successfully!")

def login():
    accs = load_accounts()
    acc_num = input("Enter Account Number: ").strip()
    pin = input("Enter PIN: ").strip()

    if acc_num in accs and accs[acc_num]["pin"] == pin:
        print("Login Successful!")
        account_menu(acc_num)
    else:
        print("Invalid Account Number or PIN.")

def account_menu(acc_num):
    while True:
        accs = load_accounts()
        acc = accs[acc_num]

        print(f"\n--- Account Menu ({acc_num}) ---")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Fund Transfer")
        print("4. Calculate Interest")
        print("5. Transaction History")
        print("6. Export History")
        print("7. Logout")
        choice = input("Select option: ").strip()

        if choice == "1":
            amt = float(input("Enter deposit amount: "))
            acc["balance"] += amt
            log_transaction(acc, "Deposit", amt)
            save_accounts(accs)
            print(f"Deposited successfully. Current Balance: ${acc['balance']:.2f}")

        elif choice == "2":
            amt = float(input("Enter withdrawal amount: "))
            if amt > acc["balance"]:
                print("Insufficient balance!")
            else:
                acc["balance"] -= amt
                log_transaction(acc, "Withdrawal", amt)
                save_accounts(accs)
                print(f"Withdrawal successful. Current Balance: ${acc['balance']:.2f}")

        elif choice == "3":
            target = input("Enter recipient Account Number: ").strip()
            if target not in accs or target == acc_num:
                print("Invalid recipient account.")
                continue
            amt = float(input("Enter transfer amount: "))
            if amt > acc["balance"]:
                print("Insufficient funds.")
            else:
                acc["balance"] -= amt
                accs[target]["balance"] += amt
                log_transaction(acc, f"Transfer to {target}", amt)
                log_transaction(accs[target], f"Transfer from {acc_num}", amt)
                save_accounts(accs)
                print("Transfer successful.")

        elif choice == "4":
            if acc["type"] == "Savings":
                rate = 0.04  # 4% annual interest rate
                interest = acc["balance"] * rate
                print(f"Estimated Annual Interest (at 4%): ${interest:.2f}")
            else:
                print("Interest is only applicable to Savings accounts.")

        elif choice == "5":
            print("\n--- Transaction History ---")
            for t in acc["transactions"]:
                print(f"[{t['timestamp']}] {t['type']}: ${t['amount']:.2f} | Balance: ${t['balance']:.2f}")

        elif choice == "6":
            filename = f"statement_{acc_num}.txt"
            with open(filename, "w") as f:
                f.write(f"Statement for Account: {acc_num}\n")
                f.write("="*40 + "\n")
                for t in acc["transactions"]:
                    f.write(f"[{t['timestamp']}] {t['type']}: ${t['amount']:.2f} | Balance: ${t['balance']:.2f}\n")
            print(f"Exported to {filename}")

        elif choice == "7":
            break

def log_transaction(acc, txn_type, amount):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    acc["transactions"].append({
        "timestamp": timestamp,
        "type": txn_type,
        "amount": amount,
        "balance": acc["balance"]
    })

def main():
    while True:
        print("\n=== Bank Account Simulation ===")
        print("1. Create New Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Select option: ").strip()

        if choice == "1":
            create_account()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Thank you❗ for using our bank system.")
            break

if __name__ == "__main__":
    main()
import json
import shutil
from datetime import datetime, timedelta

LIBRARY_FILE = "library_data.json"
BACKUP_FILE = "library_data_backup.json"
FINE_PER_DAY = 5.0  # Fine amount per overdue day

def load_data():
    try:
        with open(LIBRARY_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"books": {}, "users": {}}

def save_data(data):
    with open(LIBRARY_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_book(data):
    book_id = input("Enter Book ID: ").strip()
    if book_id in data["books"]:
        print("⚠️Book ID already exists.")
        return
    title = input("Enter Book Title: ").strip()
    author = input("Enter Author: ").strip()
    data["books"][book_id] = {"title": title, "author": author, "status": "Available", "issued_to": None, "due_date": None}
    save_data(data)
    print("✅Book added successfully.")

def issue_book(data):
    book_id = input("Enter Book ID to issue: ").strip()
    if book_id not in data["books"]:
        print("❌Book not found.")
        return
    if data["books"][book_id]["status"] == "Issued":
        print("⚠️Book is already issued.")
        return

    user_id = input("Enter User ID / Name: ").strip()
    days = 14  # Default 14 days lending period
    due_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")

    data["books"][book_id]["status"] = "Issued"
    data["books"][book_id]["issued_to"] = user_id
    data["books"][book_id]["due_date"] = due_date

    if user_id not in data["users"]:
        data["users"][user_id] = []
    data["users"][user_id].append(book_id)

    save_data(data)
    print(f"Book issued to {user_id}. Due Date: {due_date}")

def return_book(data):
    book_id = input("Enter Book ID to return: ").strip()
    if book_id not in data["books"] or data["books"][book_id]["status"] == "Available":
        print("❌Invalid Book ID or book is not currently issued.")
        return

    book = data["books"][book_id]
    due_date = datetime.strptime(book["due_date"], "%Y-%m-%d")
    today = datetime.now()

    fine = 0.0
    if today > due_date:
        overdue_days = (today - due_date).days
        fine = overdue_days * FINE_PER_DAY
        print(f"Book is OVERDUE by {overdue_days} days. Fine Amount: ${fine:.2f}")

    user_id = book["issued_to"]
    if user_id in data["users"] and book_id in data["users"][user_id]:
        data["users"][user_id].remove(book_id)

    book["status"] = "Available"
    book["issued_to"] = None
    book["due_date"] = None

    save_data(data)
    print("✅ Book returned successfully.")

def search_books(data):
    query = input("Enter Title or Author to search: ").strip().lower()
    found = False
    for b_id, details in data["books"].items():
        if query in details["title"].lower() or query in details["author"].lower():
            print(f"ID: {b_id} | Title: {details['title']} | Author: {details['author']} | Status: {details['status']}")
            found = True
    if not found:
        print("❌No matching books found.")

def display_books(data):
    print("\n--- Library Books ---")
    for b_id, details in data["books"].items():
        status_info = details["status"]
        if details["status"] == "Issued":
            status_info += f" (Issued to {details['issued_to']}, Due: {details['due_date']})"
        print(f"ID: {b_id} | Title: {details['title']} | Author: {details['author']} | Status: {status_info}")

def backup_restore_data():
    print("1. Backup Data")
    print("2. Restore Data")
    choice = input("Enter option: ").strip()
    if choice == "1":
        shutil.copy(LIBRARY_FILE, BACKUP_FILE)
        print(f"Backup created at '{BACKUP_FILE}'.")
    elif choice == "2":
        if os.path.exists(BACKUP_FILE):
            shutil.copy(BACKUP_FILE, LIBRARY_FILE)
            print("✅Data successfully restored from backup.")
        else:
            print("❌No backup file found.")

def main():
    data = load_data()
    while True:
        print("\n=== Library Management System ===")
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. Search Books")
        print("5. Display All Books")
        print("6. Backup / Restore Data")
        print("7. Exit")
        choice = input("Select an option (1-7): ").strip()

        if choice == "1":
            add_book(data)
        elif choice == "2":
            issue_book(data)
        elif choice == "3":
            return_book(data)
        elif choice == "4":
            search_books(data)
        elif choice == "5":
            display_books(data)
        elif choice == "6":
            backup_restore_data()
            data = load_data()
        elif choice == "7":
            print("⚠️Exiting Library Management System.")
            break
        else:
            print("❌Invalid selection.")

if __name__ == "__main__":
    main()
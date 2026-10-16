import os
import shutil
import hashlib
import logging

logging.basicConfig(filename="organizer.log", level=logging.INFO, format="%(asctime)s - %(message)s")

CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
    "Audio": [".mp3", ".wav", ".aac"],
    "Video": [".mp4", ".mkv", ".mov"],
    "Archives": [".zip", ".tar", ".gz", ".rar"]
}

history = []  # Stores actions for Undo feature

def categorize_files(directory):
    global history
    history.clear()
    
    if not os.path.exists(directory):
        print("Directory does not exist.")
        return

    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            ext = os.path.splitext(item)[1].lower()
            dest_folder = "Others"
            for category, exts in CATEGORIES.items():
                if ext in exts:
                    dest_folder = category
                    break

            target_dir = os.path.join(directory, dest_folder)
            os.makedirs(target_dir, exist_ok=True)
            target_path = os.path.join(target_dir, item)

            shutil.move(item_path, target_path)
            history.append((target_path, item_path))
            logging.info(f"Moved: {item_path} -> {target_path}")

    print("File categorization complete.")

def undo_last_operation():
    global history
    if not history:
        print("No operations to undo.")
        return

    for current_path, original_path in reversed(history):
        if os.path.exists(current_path):
            shutil.move(current_path, original_path)
            logging.info(f"Undone: {current_path} -> {original_path}")
    history.clear()
    print("Undo completed successfully.")

def get_file_hash(filepath):
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read(65536)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(65536)
    return hasher.hexdigest()

def find_duplicates(directory):
    hashes = {}
    duplicates = []
    for root_dir, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root_dir, filename)
            file_hash = get_file_hash(filepath)
            if file_hash in hashes:
                duplicates.append((filepath, hashes[file_hash]))
            else:
                hashes[file_hash] = filepath

    print("\n--- Duplicate Files Found ---")
    for dup, orig in duplicates:
        print(f"Duplicate: {dup} | Original: {orig}")
    return duplicates

def batch_rename(directory, prefix):
    count = 1
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            ext = os.path.splitext(filename)[1]
            new_name = f"{prefix}_{count}{ext}"
            new_path = os.path.join(directory, new_name)
            os.rename(filepath, new_path)
            logging.info(f"Renamed: {filepath} -> {new_path}")
            count += 1
    print(f"Renamed {count-1} files successfully.")

def main():
    while True:
        print("\n=== File Organizer Tool ===")
        print("1. Organize Files by Category")
        print("2. Find Duplicate Files")
        print("3. Batch Rename Files")
        print("4. Undo Last Organization")
        print("5. Exit")
        choice = input("Select option: ").strip()

        if choice == "1":
            folder = input("Enter directory path to organize: ").strip()
            categorize_files(folder)
        elif choice == "2":
            folder = input("Enter directory path to check duplicates: ").strip()
            find_duplicates(folder)
        elif choice == "3":
            folder = input("Enter directory path: ").strip()
            prefix = input("Enter filename prefix: ").strip()
            batch_rename(folder, prefix)
        elif choice == "4":
            undo_last_operation()
        elif choice == "5":
            break

if __name__ == "__main__":
    main()
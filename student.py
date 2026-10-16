import csv

# Added "Marks" to the fields list
FIELDS = ["RollNo", "FullName", "Age", "Email", "Phone", "Marks"]
DATABASE_FILE = "students.csv"


def show_menu():
    print("\n==============================")
    print("   Student Management Portal   ")
    print("==============================")
    print("1. Register New Student")
    print("2. Display All Students (with Sorting)")
    print("3. Find Student")
    print("4. Modify Student")
    print("5. Remove Student")
    print("6. Generate Performance Reports")  # Added right after Remove Student
    print("7. Exit")                           # Reassigned to 7
    print("==============================\n")


def register_student():
    print("\n--- Register New Student ---")
    student_info = {}
    for field in FIELDS:
        student_info[field] = input(f"Enter {field}: ")

    with open(DATABASE_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(student_info)

    print("✅ Student registered successfully!")


def display_students():
    try:
        with open(DATABASE_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            students = list(reader)

            if not students:
                print("⚠️ No student data found.")
                return

            print("\nSelect Display Order:")
            print("1. Default (As Registered)")
            print("2. Sort by Name (A-Z)")
            print("3. Sort by Marks (Highest to Lowest)")
            sort_choice = input("Enter choice (1-3): ")

            if sort_choice == "2":
                # Sort alphabetically by FullName (case-insensitive)
                students.sort(key=lambda x: x.get("FullName", "").lower())
                print("\n--- Student Records (Sorted by Name) ---")
            elif sort_choice == "3":
                # Sort numerically by Marks. Empty/invalid entries default to 0.
                students.sort(
                    key=lambda x: float(x.get("Marks", 0) or 0), reverse=True
                )
                print("\n--- Student Records (Sorted by Marks: Highest First) ---")
            else:
                print("\n--- Student Records (Default Order) ---")

            for student in students:
                print(" | ".join([f"{k}: {v}" for k, v in student.items()]))

    except FileNotFoundError:
        print("⚠️ No records found. Please register a student first.")


def find_student():
    roll = input("Enter Roll Number to search: ")
    found = False

    try:
        with open(DATABASE_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for student in reader:
                if student["RollNo"] == roll:
                    print("\n✅ Student Found:")
                    for key, value in student.items():
                        print(f"{key}: {value}")
                    found = True
                    break
    except FileNotFoundError:
        pass

    if not found:
        print("❌ Student not found.")


def modify_student():
    roll = input("Enter Roll Number to update: ")
    updated_records = []
    modified = False

    try:
        with open(DATABASE_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for student in reader:
                if student["RollNo"] == roll:
                    print("Enter new details (leave blank to keep existing):")
                    for field in FIELDS:
                        # Fallback to an empty string if a field is missing from old records
                        current_val = student.get(field, "")
                        new_value = input(f"{field} ({current_val}): ")
                        if new_value.strip():
                            student[field] = new_value
                        else:
                            student[field] = current_val
                    modified = True
                updated_records.append(student)

        if modified:
            with open(DATABASE_FILE, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(updated_records)
            print("✅ Student details updated successfully!")
        else:
            print("❌ Student not found.")

    except FileNotFoundError:
        print("⚠️ No data available to update.")


def remove_student():
    roll = input("Enter Roll Number to delete: ")
    updated_records = []
    deleted = False

    try:
        with open(DATABASE_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for student in reader:
                if student["RollNo"] != roll:
                    updated_records.append(student)
                else:
                    deleted = True

        if deleted:
            with open(DATABASE_FILE, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(updated_records)
            print(f"✅ Student with Roll No. {roll} deleted successfully.")
        else:
            print("❌ Student not found.")

    except FileNotFoundError:
        print("⚠️ No data available to delete.")


def generate_reports():
    """Independent function to calculate class analytics and toppers."""
    print("\n--- Performance Reports ---")
    try:
        with open(DATABASE_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            students = list(reader)

            if not students:
                print("⚠️ No student records available to evaluate.")
                return

            valid_marks = []
            toppers = []
            max_marks = -1.0

            for student in students:
                try:
                    # Parse numerical score securely
                    mark_val = float(student.get("Marks", 0) or 0)
                    valid_marks.append(mark_val)

                    # Tracking mechanism for single or tied top-scorers
                    if mark_val > max_marks:
                        max_marks = mark_val
                        toppers = [student]
                    elif mark_val == max_marks:
                        toppers.append(student)
                except ValueError:
                    continue

            if not valid_marks:
                print("⚠️ No valid numeric marks found in the file.")
                return

            average_marks = sum(valid_marks) / len(valid_marks)

            print(f"📊 Total Students Checked: {len(valid_marks)}")
            print(f"📈 Class Average Marks: {average_marks:.2f}")
            print(f"👑 Highest Score Achieved: {max_marks}")
            print("\n🏆 Class Topper(s):")
            for topper in toppers:
                print(
                    f"   - {topper['FullName']} (Roll No: {topper['RollNo']}) -> Marks: {topper['Marks']}"
                )

    except FileNotFoundError:
        print("⚠️ No records found. Please register students first.")


if __name__ == "__main__":
    while True:
        show_menu()
        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            register_student()
        elif choice == "2":
            display_students()
        elif choice == "3":
            find_student()
        elif choice == "4":
            modify_student()
        elif choice == "5":
            remove_student()
        elif choice == "6":
            generate_reports()
        elif choice == "7":
            print("\n👋 Thank you for using the Student Management Portal. Goodbye!")
            break
        else:
            print("⚠️ Invalid choice, please try again.")

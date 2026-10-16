import tkinter as tk
from tkinter import messagebox
import random
import json
import os
import time

QUIZ_DATA = {
    "Python": [
        {"q": "What is the output of print(2 ** 3)?", "options": ["6", "8", "9", "5"], "ans": "8"},
        {"q": "Which keyword is used for functions in Python?", "options": ["func", "define", "def", "function"], "ans": "def"},
        {"q": "Is Python dynamically typed?", "options": ["Yes", "No", "Depends", "None"], "ans": "Yes"}
    ],
    "General Knowledge": [
        {"q": "What is the capital of France?", "options": ["Berlin", "Madrid", "Paris", "Rome"], "ans": "Paris"},
        {"q": "Which element has atomic symbol 'O'?", "options": ["Gold", "Oxygen", "Osmium", "Silver"], "ans": "Oxygen"}
    ]
}

LEADERBOARD_FILE = "leaderboard.json"

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Application")
        self.root.geometry("500x400")

        self.score = 0
        self.current_q_idx = 0
        self.time_left = 10  # 10 seconds per question
        self.questions = []
        self.timer_job = None

        self.setup_menu()

    def setup_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Select Quiz Category", font=("Arial", 16, "bold")).pack(pady=20)

        for category in QUIZ_DATA.keys():
            btn = tk.Button(self.root, text=category, font=("Arial", 12), width=20,
                            command=lambda cat=category: self.start_quiz(cat))
            btn.pack(pady=5)

        tk.Button(self.root, text="View Leaderboard", font=("Arial", 10), command=self.show_leaderboard).pack(pady=20)

    def start_quiz(self, category):
        self.questions = QUIZ_DATA[category][:]
        random.shuffle(self.questions)
        self.score = 0
        self.current_q_idx = 0
        self.user_name = tk.simpledialog.askstring("Name", "Enter your name:") or "Anonymous"
        self.display_question()

    def display_question(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        if self.current_q_idx >= len(self.questions):
            self.end_quiz()
            return

        q_data = self.questions[self.current_q_idx]

        self.time_left = 10
        self.timer_label = tk.Label(self.root, text=f"Time Left: {self.time_left}s", font=("Arial", 12), fg="red")
        self.timer_label.pack(anchor="ne", padx=10, pady=5)

        tk.Label(self.root, text=f"Q{self.current_q_idx+1}: {q_data['q']}", font=("Arial", 12, "bold"), wraplength=450).pack(pady=15)

        self.selected_var = tk.StringVar(value="")
        for opt in q_data["options"]:
            rb = tk.Radiobutton(self.root, text=opt, variable=self.selected_var, value=opt, font=("Arial", 11))
            rb.pack(anchor="w", padx=50, pady=2)

        tk.Button(self.root, text="Submit Answer", font=("Arial", 11), command=self.check_answer).pack(pady=20)

        self.update_timer()

    def update_timer(self):
        if self.time_left > 0:
            self.timer_label.config(text=f"Time Left: {self.time_left}s")
            self.time_left -= 1
            self.timer_job = self.root.after(1000, self.update_timer)
        else:
            messagebox.showinfo("Time Out!", "Time is up for this question!")
            self.score -= 1  # Penalty for timeout / wrong
            self.next_question()

    def check_answer(self):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)

        selected = self.selected_var.get()
        correct = self.questions[self.current_q_idx]["ans"]

        if selected == correct:
            self.score += 4  # Positive marking
        else:
            self.score -= 1  # Negative marking scheme

        self.next_question()

    def next_question(self):
        self.current_q_idx += 1
        self.display_question()

    def end_quiz(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Quiz Completed!", font=("Arial", 18, "bold")).pack(pady=20)
        tk.Label(self.root, text=f"Final Score: {self.score}", font=("Arial", 14)).pack(pady=10)

        self.save_score()

        tk.Button(self.root, text="Main Menu", command=self.setup_menu).pack(pady=10)

    def save_score(self):
        leaderboard = []
        if os.path.exists(LEADERBOARD_FILE):
            with open(LEADERBOARD_FILE, "r") as f:
                leaderboard = json.load(f)

        leaderboard.append({"name": self.user_name, "score": self.score})
        leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]

        with open(LEADERBOARD_FILE, "w") as f:
            json.dump(leaderboard, f, indent=4)

    def show_leaderboard(self):
        if not os.path.exists(LEADERBOARD_FILE):
            messagebox.showinfo("Leaderboard", "⚠️ No scores recorded yet.")
            return

        with open(LEADERBOARD_FILE, "r") as f:
            lb = json.load(f)

        text = "\n".join([f"{i+1}. {entry['name']} - {entry['score']} pts" for i, entry in enumerate(lb)])
        messagebox.showinfo("Top Scores", text)

if __name__ == "__main__":
    from tkinter import simpledialog
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
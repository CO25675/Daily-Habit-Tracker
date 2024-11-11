import tkinter as tk
from tkinter import messagebox, Toplevel

# Dictionary to store habits
habits = {}

# Function to create the main application window
def create_main_window():
    main_window = tk.Tk()
    main_window.title("Daily Habit Tracker")
    main_window.geometry("400x300")

    # Title Label
    tk.Label(main_window, text="Daily Habit Tracker", font=("Arial", 16)).pack(pady=10)

    # Navigation Buttons
    tk.Button(main_window, text="Add Habit", command=open_add_habit_window).pack(pady=5)
    tk.Button(main_window, text="View Progress", command=open_progress_window).pack(pady=5)
    tk.Button(main_window, text="Settings", command=open_settings_window).pack(pady=5)
    tk.Button(main_window, text="Exit", command=main_window.quit).pack(pady=20)

    main_window.mainloop()

# Function to open the Add Habit Window
def open_add_habit_window():
    add_habit_window = Toplevel()
    add_habit_window.title("Add New Habit")
    add_habit_window.geometry("300x200")

    # Habit Name Entry
    tk.Label(add_habit_window, text="Habit Name:").pack(pady=5)
    habit_name_entry = tk.Entry(add_habit_window)
    habit_name_entry.pack(pady=5)

    # Frequency Entry (times per week)
    tk.Label(add_habit_window, text="Frequency (times per week):").pack(pady=5)
    frequency_entry = tk.Entry(add_habit_window)
    frequency_entry.pack(pady=5)

    # Save Habit Button
    tk.Button(add_habit_window, text="Save Habit",
              command=lambda: save_habit(habit_name_entry.get(), frequency_entry.get())).pack(pady=10)

# Function to save the habit with basic validation
def save_habit(habit_name, frequency):
    if not habit_name.strip():
        messagebox.showwarning("Input Error", "Please enter a habit name.")
        return
    try:
        frequency = int(frequency)
        habits[habit_name] = {"frequency": frequency, "dates": []}
        messagebox.showinfo("Success", f"Habit '{habit_name}' added successfully.")
    except ValueError:
        messagebox.showwarning("Input Error", "Please enter a valid number for frequency.")

# Function to open the View Progress Window
def open_progress_window():
    progress_window = Toplevel()
    progress_window.title("View Progress")
    progress_window.geometry("300x250")

    # Display each habit and its progress
    tk.Label(progress_window, text="Weekly Progress", font=("Arial", 14)).pack(pady=10)
    for habit_name, details in habits.items():
        tk.Label(progress_window, text=f"{habit_name} - {details['frequency']} times/week").pack()
        progress = len(details["dates"])
        tk.Label(progress_window, text=f"Completed {progress} times this week").pack()

# Function to open the Settings Window
def open_settings_window():
    settings_window = Toplevel()
    settings_window.title("Settings")
    settings_window.geometry("300x200")

    tk.Label(settings_window, text="Settings", font=("Arial", 14)).pack(pady=10)

    # Placeholder settings options (e.g., reminders)
    tk.Label(settings_window, text="Reminder Settings:").pack(pady=5)
    tk.Entry(settings_window).pack(pady=5)

    tk.Label(settings_window, text="Notification Preferences:").pack(pady=5)
    tk.Entry(settings_window).pack(pady=5)

# Run the main application
if __name__ == "__main__":
    create_main_window()
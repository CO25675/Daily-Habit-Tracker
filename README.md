import tkinter as tk
from tkinter import messagebox, Toplevel
import json
import os

# Constants
BACKGROUND_COLOR = "#1e1e2f"  # Background color for the application window
TEXT_COLOR = "#00d1b2"        # Text color used for all text labels
BUTTON_COLOR = "#29293d"      # Button background color
BUTTON_TEXT_COLOR = "#ffffff" # Text color for buttons
DATA_FILE = "habits_data.json"  # File name to store habit data
SETTINGS_FILE = "settings_data.json"  # File name to store settings data

# Global dictionaries to store habits and settings
habits = {}  # Dictionary to store habits with their frequency and completed days
settings = {  # Dictionary to store user settings like reminder state and notification frequency
    "reminder_enabled": False,
    "notification_frequency": "daily",
}

# Load habits from file if it exists
def load_habits():
    """
    Purpose: Load habit data from a JSON file to maintain persistence across app runs.
    
    This function attempts to read from the habits data file and load its contents into
    the global 'habits' dictionary. If the file does not exist or cannot be read, it will
    initialize an empty dictionary.
    """
    global habits
    try:
        with open(DATA_FILE, "r") as file:  # Open the habit data file
            habits = json.load(file)  # Load the habit data from the file into the habits dictionary
    except (FileNotFoundError, json.JSONDecodeError):  # Handle the case where file is missing or corrupt
        habits = {}  # Initialize an empty dictionary if the file doesn't exist or is invalid

# Save habits to file
def save_habits():
    """
    Purpose: Save the current habit data to a JSON file to persist changes.
    
    This function writes the global 'habits' dictionary to a file so that the habit data
    remains between app sessions.
    """
    with open(DATA_FILE, "w") as file:  # Open the habits data file for writing
        json.dump(habits, file, indent=4)  # Save the habits dictionary to the file with nice formatting

# Load settings from a file if it exists
def load_settings():
    """
    Purpose: Load user settings from a JSON file to restore previous preferences.
    
    This function attempts to read from the settings data file and load it into the global
    'settings' dictionary. If the file is missing or corrupt, it will initialize default settings.
    """
    global settings
    try:
        with open(SETTINGS_FILE, "r") as file:  # Open the settings data file
            settings = json.load(file)  # Load the settings data into the settings dictionary
    except (FileNotFoundError, json.JSONDecodeError):  # Handle missing or corrupt file
        settings = {"reminder_enabled": False, "notification_frequency": "daily"}  # Initialize default settings

# Save settings to a file
def save_settings():
    """
    Purpose: Save the current settings to a JSON file.
    
    This function writes the global 'settings' dictionary to a file, ensuring the app retains
    the user's preferences between sessions.
    """
    with open(SETTINGS_FILE, "w") as file:  # Open the settings file for writing
        json.dump(settings, file, indent=4)  # Save the settings dictionary to the file

# Function to create a styled button
def create_button(parent, text, command, width=20):
    """
    Purpose: Create a styled button that matches the application's visual theme.
    
    This function generates a Tkinter Button with specific font, colors, and dimensions.
    The button is linked to a command that is executed when clicked.
    """
    button = tk.Button(
        parent,  # Parent window to place the button in
        text=text,  # Text label on the button
        command=command,  # The callback function to be executed when the button is clicked
        font=("Helvetica", 12),  # Font style for the text on the button
        bg=BUTTON_COLOR,  # Background color of the button
        fg=BUTTON_TEXT_COLOR,  # Text color on the button
        activebackground=BUTTON_COLOR,  # Background color when the button is pressed
        activeforeground=TEXT_COLOR,  # Text color when the button is pressed
        relief="flat",  # Flat style (no border)
        width=width,  # Width of the button (number of characters)
    )
    add_hover_effects(button, TEXT_COLOR, BUTTON_COLOR)  # Add hover effects to the button
    return button

# Add hover effects to a button
def add_hover_effects(button, hover_bg, hover_fg):
    """
    Purpose: Add hover effects to a button, changing its appearance when the mouse enters or leaves.
    
    This function makes the button change color when hovered over to provide feedback to the user.
    """
    def on_enter(e):
        button["bg"] = hover_bg  # Change background color on mouse enter
        button["fg"] = hover_fg  # Change text color on mouse enter

    def on_leave(e):
        button["bg"] = BUTTON_COLOR  # Reset background color on mouse leave
        button["fg"] = BUTTON_TEXT_COLOR  # Reset text color on mouse leave

    button.bind("<Enter>", on_enter)  # Bind the "Enter" event to the on_enter function
    button.bind("<Leave>", on_leave)  # Bind the "Leave" event to the on_leave function

# Create the main application window
def create_main_window():
    """
    Purpose: Create the main application window and display the buttons for navigation.
    
    This function sets up the main window where the user interacts with the app, including 
    navigation buttons to add habits, view progress, and access settings.
    """
    main_window = tk.Tk()  # Create the main window
    main_window.title("Daily Habit Tracker")  # Set the window title
    main_window.geometry("600x400")  # Set the window size
    main_window.config(bg=BACKGROUND_COLOR)  # Set the background color of the window

    # Title Label
    tk.Label(
        main_window,
        text="Daily Habit Tracker",  # Title text
        font=("Helvetica", 20, "bold"),  # Font style and size for the title
        bg=BACKGROUND_COLOR,  # Background color of the label
        fg=TEXT_COLOR,  # Text color of the label
    ).pack(pady=20)  # Pack the label with padding on the y-axis

    # Navigation Buttons
    create_button(main_window, "Add Habit", open_add_habit_window).pack(pady=10)  # Add Habit button
    create_button(main_window, "View Progress", open_progress_window).pack(pady=10)  # View Progress button
    create_button(main_window, "Settings", open_settings_window).pack(pady=10)  # Settings button
    create_button(main_window, "Exit", main_window.quit).pack(pady=20)  # Exit button

    # Load saved habits and settings
    load_habits()  # Load habits from file
    load_settings()  # Load settings from file
    main_window.mainloop()  # Start the Tkinter event loop

# Open the Add Habit window
def open_add_habit_window():
    """
    Purpose: Open a window to add a new habit to the tracker.
    
    This function creates a new window with input fields to enter the habit's name and frequency,
    and provides a button to save the habit.
    """
    add_habit_window = Toplevel()  # Create a new top-level window
    add_habit_window.title("Add New Habit")  # Set window title
    add_habit_window.geometry("400x300")  # Set window size
    add_habit_window.config(bg=BACKGROUND_COLOR)  # Set window background color

    # Habit Name Entry
    tk.Label(
        add_habit_window, text="Habit Name:", font=("Helvetica", 12), bg=BACKGROUND_COLOR, fg=TEXT_COLOR
    ).pack(pady=10)  # Label for habit name entry
    habit_name_entry = tk.Entry(add_habit_window, font=("Helvetica", 12))  # Entry widget for habit name
    habit_name_entry.pack(pady=5)  # Pack the entry widget

    # Frequency Entry
    tk.Label(
        add_habit_window, text="Frequency (1-7 times per week):", font=("Helvetica", 12), bg=BACKGROUND_COLOR, fg=TEXT_COLOR
    ).pack(pady=10)  # Label for frequency entry
    frequency_entry = tk.Entry(add_habit_window, font=("Helvetica", 12))  # Entry widget for frequency
    frequency_entry.pack(pady=5)  # Pack the entry widget

    # Save Habit Button
    create_button(
        add_habit_window,
        "Save Habit",
        lambda: save_habit(habit_name_entry.get(), frequency_entry.get(), add_habit_window),
    ).pack(pady=20)  # Save button to save the entered habit

# Save the habit with validation
def save_habit(habit_name, frequency, window):
    """
    Purpose: Save the new habit after validating the input fields.
    
    This function checks if the habit name is non-empty and the frequency is a valid number
    between 1 and 7, and then saves the habit to the global 'habits' dictionary.
    """
    if not habit_name.strip():  # Check if habit name is empty
        messagebox.showwarning("Input Error", "Please enter a habit name.")  # Show error message
        return
    try:
        frequency = int(frequency)  # Try to convert frequency to an integer
        if 1 <= frequency <= 7:  # Check if frequency is between 1 and 7
            habits[habit_name] = {"frequency": frequency, "completed": []}  # Add habit to the dictionary
            save_habits()  # Save the updated habits dictionary to file
            messagebox.showinfo("Success", f"Habit '{habit_name}' added successfully.")  # Show success message
            window.destroy()  # Close the add habit window
        else:
            messagebox.showwarning("Input Error", "Frequency must be between 1 and 7.")  # Show error message
    except ValueError:  # If the frequency is not a valid number
        messagebox.showwarning("Input Error", "Please enter a valid number for frequency.")  # Show error message

# Open the View Progress window
def open_progress_window():
    """
    Purpose: Open a window to display the progress of all habits.
    
    This function generates a window showing all stored habits and the progress made in completing them.
    """
    progress_window = Toplevel()  # Create a new top-level window
    progress_window.title("View Progress")  # Set window title
    progress_window.geometry("400x300")  # Set window size
    progress_window.config(bg=BACKGROUND_COLOR)  # Set window background color

    tk.Label(
        progress_window, text="Weekly Progress", font=("Helvetica", 16), bg=BACKGROUND_COLOR, fg=TEXT_COLOR
    ).pack(pady=20)  # Label showing the title "Weekly Progress"

    # Display habits and their progress
    for habit_name, details in habits.items():
        progress_label = f"{habit_name}: {len(details['completed'])}/{details['frequency']} completed"  # Progress text
        tk.Label(
            progress_window, text=progress_label, font=("Helvetica", 12), bg=BACKGROUND_COLOR, fg=TEXT_COLOR
        ).pack()  # Display progress label for each habit

# Open the Settings window
def open_settings_window():
    """
    Purpose: Open the settings window to allow users to configure app preferences.
    
    This function provides a window where users can toggle daily reminders and select the frequency
    for receiving notifications.
    """
    settings_window = Toplevel()  # Create a new top-level window
    settings_window.title("Settings")  # Set window title
    settings_window.geometry("400x300")  # Set window size
    settings_window.config(bg=BACKGROUND_COLOR)  # Set window background color

    tk.Label(
        settings_window, text="Settings", font=("Helvetica", 16), bg=BACKGROUND_COLOR, fg=TEXT_COLOR
    ).pack(pady=20)  # Label showing "Settings"

    # Reminder Settings
    reminder_var = tk.BooleanVar(value=settings["reminder_enabled"])  # Boolean variable for reminders
    tk.Checkbutton(
        settings_window,
        text="Enable Daily Reminders",
        variable=reminder_var,
        bg=BACKGROUND_COLOR,
        fg=TEXT_COLOR,
        font=("Helvetica", 12),
        selectcolor=BUTTON_COLOR,
    ).pack

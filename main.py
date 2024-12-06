import os
import subprocess
from tkinter import Tk, messagebox, Button, Label, Frame

# Define suspicious file characteristics
SUSPICIOUS_FILE_NAMES = ['log', 'keylogger', 'password', 'suspicious', 'test']
SUSPICIOUS_EXTENSIONS = ['.exe', '.bat', '.txt', '.log']
SUSPICIOUS_SIZE_THRESHOLD = 100 * 1024  # Files larger than 100 KB might be suspicious


def is_suspicious_file(file_path):
    """Checks if the given file is suspicious based on its name, extension, and size."""
    try:
        # Check if the file is suspicious by name and extension first
        if any(suspicious_name in os.path.basename(file_path).lower() for suspicious_name in SUSPICIOUS_FILE_NAMES):
            return True
        if any(file_path.lower().endswith(ext) for ext in SUSPICIOUS_EXTENSIONS):
            return True

        # Check the file size
        if os.path.getsize(file_path) > SUSPICIOUS_SIZE_THRESHOLD:
            return True
    except OSError:
        # Handle the error when file properties cannot be accessed (e.g., permission issues)
        print(f"Could not access file size for: {file_path}")
    return False


def show_warning(file_paths):
    """Displays a single warning window with options to go through each suspicious file."""
    root = Tk()
    root.title("Suspicious Files Detected")
    root.geometry("400x300")

    current_index = 0  # To track which file is currently displayed

    def show_next_file():
        """Displays the next suspicious file details."""
        nonlocal current_index
        if current_index < len(file_paths) - 1:
            current_index += 1
            update_file_info()

    def show_previous_file():
        """Displays the previous suspicious file details."""
        nonlocal current_index
        if current_index > 0:
            current_index -= 1
            update_file_info()

    def open_file_location():
        """Opens the file explorer and highlights the current file."""
        subprocess.run(['explorer', '/select,', file_paths[current_index]])

    def delete_file():
        """Deletes the current suspicious file after user confirmation."""
        nonlocal current_index
        try:
            os.remove(file_paths[current_index])
            messagebox.showinfo("File Deleted",
                                f"The file '{os.path.basename(file_paths[current_index])}' has been deleted.")
            # Remove the file from the list
            file_paths.pop(current_index)
            if file_paths:
                # Adjust index to stay within bounds
                current_index = min(current_index, len(file_paths) - 1)
                update_file_info()
            else:
                # No files left, close the application
                messagebox.showinfo("All Files Deleted", "No more suspicious files remaining.")
                root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete the file: {e}")

    def update_file_info():
        """Updates the UI to show the current file's details."""
        file_label.config(text=f"Suspicious file detected: {os.path.basename(file_paths[current_index])}")

    # Show the total number of suspicious files
    messagebox.showinfo("Suspicious Files Detected", f"Found {len(file_paths)} suspicious file(s).")

    # UI elements
    file_label = Label(root, text="", wraplength=350)
    file_label.pack(pady=10)

    button_frame = Frame(root)
    button_frame.pack(pady=5)

    prev_button = Button(button_frame, text="Previous", command=show_previous_file)
    prev_button.pack(side="left", padx=5)

    next_button = Button(button_frame, text="Next", command=show_next_file)
    next_button.pack(side="left", padx=5)

    go_button = Button(root, text="Go to File Location", command=open_file_location)
    go_button.pack(pady=5)

    delete_button = Button(root, text="Delete File", command=delete_file)
    delete_button.pack(pady=5)

    # Display the first file's details initially
    update_file_info()

    root.mainloop()


# Specify the path to the folder to scan for suspicious files
folder_path = r"D:\COLLEGE\test"
suspicious_files = []

for dirpath, dirnames, filenames in os.walk(folder_path):
    for filename in filenames:
        file_path = os.path.join(dirpath, filename)
        print(f"Scanning: {file_path}")  # Log the currently scanned file
        if is_suspicious_file(file_path):
            suspicious_files.append(file_path)

if suspicious_files:
    show_warning(suspicious_files)
else:
    print("No suspicious files found.")

import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

class FileToolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer Tool")

        self.operation_var = tk.StringVar()
        self.operation_var.set("Organizer")

        self.base_name_var = tk.StringVar()
        self.base_name_var.set("new_name")

        self.start_number_var = tk.StringVar()
        self.start_number_var.set("1")

        self.change_formats_var = tk.BooleanVar()
        self.change_formats_var.set(False)

        self.new_format_var = tk.StringVar()
        self.new_format_var.set(".txt")

        self.create_widgets()

    def create_widgets(self):
        # Operation Selection
        operation_label = tk.Label(self.root, text="Select Operation:")
        operation_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        operation_menu = tk.OptionMenu(self.root, self.operation_var, "Organizer", "Deorganizer", "Renamer")
        operation_menu.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        # Base Name Entry
        base_name_label = tk.Label(self.root, text="Base Name:")
        base_name_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        base_name_entry = tk.Entry(self.root, textvariable=self.base_name_var)
        base_name_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

        # Start Number Entry
        start_number_label = tk.Label(self.root, text="Start Number:")
        start_number_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

        start_number_entry = tk.Entry(self.root, textvariable=self.start_number_var)
        start_number_entry.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

        # Change Formats Checkbox
        change_formats_checkbox = tk.Checkbutton(self.root, text="Change Formats", variable=self.change_formats_var, command=self.toggle_new_format_entry)
        change_formats_checkbox.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)

        # New Format Entry
        new_format_label = tk.Label(self.root, text="New Format:")
        new_format_label.grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)

        self.new_format_entry = tk.Entry(self.root, textvariable=self.new_format_var, state=tk.DISABLED)
        self.new_format_entry.grid(row=4, column=1, padx=10, pady=10, sticky=tk.W)

        # Browse Button
        browse_button = tk.Button(self.root, text="Browse Folder", command=self.browse_folder)
        browse_button.grid(row=5, column=0, columnspan=2, pady=20)

        # Execute Button
        execute_button = tk.Button(self.root, text="Execute Operation", command=self.execute_operation)
        execute_button.grid(row=6, column=0, columnspan=2, pady=20)

    def toggle_new_format_entry(self):
        if self.change_formats_var.get():
            self.new_format_entry.config(state=tk.NORMAL)
        else:
            self.new_format_entry.config(state=tk.DISABLED)

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_path = folder_path

    def execute_operation(self):
        operation = self.operation_var.get()
        base_name = self.base_name_var.get()
        start_number = int(self.start_number_var.get())
        change_formats = self.change_formats_var.get()
        new_format = self.new_format_var.get() if change_formats else None

        if hasattr(self, 'folder_path'):
            if operation == "Organizer":
                self.organize_files(self.folder_path)
            elif operation == "Deorganizer":
                self.flatten_folders(self.folder_path)
            elif operation == "Renamer":
                self.rename_files(self.folder_path, base_name, start_number, change_formats, new_format)
            messagebox.showinfo("Success", f"{operation} operation successful on {self.folder_path} folder.")
        else:
            messagebox.showinfo("Error", "Please browse a folder before executing the operation.")

    def organize_files(self, source_folder):
        # ... (code from the organizer script)
        # Get a list of all files in the source folder
        files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]

        # Organize files based on their formats
        for file in files:
            # Get the file extension (format)
            _, file_extension = os.path.splitext(file)

            # Create a folder for the format if it doesn't exist
            format_folder = os.path.join(source_folder, file_extension[1:].upper())
            os.makedirs(format_folder, exist_ok=True)

            # Move the file to the corresponding format folder
            source_path = os.path.join(source_folder, file)
            destination_path = os.path.join(format_folder, file)
            shutil.move(source_path, destination_path)
            print(f"Moved '{file}' to '{format_folder}'.")

    def flatten_folders(self, source_folder):
        # ... (code from the deorganizer script)
        # Get a list of all files in the source folder and its subfolders
        all_files = []
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                all_files.append(os.path.join(root, file))

        # Move all files to the parent folder
        for file_path in all_files:
            file_name = os.path.basename(file_path)
            destination_path = os.path.join(source_folder, file_name)

            # Handle name conflicts by adding a number to the file name
            counter = 1
            while os.path.exists(destination_path):
                base_name, extension = os.path.splitext(file_name)
                new_name = f"{base_name}_{counter}{extension}"
                destination_path = os.path.join(source_folder, new_name)
                counter += 1

            shutil.move(file_path, destination_path)
            print(f"Moved '{file_name}' to '{source_folder}'.")

        # Delete empty subfolders
        for root, dirs, _ in os.walk(source_folder, topdown=False):
            for folder in dirs:
                folder_path = os.path.join(root, folder)
                if not os.listdir(folder_path):  # Check if the folder is empty
                    os.rmdir(folder_path)
                    print(f"Deleted empty folder '{folder_path}'.")

    def rename_files(self, source_folder, base_name, start_number, change_formats, new_format):
        # ... (code from the renamer script)
        # Get a list of all files in the source folder
        files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]

        # Rename files
        for i, file_name in enumerate(files, start=start_number):
            _, old_format = os.path.splitext(file_name)

            new_name = f"{base_name}_{i}{new_format}" if change_formats else f"{base_name}_{i}{old_format}"
            source_path = os.path.join(source_folder, file_name)
            destination_path = os.path.join(source_folder, new_name)

            os.rename(source_path, destination_path)
            print(f"Renamed '{file_name}' to '{new_name}'.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileToolGUI(root)
    root.mainloop()

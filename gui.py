import tkinter as tk
from tkinter import scrolledtext, messagebox
import os
class FileExplorerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File System Explorer")
        self.root.geometry("800x600")
        try:
            self.current_directory = os.getcwd()
        except OSError:
            self.current_directory = os.path.expanduser("~")
        top_frame = tk.Frame(root)
        top_frame.pack(fill=tk.X, padx=10, pady=5)
        self.path_label = tk.Label(top_frame, text=f"Path: {self.current_directory}", anchor="w")
        self.path_label.pack(fill=tk.X)
        input_frame = tk.Frame(top_frame)
        input_frame.pack(fill=tk.X, pady=5)
        tk.Label(input_frame, text="Input:").pack(side=tk.LEFT)
        self.input_entry = tk.Entry(input_frame)
        self.input_entry.pack(fill=tk.X, expand=True, side=tk.LEFT, padx=5)
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        button_panel = tk.Frame(main_frame, width=200)
        button_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        buttons_info = [
            ("1. List Directory", self.list_directory),
            ("2. Move Up", self.move_up),
            ("3. Move Down", self.move_down),
            ("4. Number of Files", self.count_files),
            ("5. Size of Directory", self.get_dir_size),
            ("6. Search for File", self.search_file),
            ("7. View File Contents", self.view_file),
            ("8. Quit Program", self.root.destroy)
        ]
        for text, command in buttons_info:
            tk.Button(button_panel, text=text, command=command, anchor="w").pack(fill=tk.X, pady=3)
        self.display_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.display_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.list_directory()
    def _set_output(self, content):
        self.display_text.config(state=tk.NORMAL)
        self.display_text.delete("1.0", tk.END)
        self.display_text.insert("1.0", content)
        self.display_text.config(state=tk.DISABLED)
    def _get_input(self):
        return self.input_entry.get().strip()
    def _update_path_label(self):
        self.path_label.config(text=f"Path: {self.current_directory}")  
    def list_directory(self):
        try:
            items = os.listdir(self.current_directory)
            folders = [item for item in items if os.path.isdir(os.path.join(self.current_directory, item))]
            files = [item for item in items if os.path.isfile(os.path.join(self.current_directory, item))]            
            folders.sort()
            files.sort()            
            output = "--- FOLDERS ---\n"
            output += "\n".join(folders) if folders else "[None]"
            output += "\n\n--- FILES ---\n"
            output += "\n".join(files) if files else "[None]"            
            self._set_output(output)
        except PermissionError:
            self._set_output(f"PermissionError: Cannot access '{self.current_directory}'")
        except Exception as e:
            self._set_output(f"Error: {e}")
    def move_up(self):
        parent_dir = os.path.dirname(self.current_directory)
        if parent_dir != self.current_directory:
            self.current_directory = parent_dir
            self._update_path_label()
            self.list_directory()
        else:
            self._set_output("Already at the root directory.")
    def move_down(self):
        subdir_name = self._get_input()
        if not subdir_name:
            messagebox.showwarning("Input Needed", "Please type a directory name in the input box to move down.")
            return
        new_path = os.path.join(self.current_directory, subdir_name)
        if os.path.isdir(new_path):
            self.current_directory = new_path
            self._update_path_label()
            self.input_entry.delete(0, tk.END)
            self.list_directory()
        else:
            self._set_output(f"Error: '{subdir_name}' is not a valid directory.")
    def count_files(self):
        try:
            count = 0
            items = os.listdir(self.current_directory)
            for item in items:
                if os.path.isfile(os.path.join(self.current_directory, item)):
                    count += 1
            self._set_output(f"Total files in this directory: {count}")
        except Exception as e:
            self._set_output(f"Error: {e}")     
    def get_dir_size(self):
        self._set_output("Calculating size... This may take a moment.")
        self.root.update_idletasks()     
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(self.current_directory):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if not os.path.islink(fp):
                        total_size += os.path.getsize(fp)          
            self._set_output(f"Total directory size: {total_size:,} bytes")
        except Exception as e:
            self._set_output(f"Error calculating size: {e}")
    def search_file(self):
        search_term = self._get_input()
        if not search_term:
            messagebox.showwarning("Input Needed", "Please type a search term in the input box.")
            return       
        self._set_output(f"Searching for '{search_term}'...")
        self.root.update_idletasks()
        results = []
        try:
            for dirpath, dirnames, filenames in os.walk(self.current_directory):
                for f in filenames:
                    if search_term.lower() in f.lower():
                        results.append(os.path.join(dirpath, f))   
            if results:
                self._set_output("--- SEARCH RESULTS ---\n" + "\n".join(results))
            else:
                self._set_output(f"No files found matching '{search_term}'.")
        except Exception as e:
            self._set_output(f"Error during search: {e}")
    def view_file(self):
        filename = self._get_input()
        if not filename:
            messagebox.showwarning("Input Needed", "Please type a file name in the input box to view.")
            return
        file_path = os.path.join(self.current_directory, filename)
        if not os.path.isfile(file_path):
            self._set_output(f"Error: '{filename}' is not a file or does not exist.")
            return
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                contents = f.read(1024 * 100)
            self._set_output(f"--- CONTENTS OF {filename} ---\n\n{contents}")            
        except UnicodeDecodeError:
            self._set_output(f"Cannot display file: '{filename}' is a binary file or uses unknown encoding.")
        except PermissionError:
            self._set_output(f"PermissionError: Cannot read '{filename}'.")
        except Exception as e:
            self._set_output(f"Error reading file: {e}")
if __name__ == "__main__":
    root = tk.Tk()
    app = FileExplorerApp(root)
    root.mainloop()

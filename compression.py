import tkinter as tk
from tkinter.ttk import Treeview
from tkinter import filedialog
from PIL import Image
import os
from tkinter import messagebox
import json
import sys


def valiadate_file_count(directory_path):
    dir_count = []
    for root, dirs, files in os.walk(directory_path):
        count_images = 0
        for file in files:
            if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
                count_images += 1
        dir_count.append((root, count_images))
    return dir_count


def append_resized_to_filename(image_path):
    # Split the file path into directory, filename, and extension
    directory, filename = os.path.split(image_path)
    filename, extension = os.path.splitext(filename)

    # Append "_resized" to the filename
    new_filename = f"{filename}_resized{extension}"

    # Combine the directory and new filename to get the new file path
    new_image_path = os.path.join(directory, new_filename)

    return new_image_path.replace("\\", "/")


def process_image(image_path, output_path):
    # print(image_path)

    # Resize the image
    width = 640
    height = 480
    resize_image(image_path, output_path, width, height)


def make_directory(directory_path):
    os.makedirs(directory_path, exist_ok=True)


def resize_image(image_path, output_path, width, height):
    image = Image.open(image_path)
    resized_image = image.resize((width, height))
    resized_image.save(output_path)


def main():
    try:

        root = tk.Tk()
        root.withdraw()  # Hide the main window

        # Ask the user if they want to select a file or a directory
        MsgBox = messagebox.askquestion(
            'File or Directory', 'Select "Yes" for directory and "NO" for choosing jpg file', icon='question')

        if MsgBox == 'yes':
            # Open the file dialog with a filter for .jpg files and get the selected file path
            directory_path = filedialog.askdirectory()
            # print(directory_path)
            print("""Please wait while its resizing the images...""")
            if cycle_through_files(directory_path):
                const_tuple = new_directory_root(directory_path)
                replaced_directory_path = replace_with_new_directory(
                    directory_path, const_tuple)
                print("""Resizing completed""")
                check_window(directory_path, replaced_directory_path)

        else:
            # Open the directory dialog and get the selected directory path
            file_path = filedialog.askopenfilenames(
                filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("JPEG files", "*.jpeg")])
            # print(file_path)

            print("""Please wait while its resizing the images...""")
            for names in file_path:
                output_path = append_resized_to_filename(names)
                # print(output_path)
                process_image(names, output_path)

            print("""Resizing completed""")
            sys.exit()
    except Exception as e:
        print(e)


def create_tree(parent, directory_info, column_title):
    # Create a Treeview widget
    tree = Treeview(parent)

    # Define the columns
    tree["columns"] = ("one")

    max_length_0 = max(len(info[0]) for info in directory_info)
    max_length_1 = max(len(str(info[1])) for info in directory_info)

    # Format the columns
    tree.column("#0", width=max_length_0*6, minwidth=270, stretch=False)
    tree.column("one", width=max_length_1*100, minwidth=270,
                stretch=False, anchor='center')

    # Define the column headings
    tree.heading("#0", text="Directory Path", anchor='w')
    tree.heading("one", text=column_title, anchor='center')

    # Add the directory info to the Treeview
    for info in directory_info:
        tree.insert("", "end", text=info[0], values=(
            info[1]))

    return tree


def check_window(original_path, resized_path):
    directory_info = valiadate_file_count(
        original_path)
    directory_info_resized = valiadate_file_count(
        resized_path)

    root = tk.Tk()

    tree1 = create_tree(root, directory_info, "File Count")
    tree1.grid(row=0, column=0)

    tree2 = create_tree(root, directory_info_resized, "Resized File Count")
    tree2.grid(row=0, column=1)

    # Configure the grid to expand with the window
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)

    def on_closing():
        root.destroy()
        sys.exit()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()


def new_directory_root(directory_path):
    out_last_name_original = os.path.basename(
        directory_path)
    # print(out_last_name)
    out_last_name = out_last_name_original + "_resized"
    # print(out_last_name)
    return (out_last_name_original, out_last_name)


def replace_with_new_directory(directory_path, tuple):
    out_last_name_original, out_last_name = tuple

    return fix_slash(directory_path.replace(out_last_name_original, out_last_name))


def fix_slash(path):
    return path.replace("\\", "/")


def cycle_through_files(directory_path):
    # print("directory path ",directory_path)

    const_tuple = new_directory_root(directory_path)

    for root, dirs, files in os.walk(directory_path):

        # print("new root ",replace_with_new_directory(root, const_tuple))
        new_root = replace_with_new_directory(root, const_tuple)
        make_directory(new_root)

        for file in files:
            if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
                file_path = os.path.join(root, file)
                # print("file path ",replace_with_new_directory(file_path, const_tuple))
                output_file_path = replace_with_new_directory(
                    file_path, const_tuple)
                process_image(file_path, output_file_path)

    return True


if __name__ == "__main__":
    main()

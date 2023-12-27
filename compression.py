import tkinter as tk
from tkinter import filedialog
from PIL import Image
import os
from tkinter import messagebox
import json


def valiadate_file_count(directory_path):
    
    dir_count = []
    for root, dirs, files in os.walk(directory_path):
        count_images = 0
        for file in files:
            if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
                count_images += 1
        dir_count.append((root,count_images))
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

"""
def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Ask the user if they want to select a file or a directory
    MsgBox = messagebox.askquestion(
        'File or Directory', 'Select "Yes" for directory and "NO" for choosing jpg file', icon='question')

    if MsgBox == 'yes':
        # Open the file dialog with a filter for .jpg files and get the selected file path
        directory_path = filedialog.askdirectory()
        # print(directory_path)
        cycle_through_files(directory_path)

    else:
        # Open the directory dialog and get the selected directory path
        file_path = filedialog.askopenfilenames(
            filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("JPEG files", "*.jpeg")])
        print(file_path)

        for names in file_path:
            output_path = append_resized_to_filename(names)
            # print(output_path)
            process_image(names, output_path)

"""
def main():
    # cycle_through_files("sample")
    print(valiadate_file_count("M:/Projects/Milan Photo - Copy/2023.12.15"))

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
        count_directories += 1

        for file in files:
            if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
                file_path = os.path.join(root, file)
                # print("file path ",replace_with_new_directory(file_path, const_tuple))
                output_file_path = replace_with_new_directory(
                    file_path, const_tuple)
                process_image(file_path, output_file_path)
                count_images += 1

    return (count_directories, count_images)


if __name__ == "__main__":
    main()

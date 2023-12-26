import tkinter as tk
from tkinter import filedialog
from PIL import Image
import os
from tkinter import messagebox


def append_resized_to_filename(image_path):
    # Split the file path into directory, filename, and extension
    directory, filename = os.path.split(image_path)
    filename, extension = os.path.splitext(filename)

    # Append "_resized" to the filename
    new_filename = f"{filename}_resized{extension}"

    # Combine the directory and new filename to get the new file path
    new_image_path = os.path.join(directory, new_filename)

    return new_image_path.replace("\\", "/")


def process_image(image_path):
    # Get the new image path
    output_path = append_resized_to_filename(image_path)
    # Resize the image
    width = 640
    height = 400
    resize_image(image_path, output_path, width, height)


def append_resized_to_foldername(folder_path):
    # Get the folder name from the folder path
    folder_name = os.path.basename(folder_path)

    # Append "_resized" to the folder name
    new_folder_name = f"{folder_name}_resized"

    # Get the parent directory of the folder path
    parent_directory = os.path.dirname(folder_path)

    # Combine the parent directory and new folder name to get the new folder path
    new_folder_path = os.path.join(parent_directory, new_folder_name)

    return new_folder_path.replace("\\", "/")


def make_directory(directory_path):
    os.makedirs(directory_path, exist_ok=True)


def resize_image(image_path, output_path, width, height):
    image = Image.open(image_path)
    resized_image = image.resize((width, height))
    resized_image.save(output_path)


def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    # Open the folder dialog and get the selected folder path
    # folder_path = filedialog.askdirectory()
    # print(folder_path)

    # # Example usage
    # image_path = folder_path
    # # output_path = append_resized_to_filename(image_path)
    # # width = 640
    # # height = 400
    # # resize_image(image_path, output_path, width, height)
    # output_path = append_resized_to_foldername(image_path)
    # print(output_path)
    # make_directory(output_path)

    # Ask the user if they want to select a file or a directory
    MsgBox = messagebox.askquestion(
        'File or Directory', 'Select "Yes" for directory and "NO" for choosing jpg file', icon='question')

    if MsgBox == 'yes':
        # Open the file dialog with a filter for .jpg files and get the selected file path
        directory_path = filedialog.askdirectory()
        print(directory_path)
        cycle_through_files(directory_path)
        
    else:
        # Open the directory dialog and get the selected directory path
        file_path = filedialog.askopenfilename(
            filetypes=[("JPEG files", "*.jpg")])
        print(file_path)
        process_image(file_path)


def cycle_through_files(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".jpg"):
                file_path = os.path.join(root, file)
                print(file_path)
                process_image(file_path)



if __name__ == "__main__":
    main()

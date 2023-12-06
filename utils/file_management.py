import os
from datetime import datetime
import cv2
import tkinter as tk

# Caminho padrão do diretório de salvamento dos arquivos
DEFAULT_SAVING_DIRECTORY = "/home/sitech/Documents/teste_predic/"

sample_tag = "452156267"
resource_path = "resources/samples/predic/318-0613.jpg"

class FileManagement:

    def make_sample_dir(self, tag, index=0):
        """
        Creates a sample directory based on the given tag and index.

        Parameters:
        - `tag` (str): The tag to include in the directory name.
        - `index` (int): The index used to distinguish directories with the same tag.

        Returns:
        str: The path of the created directory.
        """

        base_directory = DEFAULT_SAVING_DIRECTORY
        directory_path = self._generate_directory_path(base_directory, tag, index)

        while os.path.exists(directory_path):
            index += 1
            directory_path = self._generate_directory_path(base_directory, tag, index)

        os.makedirs(directory_path)
        return directory_path

    def _generate_directory_path(self, base_directory, tag, index):
        """
        Generates the directory path based on the base directory, tag, and index.

        Parameters:
        - `base_directory` (str): The base directory path.
        - `tag` (str): The tag to include in the directory name.
        - `index` (int): The index used to distinguish directories with the same tag.

        Returns:
        str: The generated directory path.
        """

        if index == 0:
            return os.path.join(base_directory, tag)
        else:
            return os.path.join(base_directory, f"{tag} ({index})")



    # Gera o nome do arquivo de imagem tag_timestamp.png
    def get_image_filename(self, tag):
        """
        Generates a filename for an image based on the given tag and current timestamp.

        Parameters:
        - `tag` (str): The tag to include in the filename.

        Returns:
        str: The generated filename.
        """

        current_timestamp = datetime.now();
        formatted_timestamp = current_timestamp.strftime("%Y-%m-%d_%H.%M.%S")

        filename = f"{tag}_{formatted_timestamp}.png"
        return filename


    # Opens a file dialog so the user can select the file path where image files will be stored
    def open_file_dialog(self, master):
        """
        Opens a file dialog and allows the user to select a directory path in the file system.

        Parameters:
        - `master`: The window from which the file dialog is called.

        Returns:
        str: The selected directory path. Returns an empty string if the user cancels the operation.
        """

        # Hide the main window
        master.withdraw()

        try:
            # Opens a file dialog to select a folder
            selected_dir_path = tk.filedialog.askdirectory(title="Selecione a pasta")
            return selected_dir_path
        except Exception as e:
            # Handle exceptions, if any
            print(f"An error ocurred: {e}")
            return ""
        finally:
            # Deiconify (unhide) the master window after the file dialog is closed or an exception occurs
            master.deiconify()


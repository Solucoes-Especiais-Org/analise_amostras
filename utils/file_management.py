import os
from datetime import datetime
import cv2
import tkinter as tk

# Caminho padrão do diretório de salvamento dos arquivos
DEFAULT_SAVING_DIRECTORY = "/home/sitech/Documents/teste_predic/"

sample_tag = "452156267"
resource_path = "resources/samples/predic/318-0613.jpg"

class FileManagement:

    def make_sample_dir(self, tag, i=0):
        if (i==0):
            new_directory_path = DEFAULT_SAVING_DIRECTORY + tag + '/'
        else:
            new_directory_path = DEFAULT_SAVING_DIRECTORY + tag + ' (' + str(i) + ')/'

        if os.path.exists(new_directory_path):
            return self.make_sample_dir(tag, i+1)
        else:
            os.makedirs(new_directory_path)
            return new_directory_path

    # Gera o nome do arquivo de imagem tag_timestamp.png
    def get_image_filename(self, tag):
        # Get current datetime
        current_timestamp = datetime.now();
        formatted_timestamp = current_timestamp.strftime("%Y-%m-%d_%H.%M.%S")

        # Get filename as tag_timestamp.png
        filename = tag + '_' + formatted_timestamp + '.png'
        return filename


    # Opens a file dialog so the user can select the file path where image files will be stored
    def open_file_dialog(self, master):
        # Hide the main window
        master.withdraw()

        # Opens a file dialog to select a folder
        file_path = tk.filedialog.askdirectory(title="Selecione a pasta")
        return file_path

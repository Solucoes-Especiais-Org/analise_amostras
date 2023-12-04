from tkinter import *
from tkinter import filedialog
import os
from datetime import datetime

import cv2

from utils.impurity_detector import ImpurityDetector
from utils.qr_code_reader import QRCodeReader

# Caminho padrão do diretório de salvamento dos arquivos
DEFAULT_SAVING_DIRECTORY = "/home/sitech/Documents/teste_predic/"

sample_tag = "452156267"
resource_path = "resources/samples/predic/318-0613.jpg"

class MainWindow:

    def __init__(self, master, video_source):
        self.master = master
        master.title("Análise de Amostras")
        master.geometry('645x400')
        master.minsize(645, 400)

        self.qr_code_reader = QRCodeReader()
        self.impurity_detector = ImpurityDetector()

        self.vid = cv2.VideoCapture(video_source)

        # Nome da imagem = TAG + TimeStamp
        name = Label(master, text='tag_timestamp.png', font=("Helvetica", 16))
        name.grid(column=0, row=0, columnspan=3)

        # Resultado da análise ("Amostra Contaminada" / "Amostra Livre de Impureza")
        #result = Label(master, text='', font=("Helvetica", 16))
        #result.grid(column=0, row=3, columnspan=3)

        # Campo de exibição 1 - Máscara aplicada
        image_canvas1 = Canvas(master, width=300, height=300, borderwidth=2, relief="solid")
        image_canvas1.grid(column=0, row=1, sticky="nsew")

        # Campo de exibição 2 - Binarização da imagem
        image_canvas2 = Canvas(master, width=300, height=300, borderwidth=2, relief="solid")
        image_canvas2.grid(column=2, row=1, sticky="nsew")

        # Inicia o processo
        start_button = Button(master, text="START", width=10, command=self.start_process(master), background="#f8f4f4")
        start_button.grid(column=0, row=4)

        # Encerra o processo
        stop_button = Button(master, text='STOP', width=10, background="#f8f4f4")
        stop_button.grid(column=2, row=4)
        stop_button.configure(state=DISABLED)

        # Função para configurar o cursor ao passar o mouse sobre o botão START
        def on_enter_start(event):
            start_button.config(cursor="hand2")
            start_button.config(background="#dddddd")

        # Função para configurar o cursor ao retirar o mouse do botão START
        def on_leave_start(event):
            start_button.config(cursor="")
            start_button.config(background="#f8f4f4")

        # Função para configurar o cursor ao passar o mouse sobre o botão STOP
        def on_enter_stop(event):
            stop_button.config(cursor="hand2")
            stop_button.config(background="#dddddd")

        # Função para configurar o cursor ao retirar o mouse do botão STOP
        def on_leave_stop(event):
            stop_button.config(cursor="")
            stop_button.config(background="#f8f4f4")

        # Associa os eventos de passagem do mouse às funções correspondentes
        start_button.bind("<Enter>", on_enter_start)
        start_button.bind("<Leave>", on_leave_start)

        stop_button.bind("<Enter>", on_enter_stop)
        stop_button.bind("<Leave>", on_leave_stop)

        # Configuração para manter os tamanhos
        master.columnconfigure(0, weight=1, minsize=300)
        master.columnconfigure(2, weight=1, minsize=300)
        master.rowconfigure(1, weight=1, minsize=300)
        master.rowconfigure(4, weight=1)
    

    def start_process(self, master):
        # Resultado da análise ("Amostra Contaminada" / "Amostra Livre de Impureza")
        resultLabel = Label(master, text='', font=("Helvetica", 16))
        resultLabel.grid(column=0, row=3, columnspan=3)

        self.save_image()

        [result, result_img] = self.impurity_detector.search_for_impurity("resources/samples/predic/318-0382.jpg")

        if (result):
            resultLabel.config(text="Amostra contaminada")
        else:
            resultLabel.config(text="Amostra livre de impureza")

        self.save_image(result_img)


    # Creates a new folder inside DEFAULT_SAVING_DIRECTORY with the same name as the sample's tag
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
    def get_new_filename(tag):
        # Get current datetime
        current_timestamp = datetime.now();
        formatted_timestamp = current_timestamp.strftime("%Y-%m-%d_%H.%M.%S")

        # Get filename as tag_timestamp.png
        filename = tag + '_' + formatted_timestamp + '.png'
        return filename

    """
    def save_image(self, tag, img, canny1):
        # Creates new folder inside DEFAULT_SAVING_DIRECTORY with the same name as the sample's tag
        dir_path = self.make_sample_dir(tag)

        # Save original image
        orig_filename = self.get_new_filename(str(tag) + "orig_" )
        orig_filepath = dir_path + str(orig_filename)
        cv2.imwrite(orig_filepath, img)

        # Save image with canny contour method applied
        canny_filename = self.get_new_filename(str(tag) + "canny_")
        canny_filepath = dir_path + canny_filename
        cv2.imwrite(canny_filepath, canny1)    
    """

    def save_image(self, tag, img, canny1):
        # Creates new folder inside DEFAULT_SAVING_DIRECTORY with the same name as the sample's tag
        dir_path = self.make_sample_dir(tag)

        # Save original image
        file_name = self.get_new_filename(tag)
        file_path = dir_path + str(file_name)
        cv2.imwrite(file_path, img)

        return file_path


    # Opens a file dialog so the user can select the file path where image files will be stored
    def open_file_dialog():
        # Hide the main window
        master.withdraw()

        # Opens a file dialog to select a folder
        file_path = filedialog.askdirectory(title="Selecione a pasta")
        return file_path


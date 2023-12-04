import tkinter as tk
import os
from datetime import datetime

import cv2

from utils.file_management import FileManagement
from utils.impurity_detector import ImpurityDetector
from utils.qr_code_reader import QRCodeReader
from gui.webcam_window import WebcamWindow

# Caminho padrão do diretório de salvamento dos arquivos
DEFAULT_SAVING_DIRECTORY = "/home/sitech/Documents/teste_predic/"

sample_tag = "452156267"
resource_path = "resources/samples/predic/318-0613.jpg"

# Example usage in another application
class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Análise de Amostras")
        root.geometry('645x400')
        root.minsize(645, 400)

        self.file_management = FileManagement();
        self.impurity_detector = ImpurityDetector();

        # Create a canvas to display the webcam stream
        #self.canvas = tk.Canvas(root)
        #self.canvas.pack()

         # Campo de exibição 1 - Máscara aplicada
        self.image_canvas1 = tk.Canvas(root, width=300, height=300, borderwidth=2, relief="solid")
        self.image_canvas1.grid(column=0, row=1, sticky="nsew")

        # Create an instance of WebcamApp and pass the canvas as a parameter
        self.webcam_window = WebcamWindow(self.image_canvas1, video_source=0)

        # Campo de exibição 2 - Binarização da imagem
        image_canvas2 = tk.Canvas(root, width=300, height=300, borderwidth=2, relief="solid")
        image_canvas2.grid(column=2, row=1, sticky="nsew")

        # Add other widgets or functionality to your application as needed
        # ...
         # Inicia o processo
        start_button = tk.Button(root, text="START", width=10, command=self.start_process(root), background="#f8f4f4")
        start_button.grid(column=0, row=4)

        # Encerra o processo
        stop_button = tk.Button(root, text='STOP', width=10, background="#f8f4f4")
        stop_button.grid(column=2, row=4)
        stop_button.configure(state=tk.DISABLED)

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
        root.columnconfigure(0, weight=1, minsize=300)
        root.columnconfigure(2, weight=1, minsize=300)
        root.rowconfigure(1, weight=1, minsize=300)
        root.rowconfigure(4, weight=1)

        # Set up the window closing event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        # Perform any cleanup tasks and close the application
        # For example, you might stop other threads or processes
        self.webcam_window.stop_video()
        self.root.destroy()


    def start_process(self, root):
        # Resultado da análise ("Amostra Contaminada" / "Amostra Livre de Impureza")
        resultLabel = tk.Label(root, text='', font=("Helvetica", 16))
        resultLabel.grid(column=0, row=3, columnspan=3)

        sample_dir = self.file_management.make_sample_dir(sample_tag)

        src_image_path = self.webcam_window.capture_frame(sample_dir, sample_tag)

        #self.save_image()

        #self.webcam_window.capture_frame()

        result = self.impurity_detector.search_for_impurity(sample_dir, sample_tag, src_image_path)

        if (result):
            resultLabel.config(text="Amostra contaminada")
        else:
            resultLabel.config(text="Amostra livre de impureza")

        #self.save_image(result_img)


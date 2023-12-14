import os
import cv2
import tkinter as tk
from datetime import datetime
from utils.file_management import FileManagement
from utils.impurity_detector import ImpurityDetector
from utils.qr_code_reader import QRCodeReader
from gui.webcam_window import WebcamWindow
from PIL import Image, ImageTk

# Caminho padrão do diretório de salvamento dos arquivos
DEFAULT_SAVING_DIRECTORY = "/home/sitech/Documents/teste_predic/"
sample_tag = "452156267"
resource_path = "resources/samples/predic/test.jpg"

# Example usage in another application
class MainWindow:

    def __init__(self, root):
        self.root = root
        self.root.title("Análise de Amostras")
        self.root.state('zoomed')
        self.root.resizable(width=False, height=False)
        self.file_management = FileManagement()
        self.impurity_detector = ImpurityDetector()
        # self.qr_code_reader = QRCodeReader()
        self.result_image_canvas = None
        self.image_tk = None
        self.init_ui(self.root)

    def init_ui(self, root):
        """
        Initialize the user interface for the main application window.

        This function sets up the UI components including canvases for webcam stream and result image,
        START and STOP buttons, and configures column and row sizes.

        Additionally, it establishes the event handler for the window closing event.

        Parameters:
            root (tk.Tk): The Tkinter root window.

        Returns:
            None
        """
        # Create and configure START button
        start_button = tk.Button(root, text="START", width=10, command=self.start_process, background="#f8f4f4")
        start_button.grid(column=0, row=4)
        self.configure_button_hover(start_button)

        # Create and configure STOP button
        stop_button = tk.Button(root, text='STOP', width=10, background="#f8f4f4", state=tk.DISABLED)
        stop_button.grid(column=2, row=4)
        self.configure_button_hover(stop_button)

        # Configure column and row sizes
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(4, weight=1)

        # Set up the window closing event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Create a canvas for webcam stream
        webcam_canvas = self.create_image_canvas(root, column=0, row=1, sticky="nsew")
        # Create an instance of WebcamWindow and pass the canvas as a parameter
        self.webcam_window = WebcamWindow(webcam_canvas, video_source=0)

        # Create a canvas for the result image
        self.result_image_canvas = self.create_result_image_canvas(root)

        # Define o tamanho desejado do canvas
        canvas_width = 640
        canvas_height = 480

        # Carrega a imagem usando PIL
        img_pil = Image.open(resource_path)

        # Calcula o fator de zoom para preencher o canvas
        zoom_factor = max(canvas_width / img_pil.width, canvas_height / img_pil.height)
        # Redimensiona a imagem aplicando o fator de zoom
        img_pil = img_pil.resize((int(img_pil.width * zoom_factor), int(img_pil.height * zoom_factor)))

        # Converte a imagem para o formato compatível com Tkinter
        self.image_tk = ImageTk.PhotoImage(img_pil)

        # Exibe a imagem no Canvas result_image_canvas
        self.result_image_canvas.config(width=canvas_width, height=canvas_height)
        self.result_image_canvas.create_image(340, 0, anchor="n", image=self.image_tk)

    def create_result_image_canvas(self, root):
        """
        Creates a Tkinter Canvas widget for displaying the result image.

        Parameters:
            root (tk.Tk): The Tkinter root window.

        Returns:
            tk.Canvas: The created Canvas widget for displaying the result image.
        """
        result_canvas = self.create_image_canvas(root, column=2, row=1, sticky="nsew")
        return result_canvas

    def create_image_canvas(self, root, column, row, sticky):
        """
        Creates a Tkinter Canvas widget for displaying images.

        Parameters:
            root (tk.Tk): The Tkinter root window.
            column (int): The column index where the canvas should be placed.
            row (int): The row index where the canvas should be placed.
            sticky (str): Defines how the canvas should expand or shrink if the widget exceeds its natural size.

        Returns:
            tk.Canvas: The created Canvas widget for displaying images.
        """
        canvas = tk.Canvas(root, width=640, height=480, borderwidth=1, relief="solid")
        canvas.grid(column=column, row=row, sticky=sticky)
        return canvas

    def configure_button_hover(self, button):
        """
        Configures button hover behavior.

        Binds the <Enter> and <Leave> events for a Tkinter button to corresponding methods.

        Args:
            button (tk.Button): The Tkinter Button widget to which hover behavior will be applied.
        """
        button.bind("<Enter>", lambda event: self.on_enter_button(event, button))
        button.bind("<Leave>", lambda event: self.on_leave_button(event, button))

    def on_enter_button(self, event, button):
        """
        Event handler for mouse entering a Tkinter button.

        Changes the cursor to a hand icon and adjusts the button background when the mouse enters the button.

        Args:
            event: The event object containing information about the mouse event.
            button (tk.Button): The Tkinter Button widget being interacted with.
        """
        button.config(cursor="hand2")
        button.config(background="#dddddd")

    def on_leave_button(self, event, button):
        """
        Event handler for mouse leaving a Tkinter button.

        Resets the cursor to the default and restores the original button background when the mouse leaves the button.

        Args:
            event: The event object containing information about the mouse event.
            button (tk.Button): The Tkinter Button widget being interacted with.
        """
        button.config(cursor="")
        button.config(background="#f8f4f4")

    def start_process(self, root):
        # Resultado da análise ("Amostra Contaminada" / "Amostra Livre de Impureza")
        resultLabel = tk.Label(root, text='', font=("Helvetica", 16))
        resultLabel.grid(column=0, row=3, columnspan=3)
        sample_dir = self.file_management.make_sample_dir(sample_tag)
        src_image_path = self.webcam_window.capture_frame(sample_dir, sample_tag)
        result = self.impurity_detector.search_for_impurity(sample_dir, sample_tag, src_image_path)
        if result:
            resultLabel.config(text="Amostra contaminada")
        else:
            resultLabel.config(text="Amostra livre de impureza")

    def on_closing(self):
        # Perform any cleanup tasks and close the application
        # For example, you might stop other threads or processes
        self.webcam_window.stop_video()
        self.root.destroy()

from tkinter import Tk
from gui.main_window import MainWindow

if __name__ == "__main__":
    root = Tk()
    video_source = 0
    qr_code_source = 1
    app = MainWindow(root, video_source)
    root.mainloop()

import cv2
import tkinter as tk
from PIL import Image, ImageTk
from utils.file_management import FileManagement

class WebcamWindow:

    def __init__(self, canvas, video_source=0):
        self.file_management = FileManagement()
        self.canvas = canvas
        self.photo_image = None
        self.vid = cv2.VideoCapture(video_source)
        self.update()

    def update(self):
        ret, frame = self.vid.read()

        if ret:
            frame = cv2.resize(frame, (640, 480))
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            photo = ImageTk.PhotoImage(image=Image.fromarray(rgb_frame))

            # Resize the image
            canvas_width = 640
            canvas_height = 480
            resized_img = Image.fromarray(rgb_frame).resize((canvas_width, canvas_height))
            resized_photo = ImageTk.PhotoImage(resized_img)
            self.canvas.config(width=canvas_width, height=canvas_height)
            self.canvas.create_image(340, 0, anchor="n", image=resized_photo)
            self.canvas.photo = resized_photo
            self.photo_image = resized_photo
            self.canvas.after(10, self.update)

    def get_image_size(self):
        if self.photo_image:
            return self.photo_image.width(), self.photo_image.height()
        else:
            return 0, 0

    def stop_video(self):
        # Release the video source
        if self.vid.isOpened():
            self.vid.release()

    def capture_frame(self, dir_path, tag):
        # Get a frame from the video source
        ret, frame = self.vid.read()

        if ret:
            # Convert the frame to RGB format
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image_filename = "orig_" + self.file_management.get_image_filename(tag)
            image_path = dir_path + image_filename
            # Save the captured frame as an image file
            cv2.imwrite(image_path, rgb_frame)
            return image_path

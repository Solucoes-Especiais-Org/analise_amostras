import cv2
import tkinter as tk
from PIL import Image, ImageTk

from utils.file_management import FileManagement

class WebcamWindow:
    def __init__(self, canvas, video_source=0):
        self.file_management = FileManagement()

        self.canvas = canvas

        # Open the video source (webcam)
        self.vid = cv2.VideoCapture(video_source)

        # Call the update method to start streaming video
        self.update()

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.read()

        if ret:
            # Convert the frame to RGB format
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert the frame to a PhotoImage object
            photo = ImageTk.PhotoImage(image=Image.fromarray(rgb_frame))

            # Update the canvas with the new PhotoImage
            self.canvas.config(width=photo.width(), height=photo.height())
            self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)

            # Keep a reference to avoid garbage collection
            self.canvas.photo = photo

            # Call the update method again after the specified delay
            self.canvas.after(10, self.update)

    def stop_video(self):
        # Release the video source
        if self.vid.isOpened():
            self.vid.release()

    def capture_frame(self, dir_path, tag):
        # Get a frame from the video source
        ret, frame = self.vid.read()

        if ret:
            # Convert the frame to RGB format
            #rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            image_filename = "orig_" + self.file_management.get_image_filename(tag)

            image_path = dir_path + image_filename

            # Save the captured frame as an image file
            cv2.imwrite(image_path, frame)

            return image_path

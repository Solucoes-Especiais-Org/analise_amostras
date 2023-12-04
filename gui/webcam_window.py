import cv2
import tkinter as tk
from PIL import Image, ImageTk

class WebcamWindow:
    def __init__(self, canvas, video_source=0):
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

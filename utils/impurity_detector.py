import cv2
import imutils
import numpy as np
from imutils import contours

from utils.file_management import FileManagement

class ImpurityDetector:

    def __init__(self):
        self.file_management = FileManagement()

    def search_for_impurity(self, dir_path, tag, src_image_path):

        original_img = cv2.imread(src_image_path)
        original_img = original_img[::2, ::2]

        cropped_img = self.crop_image(original_img)

        circular_masked_img = self.create_circular_mask(cropped_img)

        # Convert from RGB to grayscale
        rgb_img = cv2.cvtColor(circular_masked_img, cv2.COLOR_BGR2GRAY)
        # Aplly gaussian blur filter
        blur_img = cv2.GaussianBlur(rgb_img, (7, 7), 0)
        # Adaptative threshold
        adaptative_threshold = cv2.adaptiveThreshold(blur_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 5)
        # Aplly Canny border detection algorithim
        canny_img = cv2.Canny(adaptative_threshold, 20, 120)

        # Saves result image to image file
        self.save_result_image(canny_img, dir_path, tag)

        canny_img = cv2.dilate(canny_img, None, iterations=1)
        canny_img = cv2.erode(canny_img, None, iterations=1)

        # Grab contours using canny result image (canny1)
        # Use flag cv2.RETR_TREE to find inner contours instead of only the most external one, which is achieved using flag RETR_EXTERNAL
        contours = cv2.findContours(canny_img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        # sort the contours from left-to-right and initialize the 'pixels per metric' calibration variable
        (contours, _) = contours.sort_contours(contours)

        areas = {}
        i = 0
        # loop over the contours individually
        for contour in contours:
            area = cv2.contourArea(contour)

            # area > 50 means there is light reflexion on the image
            # area < 0.0001 means the particle can be ignored
            if (area > 50) or (area < 0.0001):
                continue

            areas[i] = area
            i = i + 1


        if len(areas) > 4:
            return True
        else:
            return False


    def create_circular_mask(self, img):
        """
        Create a circular mask on the image to delimit the area of the bottle cap.

        Parameters:
            img (numpy.ndarray): The original image.

        Returns:
            numpy.ndarray: The image with the circular mask applied.
        """

        mascara = np.zeros(img.shape[:2], dtype="uint8")
        (cX, cY) = (img.shape[1] // 2, img.shape[0] // 2)
        cv2.circle(mascara, (cX, cY), 100, 255, -1)
        img = cv2.bitwise_and(img, img, mask=mascara)
        return img

    def crop_image(self, img):
        """
        Crop the image, keeping only the area corresponding to the bottle cap.

        Args:
            img (numpy.ndarray): The original image.

        Returns:
            numpy.ndarray: The cropped image.
        """

        ROWS = img.shape[0]
        COLS = img.shape[1]
        BORDER_RIGHT = (0, 0)
        BORDER_LEFT = (0, 0)

        right_found = False
        left_found = False

        # find borders of blank space for removal.
        # left and right border
        # print('Searching for Right and Left corners')
        for col in range(COLS):
            for row in range(ROWS):
                if left_found and right_found:
                    break

                # searching from left to right
                if not left_found and np.sum(img[row][col]) > 0:
                    BORDER_LEFT = (row, col)
                    left_found = True

                # searching from right to left
                if not right_found and np.sum(img[row][-col]) > 0:
                    BORDER_RIGHT = (row, img.shape[1] + (-col))
                    right_found = True

        BORDER_TOP = (0, 0)
        BORDER_BOTTOM = (0, 0)

        top_found = False
        bottom_found = False

        # top and bottom borders
        # print('Searching for Top and Bottom corners')
        for row in range(ROWS):
            for col in range(COLS):
                if top_found and bottom_found:
                    break

                # searching top to bottom
                if not top_found and np.sum(img[row][col]) > 0:
                    BORDER_TOP = (row, col)
                    top_found = True

                # searching bottom to top
                if not bottom_found and np.sum(img[-row][col]) > 0:
                    BORDER_BOTTOM = (img.shape[0] + (-row), col)
                    bottom_found = True

        # crop left and right borders, top and bottom borders
        new_img = img[BORDER_TOP[0]:BORDER_BOTTOM[0], BORDER_LEFT[1]:BORDER_RIGHT[1]]

        return new_img

    def save_result_image(self, img, dir_path, tag):

        image_filename = "canny_" + self.file_management.get_image_filename(tag)

        image_path = dir_path + image_filename

        cv2.imwrite(image_path, img)



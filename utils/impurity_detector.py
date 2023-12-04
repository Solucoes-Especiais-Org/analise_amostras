import cv2
import imutils
import numpy as np
from imutils import contours


class ImpurityDetector:

    def search_for_impurity(self, image_path):
        #self.master = master
        # Leitura da imagem com a função imread()

        #img = cv2.imread("resources/samples/predic/318-0613.jpg")
        img = cv2.imread(image_path)
        img = img[::2, ::2]

        # Redimensiona a imagem

        print('Largura em pixels: ', end='')
        print(img.shape[1])  # largura da imagem
        print('Altura em pixels: ', end='')
        print(img.shape[0])  # altura da imagem
        print('Qtde de canais: ', end='')
        print(img.shape[2])

        imgWidth = img.shape[1]  # largura da imagem
        imgHeight = img.shape[0]  # altura da imagem

        # Mostra a imagem com a função imshow
        #cv2.imshow("Imagem original", img)

        img = self.crop_image(img)

        # Cria uma máscara circular na imagem para delimitar a área da tampinha
        mascara = np.zeros(img.shape[:2], dtype="uint8")
        (cX, cY) = (img.shape[1] // 2, img.shape[0] // 2)
        cv2.circle(mascara, (cX, cY), 100, 255, -1)
        img = cv2.bitwise_and(img, img, mask=mascara)
        #cv2.imshow("Mascara aplicada a imagem", img)

        # Convert from RGB to grayscale
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Aplly gaussian blur filter
        suave = cv2.GaussianBlur(img, (7, 7), 0)
        # Adaptative threshold
        bin1 = cv2.adaptiveThreshold(suave, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 5)
        # Aplly Canny border detection algorithim
        canny1 = cv2.Canny(bin1, 20, 120)
        ############ SHOW CANNY1 ON GUI ########################

        """
        # Show results
        resultado = np.vstack([
            np.hstack([img, suave]),
            np.hstack([bin1, canny1])
        ])
        cv2.imshow("Binarizacao da imagem", resultado)  
        """

        # Find contours on Canny's result image
        canny1 = cv2.dilate(canny1, None, iterations=1)
        canny1 = cv2.erode(canny1, None, iterations=1)
        # Use flag cv2.RETR_TREE to find inner contours instead of only the most external one, which is achieved using flag RETR_EXTERNAL
        cnts = cv2.findContours(canny1.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        # sort the contours from left-to-right and initialize the 'pixels per metric' calibration variable
        (cnts, _) = contours.sort_contours(cnts)
        pixelsPerMetric = None  # Considerando a tampinha com 5 cm de diâmetro

        storeArea = {}
        i = 0
        # loop over the contours individually
        for c in cnts:
            area = cv2.contourArea(c)

            # area > 50 means there is light reflexion on the image
            # area < 0.0001 means the particle can be ignored
            if (area > 50) or (area < 0.0001):
                continue

            storeArea[i] = area
            i = i + 1


        if len(storeArea) > 4:
            return [1, img]
        else:
            return [0, img]



        # Atualiza a interface gráfica
        #master.update()

        # Reativa o botão START após o processamento
        #start_button.configure(state=NORMAL)


    def crop_image(self, img):

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

        #cv2.imshow("Imagem cortada", new_img)
        return new_img





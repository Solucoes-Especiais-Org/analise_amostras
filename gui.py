# testes
import cv2
import imutils
import numpy as np
from imutils import contours
from tkinter import *
import time

# Variável global para armazenar o último QR Code lido
last_read = ""


# Função para detecção de impurezas na imagem
def impurity_detection(image_path):
    global img
    global storeArea

    def crop_image():
        global img
        ROWS = img.shape[0]
        COLS = img.shape[1]
        BORDER_RIGHT = (0, 0)
        BORDER_LEFT = (0, 0)

        right_found = False
        left_found = False

        # Encontra as bordas do espaço em branco para remoção.
        # Bordas esquerda e direita
        for col in range(COLS):
            for row in range(ROWS):
                if left_found and right_found:
                    break

                # Procurando da esquerda para a direita
                if not left_found and np.sum(img[row][col]) > 0:
                    BORDER_LEFT = (row, col)
                    left_found = True

                # Procurando da direita para a esquerda
                if not right_found and np.sum(img[row][-col]) > 0:
                    BORDER_RIGHT = (row, img.shape[1] + (-col))
                    right_found = True

        BORDER_TOP = (0, 0)
        BORDER_BOTTOM = (0, 0)

        top_found = False
        bottom_found = False

        # Bordas superior e inferior
        for row in range(ROWS):
            for col in range(COLS):
                if top_found and bottom_found:
                    break

                # Procurando de cima para baixo
                if not top_found and np.sum(img[row][col]) > 0:
                    BORDER_TOP = (row, col)
                    top_found = True

                # Procurando de baixo para cima
                if not bottom_found and np.sum(img[-row][col]) > 0:
                    BORDER_BOTTOM = (img.shape[0] + (-row), col)
                    bottom_found = True

        # Corta as bordas esquerda e direita, superior e inferior
        new_img = img[BORDER_TOP[0]:BORDER_BOTTOM[0], BORDER_LEFT[1]:BORDER_RIGHT[1]]

        return new_img

    # Leitura da imagem com a função imread()
    img = cv2.imread(image_path)
    img = img[::2, ::2]

    # Redimensiona a imagem
    imgWidth = img.shape[1]
    imgHeight = img.shape[0]

    # Mostra a imagem com a função imshow
    img = crop_image()

    # Cria uma máscara circular na imagem para delimitar a área da tampinha
    mascara = np.zeros(img.shape[:2], dtype="uint8")
    (cX, cY) = (img.shape[1] // 2, img.shape[0] // 2)
    cv2.circle(mascara, (cX, cY), 100, 255, -1)
    img = cv2.bitwise_and(img, img, mask=mascara)

    # Convert de RGB para escala de cinza
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplica um filtro de desfoque gaussiano
    suave = cv2.GaussianBlur(img, (7, 7), 0)

    # Limiar adaptativo
    bin1 = cv2.adaptiveThreshold(suave, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 5)

    # Detecção de borda usando o algoritmo Canny
    canny1 = cv2.Canny(bin1, 20, 120)

    # Exibe os resultados
    resultado = np.vstack([
        np.hstack([img, suave]),
        np.hstack([bin1, canny1])
    ])

    # Encontra contornos na imagem resultante do Canny
    canny1 = cv2.dilate(canny1, None, iterations=1)
    canny1 = cv2.erode(canny1, None, iterations=1)

    # Usa a flag cv2.RETR_TREE para encontrar contornos internos em vez de apenas o mais externo
    cnts = cv2.findContours(canny1.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # Classifica os contornos da esquerda para a direita e inicializa a variável de calibração 'pixelsPerMetric'
    (cnts, _) = contours.sort_contours(cnts)
    pixelsPerMetric = None  # Considerando a tampinha com 5 cm de diâmetro

    storeArea = {}
    i = 0

    # Percorre os contornos individualmente
    for c in cnts:
        area = cv2.contourArea(c)

        # Área > 50 significa que há reflexo de luz na imagem
        # Área < 0.0001 significa que a partícula pode ser ignorada
        if (area > 50) or (area < 0.0001):
            continue

        storeArea[i] = area
        i = i + 1

    # Atualiza a interface gráfica
    window.update()

    # Reativa o botão START após o processamento
    start_button.configure(state=NORMAL)

    cv2.waitKey(0)

    # Retorna storeArea no final da função
    result_store_area = storeArea
    storeArea = {}  # Reinicia a variável para uma nova chamada
    return result_store_area


# Função para leitura do QR Code e código de barras
# Função para leitura do QR Code e código de barras
# Função para leitura do QR Code e código de barras
def qr_code_and_barcode_reader():
    global last_read
    global storeArea
    camera_id = 1
    delay = 1

    qcd = cv2.QRCodeDetector()
    cap = cv2.VideoCapture(camera_id)
    bd = cv2.barcode.BarcodeDetector()

    while True:
        ret, frame = cap.read()
        if ret:
            ret_qr, decoded_info, points, _ = qcd.detectAndDecodeMulti(frame)
            ret_bc, decoded_infoB, _, pointsB = bd.detectAndDecodeWithType(frame)

            # Verifica se há QR Codes
            if ret_qr:
                for s, p in zip(decoded_info, points):
                    if s:
                        print("QRCODE", s)
                        last_read = s  # Atualiza o valor lido
                        color = (0, 255, 0)

                        timestamp = time.strftime("%Y%m%d%H%M%S")
                        human_timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                        print(f"Timestamp humano: {human_timestamp}")

                        image_format = "jpg"
                        image_name = f"{s}_{timestamp}.{image_format}"

                        # Chama a função de detecção de impurezas e atribui o resultado a storeArea
                        storeArea = impurity_detection("samples/predic/318-0382.jpg")

                        if last_read:
                            if len(storeArea) > 4:
                                result.config(text="Amostra contaminada")
                            else:
                                result.config(text="Amostra livre de impureza")

                            cap.release()
                            cv2.destroyAllWindows()
                            return
                    else:
                        color = (0, 0, 255)
                    frame = cv2.polylines(frame, [p.astype(int)], True, color, 8)

            # Verifica se há códigos de barras
            if ret_bc:
                for s, p in zip(decoded_infoB, pointsB):
                    if s:
                        print("BARCODE: ", s)
                        last_read = s  # Atualiza o valor lido

                        timestamp = time.strftime("%Y%m%d%H%M%S")
                        human_timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                        print(f"Timestamp humano: {human_timestamp}")

                        image_format = "jpg"
                        image_name = f"{s}_{timestamp}.{image_format}"

                        # Chama a função de detecção de impurezas e atribui o resultado a storeArea
                        storeArea = impurity_detection("samples/predic/318-0382.jpg")

                        if last_read:
                            if len(storeArea) > 4:
                                result.config(text="Amostra contaminada")
                            else:
                                result.config(text="Amostra livre de impureza")

                            cap.release()
                            cv2.destroyAllWindows()
                            return
                    else:
                        frame = cv2.polylines(frame, [p.astype(int)], True, (0, 255, 0), 3)

            if cv2.waitKey(delay) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()


# Função para iniciar o processo (leitura de QR Code e análise de impurezas)
def start_process():
    global storeArea
    # impurity_detection("samples/predic/318-0382.jpg") <- Está sendo feito em qr_code_and_barcode_reader()
    # Limpa a label de resultados
    result.config(text="")

    # Inicia a leitura
    qr_code_and_barcode_reader()

    # Agora, a variável last_read contém o valor lido
    if last_read:
        # Adiciona o print com o formato de data/hora humanos
        human_timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"Iniciando análise de impurezas em {human_timestamp}")

        # Realiza a análise de impurezas
        timestamp = time.strftime("%Y%m%d%H%M%S")
        image_format = "jpg"
        image_name = f"{last_read}_{timestamp}.{image_format}"

        # Atualiza o texto da label `name`
        name.config(text=image_name)

        impurity_detection("samples/predic/318-0382.jpg")
        # Atualiza a interface gráfica com o resultado da análise
        if len(storeArea) > 4:
            result.config(text="Amostra contaminada")
        else:
            result.config(text="Amostra livre de impureza")

        # Pausa a leitura contínua após a leitura do QR Code
        return

# Configurações da interface gráfica
window = Tk()
window.title('Análise de Amostras')
window.geometry('645x400')
window.minsize(645, 400)

# Nome da imagem = TAG + TimeStamp
name = Label(window, text='tag_timestamp.format', font=("Helvetica", 16))
name.grid(column=0, row=0, columnspan=3)

# Resultado da análise ("Amostra Contaminada" / "Amostra Livre de Impureza")
result = Label(window, text='', font=("Helvetica", 16))
result.grid(column=0, row=3, columnspan=3)

# Campo de exibição 1 - Máscara aplicada
image_canvas1 = Canvas(window, width=300, height=300, borderwidth=2, relief="solid")
image_canvas1.grid(column=0, row=1, sticky="nsew")

# Campo de exibição 2 - Binarização da imagem
image_canvas2 = Canvas(window, width=300, height=300, borderwidth=2, relief="solid")
image_canvas2.grid(column=2, row=1, sticky="nsew")

# Inicia o processo
start_button = Button(window, text="START", width=10, command=start_process, background="#f8f4f4")
start_button.grid(column=0, row=4)

# Encerra o processo
stop_button = Button(window, text='STOP', width=10, background="#f8f4f4")
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
window.columnconfigure(0, weight=1, minsize=300)
window.columnconfigure(2, weight=1, minsize=300)
window.rowconfigure(1, weight=1, minsize=300)
window.rowconfigure(4, weight=1)
window.mainloop()

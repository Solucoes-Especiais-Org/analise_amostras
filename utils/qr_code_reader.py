import cv2

class QRCodeReader:

	window_name = 'OpenCV QR Code'

	def __init__(self):
		self.camera_id = 1
		self.delay = 1
		self.qcd = cv2.QRCodeDetector()
		self.cap = cv2.VideoCapture(self.camera_id)
		self.bd = cv2.barcode.BarcodeDetector()

	def read_qr_code(self):

		while True:
			ret, frame = self.cap.read()
			if ret:
				ret_qr, decoded_info, points, _ = self.qcd.detectAndDecodeMulti(frame)
				if ret_qr:
					for s, p in zip(decoded_info, points):
						if s:
							print("QRCODE", s)
							color = (0, 255, 0)
						else:
							color = (0, 0, 255)
						frame = cv2.polylines(frame, [p.astype(int)], True, color, 8)
				#cv2.imshow(window_name, frame)
				ret_bc, decoded_infoB, _, pointsB = self.bd.detectAndDecodeWithType(frame)
				if ret_bc:
					frame = cv2.polylines(frame, pointsB.astype(int), True, (0, 255, 0), 3)
					for s, p in zip(decoded_infoB, pointsB):
						if s:
							print("BARCODE: ",s)
							frame = cv2.putText(frame, s, p[1].astype(int),cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2, cv2.LINE_AA)
				cv2.imshow(self.window_name, frame)
			if cv2.waitKey(self.delay) & 0xFF == ord('q'):
				break
		cv2.destroyWindow(self.window_name)
		return s

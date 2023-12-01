import cv2

camera_id = 1
delay = 1
window_name = 'OpenCV QR Code'

qcd = cv2.QRCodeDetector()
cap = cv2.VideoCapture(camera_id)
bd = cv2.barcode.BarcodeDetector()

while True:
	ret, frame = cap.read()
	if ret:
		ret_qr, decoded_info, points, _ = qcd.detectAndDecodeMulti(frame)
		if ret_qr:
			for s, p in zip(decoded_info, points):
				if s:
					print("QRCODE",s)
					color = (0, 255, 0)
				else:
					color = (0, 0, 255)
				frame = cv2.polylines(frame, [p.astype(int)], True, color, 8)
		#cv2.imshow(window_name, frame)
		ret_bc, decoded_infoB, _, pointsB = bd.detectAndDecodeWithType(frame)
		if ret_bc:
			frame = cv2.polylines(frame, pointsB.astype(int), True, (0, 255, 0), 3)
			for s, p in zip(decoded_infoB, pointsB):
				if s:
					print("BARCODE: ",s)
					frame = cv2.putText(frame, s, p[1].astype(int),cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2, cv2.LINE_AA)
		cv2.imshow(window_name, frame)
	if cv2.waitKey(delay) & 0xFF == ord('q'):
		break
cv2.destroyWindow(window_name)
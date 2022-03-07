import cv2
import pytesseract


img = cv2.imread('captcha/teste.png')
gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
(h, w) = gry.shape[:2]
gry = cv2.resize(gry, (w*2, h*2))
cls = cv2.morphologyEx(gry, cv2.MORPH_CLOSE, None)
thr = cv2.threshold(cls, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

filename = 'captcha/temp.png'
cv2.imwrite(filename, thr)


pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
text = pytesseract.image_to_string('captcha/temp.png')
print(text)
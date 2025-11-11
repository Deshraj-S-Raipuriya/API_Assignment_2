from PIL import Image
import pytesseract

# Path to tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\singh\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

img_path = "./tmp/test_screenshot.png"
img = Image.open(img_path)
text = pytesseract.image_to_string(img)
print("OCR text snippet:\n", text[:200])

if "invoice" in text.lower():
    print("Predicted: invoice")
elif "error" in text.lower() or "exception" in text.lower():
    print("Predicted: error_screen")
else:
    print("Predicted: other/profile or unknown")

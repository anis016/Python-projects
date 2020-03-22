# OCR (Optical Character Recognition)

* Setup `Tesseract` in Ubuntu
```bash
$ bash setup_tesseract.sh
```
* Download a OCR file
* Run the `ocr.py` to get the text from the image
```python
python ocr.py ocr.jpg
 ```

#### Requirements
```
pytesseract==0.3.3
opencv-python==4.2.0.32
```

TODO:
1. Integrate Flask for Web
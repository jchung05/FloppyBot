try:
    from PIL import Image, ImageEnhance, ImageOps, ImageMath
except ImportError:
    import Image, ImageEnhance, ImageOps, ImageMath
import pytesseract

import cv2
import numpy as np
import re

class Parser(object):
    def __init__(self):
        self.parsed_mvp = list()
        self.image = None

    def PILtoCV(self, image:Image):
        self.image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Read an image from OS, used for debugging
    def imageRead(self, image:str):
        try:
            self.image = cv2.imread(image)
        except:
            print("This image is busted")

    def invertRGB(self):
        self.image = cv2.bitwise_not(self.image)

    def toGrayScale(self):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    def inflateImage(self, fx:float, fy:float):
        self.image = cv2.resize(self.image, None, fx=fx, fy=fy, interpolation=cv2.INTER_CUBIC)
    
    def reduceNoise(self):
        # self.image = cv2.threshold(cv2.GaussianBlur(self.image, (5, 5), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        # self.image = cv2.threshold(cv2.bilateralFilter(self.image, 5, 150, 150), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        # self.image = cv2.threshold(cv2.medianBlur(self.image, 1), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        self.image = cv2.threshold(self.image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


    # Take string block and parse for matching objects
    def parseScreenshot(self):
        MVP_PATTERN = r"MVP"
        CH_PATTERN = r"C[CH] *(\d{1,2})"
        TIME_PATTERN = r"XX[: ](\d{1,2})"

        str_block = pytesseract.image_to_string(self.image)
        str_list = str_block.splitlines()
        for s in str_list:
            s = s.upper()

            # Find regex objects or None
            mvp = re.search(MVP_PATTERN, s)
            channel = re.search(CH_PATTERN, s)
            time = re.search(TIME_PATTERN, s)

            if mvp and channel and time:
                self.parsed_mvp.append({time.group(1) : {"channel" : channel.group(1)}})

    def reset(self):
        self.image = None
        self.parsed_mvp = list()

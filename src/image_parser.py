try:
    from PIL import Image, ImageEnhance, ImageOps, ImageMath
except ImportError:
    import Image, ImageEnhance, ImageOps, ImageMath
import pytesseract, cv2, re
import numpy as np

# We do not use noise removal algorithms because that would eliminate : and .
class ImageParser(object):
    def __init__(self, path):
        self.parsed_mvp = list()
        self.image = None
        pytesseract.pytesseract.tesseract_cmd = path

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

    # Mask/saturate background colors away so their grayscale values don't truncate text
    # Yellow backgrounds have BGR of 30,188,228
    def maskImage(self):
        # TODO: Narrow the yellow bounds because text is being eroded
        lower = np.array([50,50,50], dtype = "uint16")
        upper = np.array([245,190,255], dtype = "uint16")
        mask = cv2.inRange(self.image, lower, upper)
        self.image = cv2.bitwise_and(self.image, self.image, mask=mask)
        cv2.imwrite('screenshots/image_masked.png', self.image)
    
    def reduceNoise(self):
        # self.image = cv2.threshold(cv2.GaussianBlur(self.image, (5, 5), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        # self.image = cv2.threshold(cv2.bilateralFilter(self.image, 5, 150, 150), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        # self.image = cv2.threshold(cv2.medianBlur(self.image, 1), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        pass

    def thresholding(self):
        self.image = cv2.threshold(self.image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    def dilate(self):
        kernel = np.ones((5,5),np.uint8)
        return cv2.dilate(self.image, kernel, iterations = 1)

    def erode(self):
        kernel = np.ones((5,5),np.uint8)
        return cv2.erode(self.image, kernel, iterations = 1)

    #opening - erosion followed by dilation
    def opening(self):
        kernel = np.ones((5,5),np.uint8)
        return cv2.morphologyEx(self.image, cv2.MORPH_OPEN, kernel)

    def canny(self):
        return cv2.Canny(self.image, 100, 200)

    # Take string block and parse for matching objects
    def parseScreenshot(self):
        MVP_PATTERN = r"MVP"
        CH_PATTERN = r"C[CH] *(\d{1,2})"
        TIME_PATTERN = r"XX[: ]*(\d{2})"

        str_block = pytesseract.image_to_string(self.image)
        str_list = str_block.splitlines()
        for s in str_list:
            s = s.upper()

            # Find regex objects or None
            mvp = re.search(MVP_PATTERN, s)
            channel = re.search(CH_PATTERN, s)
            time = re.search(TIME_PATTERN, s)

            # TODO: Bound checking channel and time ints
            if mvp and channel and time:
                print("I found one!")
                self.parsed_mvp.append({time.group(1) : {"channel" : channel.group(1)}})

    def reset(self):
        self.image = None
        self.parsed_mvp = list()

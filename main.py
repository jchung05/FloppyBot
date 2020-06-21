import time
import os
import pyautogui
from datetime import datetime
from dotenv import load_dotenv

from bot import FloppyBot
from image_parser import ImageParser

"""
1.) Get the coordinates from dotenv
2.) Sleep 30 seconds
    a.) Take a screenshot with coordinates
    b.) Invoke Parser/Bot
3.) Every 450 seconds, cleanup garbage pile
"""

def main():
    load_dotenv()

    WEBHOOK = os.getenv('WEBHOOK_URL')
    ROLE = os.getenv('ROLE_ID')
    TESSERACT_PATH = os.getenv('TESSERACT_PATH')

    # region => (x,y,w,h)
    X = os.getenv('X')
    Y = os.getenv('Y')
    W = os.getenv('W')
    H = os.getenv('H')

    bot = FloppyBot(WEBHOOK, ROLE)
    p = ImageParser(r'{}/tesseract.exe'.format(TESSERACT_PATH))
    cleanup_counter = 1

    try:
        while True:
            start_time = datetime.now()
            print('{}: Parsing...'.format(start_time.strftime("%H:%M:%S")))

            ss = pyautogui.screenshot(region=(X,Y,W,H))

            for i in range(2):
                p.PILtoCV(ss)
                p.inflateImage(1.03,1.02)
                i and p.invertRGB() # Must run invert and non-invert to catch all text
                p.toGrayScale()
                p.reduceNoise()
                p.parseScreenshot()
                for timestamp in p.parsed_mvp:
                    for k,v in timestamp.items():
                        bot.enqueue(k,v)
                p.reset()

            bot.sendMessage()

            cleanup_counter += 1
            # 15 minute counter
            if cleanup_counter == 30:
                minute = int(start_time.strftime("%M")) # Any race conditions using the start_time here?
                bot.garbagePickup(minute)
                cleanup_counter = 1
            
            time_delta = 30 - (datetime.now() - start_time).total_seconds()
            time.sleep(time_delta)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
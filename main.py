import time
import os
import pyautogui
from datetime import datetime
from dotenv import load_dotenv

"""
1.) Get the coordinates from dotenv
2.) Sleep 30 seconds
    a.) Take a screenshot with coordinates
    b.) Invoke Parser/Bot
3.) Every 450 seconds
    a.) Take screenshot
    b.) Cleanup garbage pile
"""

load_dotenv()

WEBHOOK = os.getenv('WEBHOOK_URL')
ROLE = os.getenv('ROLE_ID')

# region => (x,y,w,h)
X = os.getenv('X')
Y = os.getenv('Y')
W = os.getenv('W')
H = os.getenv('H')

bot = FloppyBot(WEBHOOK, ROLE)
p = Parser()
cleanup_counter = 1

try:
    while True:
        start_time = datetime.now()
        print(f'{start_time.strftime("%H:%M:%S")}: Parsing...')

        ss = pyautogui.screenshot(region=(X,Y,W,H))

        p.PILtoCV(ss)
        p.inflateImage(1.03,1.02)
        p.invertRGB() # Must run invert and non-invert to catch all text
        p.toGrayScale()
        p.reduceNoise()
        p.parseScreenshot()
        for time in p.parsed_mvp:
            for k,v in time.items():
                bot.enqueue(k,v)
        p.reset()

        bot.sendMessage()

        cleanup_counter += 1
        # 15 minute counter
        if cleanup_counter == 30:
            minute = int(start_time.strftime("%M")) # Any race conditions using the start_time here?
            bot.garbagePickup(minute)
            cleanup_counter = 1
        
        time_delta = (datetime.now() - start_time).total_seconds()
        time.sleep(30 - time_delta)
except KeyboardInterrupt:
    pass

# FloppyBot
Discord bot and client script for OCR capturing MVP timestamps in Maplestory Reboot server. Requires Python3.5+

# How to Use:
  * Fill out the .env file in the folder
  * Run the `run.sh`
  * Start MapleStory

# Three modules

## Client
  The main body is located here and will screenshot and fire off a discord check every 30 seconds to parse for images.

## FloppyBot
  The discord bot checks the announcement queue every 30 seconds. When there are announcements it will fire
  the announcement off to the discord server and then move the announcement over to a garbage pile so that
  future image parses can check against the garbage pile for duplicate matches. The garbage pile is cleaned
  up every 15 minutes.

## ScreenshotParser
  CURRENTLY UNTRAINED. Tesseract/OpenCV image parsing module. Will check for any screenshots in the specified
  folder and parse them. The requirements for a successful push to the announcement queue are currently:
  
   * 'mvp' or 'MVP'
   * 'cc<number>' or 'ch<number'
   * 'xx:<number>'
  
  Things to improve via training for later:
  
   * Parsing names
   * Better accuracy for character recognition ('n' and 'h', 'I' and 'l', etc)
   * A GUI for user input for variables

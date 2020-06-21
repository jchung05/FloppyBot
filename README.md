# FloppyBot
Discord bot and client script for OCR capturing MVP timestamps in Maplestory Reboot server. Requires Python3.5+ and Tesseract installed

# Required Installations
  [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki) - When you specify which folder you are downloading to, copy that into the .env file under TESSERACT_PATH

  [Python3.5+](https://www.python.org/downloads/) - Needed to run the bot!

  [Cygwin](http://www.cygwin.com/) - Needed to run the script to build everything!

  **OPTIONAL**[MouseLocator](http://efigureout.com/free-utility-to-locate-mouse-cursor-position/) - Needed (for now) to specify coordinates of the external chat box

# How to Use:
  * Clone or download me!
  * Fill out the .env file in the folder
  * Start MapleStory
  * Open a Command Prompt with admin privileges and navigate to the folder location
  * Run the command `bash run.sh` and leave MapleStory on main focus (preferably with the chat box in front of a black background
  * To kill the program, go back to the Command Prompt and press Ctrl+C

# Three modules

## Client
  The main body is located here and will screenshot and fire off a discord check every 30 seconds to parse for images.

## FloppyBot
  The discord bot checks the announcement queue every 30 seconds. When there are announcements it will fire
  the announcement off to the discord server and then move the announcement over to a garbage pile so that
  future image parses can check against the garbage pile for duplicate matches. The garbage pile is cleaned
  up every 15 minutes.

## ImageParser
  CURRENTLY UNTRAINED. Tesseract/OpenCV image parsing module. Will check for any screenshots in the specified
  folder and parse them. The requirements for a successful push to the announcement queue are currently:
  
   * 'mvp' or 'MVP'
   * 'cc<number>' or 'ch<number'
   * 'xx:<number>'
  
  Things to improve via training for later:
  
   * Parsing names
   * Better accuracy for character recognition ('n' and 'h', 'I' and 'l', etc)
   * A GUI for user input for variables

# Troubleshoot
  You may run into some problems. That's expected because nobody programs on Windows! Here are a few and what to do:

## No Tesseract Path
  `pytesseract.pytesseract.TesseractNotFoundError: tesseract is not installed or it's not in your PATH` means your path to Tesseract is incorrect. Double check its location and copy the string correctly!

## Windows Thinks It Knows Better Than You
  You will likely see something like `run.sh: line 4: /your/path/to/Python/python: Permission denied`. If you do it's because Windows has its own special Python aliases. Please refer to [this StackOverflow solution](https://stackoverflow.com/a/57168165/4596298) for instructions on how to disable them.

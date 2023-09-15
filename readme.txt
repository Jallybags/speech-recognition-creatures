Script to take voice input then type it out, with keys to turn on/off, and accept/reject output, and some settings specific to Creatures (mainly a max phrase length and typing delay)

Tested on Windows 10, with Cretures/Creatures 2/Creatures 3 (though the settings were made for Creatures 2)

Uses python, and the packages
keyboard PyAutoGUI pynput SpeechRecognition vosk

Needs a vosk model (https://alphacephei.com/vosk/models) (put in same directory as speech_recognition_creatures.py and call the folder "model")

How I run it on Windows:
py -m speech_recognition_creatures.py

Parameters in the speech_recognition_creatures.py file

######################
USAGE: ########
If using Vosk: Download and extract a Vosk model folder, rename it "model" and place it in this script's location (vosk-model-small-en-us-0.15 works well for me)
If using Google (doesn't work as well for me): need an internet connection
Press LISTEN_KEY and your speech will be recorded, press END_LISTEN_KEY and your recorded speech will be transcribed
It will then be typed, as if by the keyboard, by this script
If it is incorrect, press CANCEL_KEY, and a number of backspaces corresponsing to the length of the text will be typed
If it is correct, press CONFIRM_KEY, and subsequent presses of the CANCEL_KEY will not remove anything (this is enter as that also says the text in Creatures)
Press SUSPEND_KEY and the program will not listen or cancel until you press UNSUSPEND_KEY
Need to run as administrator if Creatures is running as administrator (it's pynput that needs this)
Make sure main program (e.g. "Creatures 2 - NornName") is active, and not an applet, or the words typed won't be sent to the main program
END USAGE ######
######################

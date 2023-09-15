Script to take voice input then type it out, with keys to turn on/off, and accept/reject output, and some settings specific to Creatures (mainly a max phrase length and typing delay)

Tested on Windows 10, with Cretures/Creatures 2/Creatures 3 (though the settings were made for Creatures 2)

Uses python, and the packages
keyboard PyAutoGUI pynput SpeechRecognition vosk

Needs a vosk model (https://alphacephei.com/vosk/models) (put in same directory as speech_recognition_creatures.py and call the folder "model")

How I run it on Windows:
py -m speech_recognition_creatures.py

Parameters in the speech_recognition_creatures.py file

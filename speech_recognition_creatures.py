import sys
import pyautogui
import speech_recognition as sr
from hotkey_recognizer import Hotkey_Recognizer
from pynput.keyboard import Key, Listener
import keyboard
import winsound
import vosk
import re
import json
import time

######################
####### USAGE ########
######################

# If using Vosk: Download and extract a Vosk model folder, rename it "model" and place it in this script's location (vosk-model-small-en-us-0.15 works well for me)
# If using Google (doesn't work as well for me): need an internet connection
# Press LISTEN_KEY and your speech will be recorded, press END_LISTEN_KEY and your recorded speech will be transcribed
# It will then be typed, as if by the keyboard, by this script
# If it is incorrect, press CANCEL_KEY, and a number of backspaces corresponsing to the length of the text will be typed
# If it is correct, press CONFIRM_KEY, and subsequent presses of the CANCEL_KEY will not remove anything (this is enter as that also says the text in Creatures)
# Press SUSPEND_KEY and the program will not listen or cancel until you press UNSUSPEND_KEY
# Need to run as administrator if Creatures is running as administrator (it's pynput that needs this)
# Make sure main program (e.g. "Creatures 2 - NornName") is active, and not an applet, or the words typed won't be sent to the main program

######################
##### END USAGE ######
######################

######################
##### PARAMETERS #####
######################

STT_ENGINE     = "VOSK"		 # What stt engine to use, VOSK and GOOGLE atm, but you can add others easily to the "def get_transcript" function below

CANCEL_KEY     = Key.shift_l # pynput key   : enters a number of backspaces equal to the length of the entered text
LISTEN_KEY     = Key.shift_r # pynput key   : starts listening operation
END_LISTEN_KEY = 'shift'     # keyboard key : ends listening operation
CONFIRM_KEY    = Key.enter   # pynput key   : confirms entered text (i.e. text cannot be cancelled)
SUSPEND_KEY    = Key.alt_l   # pynput key   : listen/cancel cannot be called when suspended
UNSUSPEND_KEY  = Key.alt_gr  # pynput key   : unsuspends, listen/cancel can be called
ESCAPE_KEY     = Key.esc     # pynput key   : quits program

MAXCHAR        = 35          # Max text input length for Creatures 2

INPUT_DELAY    = 0.1         # Delay for keyboard input from script in seconds, Creatures 2 drops inputs if too small

LISTEN_DELAY   = 0.25        # minimum delay in seconds between end of listening operation and start of new listening operation

USE_SOUND      = True        # plays beeps of varying frequencies depending on which operation runs
SOUND_DURATION = 100         # millisecomds
CANCEL_FREQ    = 250
LISTEN_FREQ    = 500
LISTENED_FREQ  = 600
CONFIRM_FREQ   = 1000
SUSPEND_FREQ   = 150
UNSUSPEND_FREQ = 200

######################
### END PARAMETERS ###
######################


active = True
pyautogui.PAUSE = INPUT_DELAY
length = 0
last_listen = time.time()
r = Hotkey_Recognizer()

def get_transcript(audio):
	if(STT_ENGINE=="VOSK"):
		return json.loads(r.recognize_vosk(audio))["text"]
	elif(STT_ENGINE=="GOOGLE"):
		s = r.recognize_google(audio)
		return re.sub(r'[^A-Za-z0-9 ]+', '', s).lower()
	else:
		return ""

print("Using " + STT_ENGINE)
with sr.Microphone() as source:
	print("Calibrating ambient noise...")
	r.adjust_for_ambient_noise(source)
	print("Ambient noise calibrated.")
	def on_press(key): 
		global length
		global last_listen
		global active
		if(key==ESCAPE_KEY):
			print("Exiting program")
			exit()
		if(key==SUSPEND_KEY and active==True and length==0):
			if(USE_SOUND):
				winsound.Beep(SUSPEND_FREQ, SOUND_DURATION)
			print("Suspended")
			active = False
		if(key==UNSUSPEND_KEY and active==False):
			if(USE_SOUND):
				winsound.Beep(UNSUSPEND_FREQ, SOUND_DURATION)
			print("Un-suspended")
			active = True
		if(key==ESCAPE_KEY):
			print("Exiting program")
			exit()
		if(key==CONFIRM_KEY and length>0):
			if(USE_SOUND):
				winsound.Beep(CONFIRM_FREQ, SOUND_DURATION)
			print("Confirmed")
			length = 0
		if(key==Key.backspace):
			print("Backspace")
			length = max(0,length-1)
		if(active):
			if(key==CANCEL_KEY and length>0):
				if(USE_SOUND):
					winsound.Beep(CANCEL_FREQ, SOUND_DURATION)
				print("Cancelled")
				print(length)
				for i in range(length):
					pyautogui.write("\b")
					#keyboard.send('backspace')
				length = 0
			elif(key==LISTEN_KEY and time.time()-last_listen>LISTEN_DELAY):
				last_listen = time.time()
				if(USE_SOUND):
					winsound.Beep(LISTEN_FREQ, SOUND_DURATION)
				print("Listening...")
				audio = r.listen(source,END_LISTEN_KEY)
				try:
					s = get_transcript(audio)
					print("Transcript: " + s)
					if(length==0):
						for i in range(min(len(s),MAXCHAR)):
							pyautogui.write(s[i])
						length = min(MAXCHAR,length+len(s))
					else:
						if(length<MAXCHAR):
							pyautogui.write(" ")
							length = min(MAXCHAR,length+1)
						for i in range(min(len(s),MAXCHAR-length)):
							pyautogui.write(s[i])
						length = min(MAXCHAR,length+len(s))
				except sr.UnknownValueError:
					print("Could not understand audio")
				except sr.RequestError as e:
					print("Could not request results")
				last_listen = time.time()
				winsound.Beep(LISTENED_FREQ, SOUND_DURATION)
	with Listener(on_press=on_press) as listener: 
		listener.join()

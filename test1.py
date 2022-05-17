import speech_recognition as sr
from playsound import playsound
import RPi.GPIO as GPIO
import time

power_button = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(power_button, GPIO.OUT)
GPIO.output(power_button, GPIO.LOW)

print(sr.__version__)
recognizer = sr.Recognizer()
# mic = sr.Microphone()
# print(sr.Microphone.list_microphone_names())
mic = sr.Microphone(device_index=1)


def some_cool_thing(words):
	words = words.lower()
	if words == "magic mirror turn on":
		print("Turning On Magic Mirror!")
		GPIO.output(power_button, GPIO.HIGH)
		time.sleep(1)
		GPIO.output(power_button, GPIO.LOW)
	elif words == "magic mirror turn off":
		print("Turning Off Magic Mirror!")
		GPIO.output(power_button, GPIO.HIGH)
		time.sleep(1)
		GPIO.output(power_button, GPIO.LOW)
	elif words == "i love the beach" or words in "i love the beach":
		print(words)
		playsound('steppin.mp3')


while True:
	print("Waiting for Speech...")

	with mic as source:
		recognizer.adjust_for_ambient_noise(source)
		audio = recognizer.listen(source)

	response = {
		"success": True,
		"error": None,
		"transcription": None
	}

	try:
		response["transcription"] = recognizer.recognize_google(audio)
		some_cool_thing(response["transcription"])
	except sr.RequestError:
		# API was unreachable or unresponsive
		response["success"] = False
		response["error"] = "API unavailable"
	except sr.UnknownValueError:
		# speech was unintelligible
		response["error"] = "Unable to recognize speech"

	print(response)
	print()
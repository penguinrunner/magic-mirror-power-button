import speech_recognition as sr
# from playsound import playsound
import RPi.GPIO as GPIO
import time
from gtts import gTTS
import os
import requests
import json
import datetime

GPIO.setwarnings(False)
path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)

api_key = "YOUR_API_KEY"
lon = "-82.5154"
lat = "40.7584"
weaher_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=imperial"
weaher_url_forcast = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=imperial"

language = 'en'
tld = 'com'
# tld = 'co.uk'
# tld = 'com.au'
# tld = 'ie'

power_button = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(power_button, GPIO.OUT)
GPIO.output(power_button, GPIO.LOW)

print(sr.__version__)
recognizer = sr.Recognizer()
# mic = sr.Microphone()
# print(sr.Microphone.list_microphone_names())
mic = sr.Microphone(device_index=1)

def get_weather():
	response = requests.get(weaher_url).json()
	# print(json.dumps(response, indent=4))
	current = response['main']['temp']
	city = response['name']
	description = response['weather'][0]['description']
	mytext = f"Currently in {city}, it is {current} degrees and {description}"
	myobj = gTTS(text=mytext, lang=language, slow=False, tld=tld)
	myobj.save(path + "/tts.mp3")
	os.system(f"mpg321 {path}/tts.mp3")


def get_weather_forcast():
	response = requests.get(weaher_url_forcast).json()
	print(json.dumps(response, indent=4))
	with open('forcast.json','w+') as outfile:
		json.dump(response,outfile,indent=4)

	with open('forcast.json','r') as infile:
		data = json.load(infile)

	all_days = {}
	forcast_data = {}
	for each_date in data['list']:
		this_date = each_date['dt']
		millseconds = this_date
		this_date = datetime.datetime.fromtimestamp(millseconds)

		if not this_date.date() in all_days:
			all_days[this_date.date()] = [each_date]
		else:
			these_days = all_days[this_date.date()]
			these_days.append(each_date)
			all_days[this_date.date()] = these_days


		for each_date in all_days:
			max_temp = -50
			min_temp = 100
			descriptions = {}
			# print('**',each_date)

			for each_forcast in all_days[each_date]:
				# print(each_forcast)
				if float(each_forcast['main']['temp_max']) > max_temp:
					max_temp = float(each_forcast['main']['temp'])

				if float(each_forcast['main']['temp_min']) < min_temp:
					min_temp = float(each_forcast['main']['temp'])

			print(f"Max temp for {each_date} is {max_temp} and the min is {min_temp}")
## new
			forcast_data[each_date] = {'high':max_temp,'low':min_temp}
		print(forcast_data)

		text=""
		i = 0
		for each_date in forcast_data:
			if i == 0:
				this_day = "today"
			elif i == 1:
				this_day = "tomorrow"
			else:
				break
			i+=1

			text = text + f"The high for {this_day} will be {forcast_data[each_date]['high']}, and the low will be {forcast_data[each_date]['low']}. "
		print(text)

	myobj = gTTS(text=text, lang=language, slow=False, tld=tld)
	myobj.save(path + "/tts.mp3")
	os.system(f"mpg321 {path}/tts.mp3")




def some_cool_thing(words):
	words = words.lower()
	if words == "magic mirror turn on":
		print("Turning On Magic Mirror!")

		mytext = 'Turning on your Mirror!'
		myobj = gTTS(text=mytext, lang=language, slow=False,tld=tld)
		myobj.save(path + "/tts.mp3")
		os.system(f"mpg321 {path}/tts.mp3")

		GPIO.output(power_button, GPIO.HIGH)
		time.sleep(1)
		GPIO.output(power_button, GPIO.LOW)
	elif words == "magic mirror turn off":
		print("Turning Off Magic Mirror!")

		mytext = 'Turning off your Mirror!'
		myobj = gTTS(text=mytext, lang=language, slow=False,tld=tld)
		myobj.save(path + "/tts.mp3")
		os.system(f"mpg321 {path}/tts.mp3")

		GPIO.output(power_button, GPIO.HIGH)
		time.sleep(1)
		GPIO.output(power_button, GPIO.LOW)

	elif words == "i love the beach" or words in "i love the beach":
		mytext = 'Well, you asked for it!'
		myobj = gTTS(text=mytext, lang=language, slow=False,tld=tld)
		myobj.save(path + "/tts.mp3")
		os.system(f"mpg321 {path}/tts.mp3")
		os.system(f"mpg321 {path}/steppin.mp3")
		print(words)

	elif words == "what is the meaning of life" or words in "what is the meaning of life":
		mytext = 'The meaning of life is. forty two'
		myobj = gTTS(text=mytext, lang=language, slow=False,tld=tld)
		myobj.save(path + "/tts.mp3")
		os.system(f"mpg321 {path}/tts.mp3")
		print(words)

	elif words == "what is love" or words in "what is love":
		mytext = "Baby don't hurt me. don't hurt me. No more."
		myobj = gTTS(text=mytext, lang=language, slow=False,tld=tld)
		myobj.save(path + "/tts.mp3")
		os.system(f"mpg321 {path}/tts.mp3")
		print(words)

	elif words == "what is the weather" or words in "what is the weather":
		get_weather()

	elif words == "what is the forecast" or words in "what is the forecast":
		get_weather()
		get_weather_forcast()


# get_weather_forcast()

print()
print()
print()
mytext = 'Magic Mirror is Ready!'
myobj = gTTS(text=mytext, lang=language, slow=False,tld=tld)
myobj.save(path+"/tts.mp3")
os.system(f"mpg321 {path}/tts.mp3")

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
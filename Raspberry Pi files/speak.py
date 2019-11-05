import os

def speak_currency(currency, confidence):
	try:
		cmd = 'espeak -ven+f4 -s180 "I think this is ." --stdout |aplay'
		cmd += '&& espeak -ven+f4 -s120 "' + str(currency) + '" --stdout |aplay'
		cmd += '&& espeak -ven+f4 -s180 " with ' + str(confidence) + '% confidence ." --stdout |aplay'
		for _ in range(1):
			os.system(cmd)
		#espeak "hello world" --stdout |aplay
	except Exception as e:
		print(e)

def speak(message):
	try:
		cmd = 'espeak -ven+f4 -s180 "'+ message +'" --stdout |aplay'
		for _ in range(1):
			os.system(cmd)
	except Exception as e:
		print(e)
			
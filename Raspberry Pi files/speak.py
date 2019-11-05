import os
currency = 2000
confidence = 99.93
cmd = 'espeak -ven+f4 -s180 "I think this is ." --stdout |aplay'
cmd += '&& espeak -ven+f4 -s120 "' + str(currency) + '" --stdout |aplay'
cmd += '&& espeak -ven+f4 -s180 " with ' + str(confidence) + '% confidence ." --stdout |aplay'
for _ in range(1):
	os.system(cmd)
#espeak "hello world" --stdout |aplay
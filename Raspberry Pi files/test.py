import tensorflow as tf
from numpy import expand_dims, array, float32
#from tensorflow.keras.preprocessing import image
#import importlib
from os import listdir
import cv2
import capture, preprocess
import json

with open('config.json') as config_file:
    config = json.load(config_file)

# capture = getattr(importlib.import_module("capture"), "capture")
# init_cam = getattr(importlib.import_module("capture"), "init_cam")
# release_cam = getattr(importlib.import_module("capture"), "release_cam")
# preprocess_captured = getattr(importlib.import_module("preprocess"), "preprocess_captured")
#is_object_present = getattr(importlib.import_module("preprocess"), "is_object_present")

if config['capture_enabled']:
	cam = capture.init_cam(config["camera_device_str"])
	if cam == None:
		print("Error opening camera. Exiting.. ")
		exit

model_name = config["model_name"]
classes = {0: 'fifty_2',
            1: 'five',
            2: 'fivehundred_2',
            3: 'hundred',
            4: 'hundred_2',
            5: 'ten_2',
            6: 'twenty_2',
            7: 'twohundred',
            8: 'twothousand'}
# Load TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(model_path=model_name + ".tflite")
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


# Test model on input data.
input_shape = input_details[0]['shape']
#print(input_shape)
while True:
	t = input("Exit? [N/y] : ")
	if t=='n' or t=='N' or t=='':
		pass
	else:
		if config['capture_enabled']:
			capture.release_cam(cam)
		break
	if config['capture_enabled']:
		capture.capture(cam, display_enabled = config["display_enabled"], 
		capture_count = config["capture_count"], capture_delay = config["capture_delay"])
	if config['preprocess_enabled']:
		preprocess.preprocess_captured()

	for f in listdir("preprocessed/"):
		#img = image.load_img("preprocessed/" + f, target_size=tuple(input_shape[1:3]))
		img = cv2.imread("preprocessed/" + f) 
		img = cv2.resize(img, tuple(input_shape[1:3]))
		input_data = array(img, dtype=float32)
		input_data /= 255.
		input_data = expand_dims(input_data, axis=0)
		interpreter.set_tensor(input_details[0]['index'], input_data)

		interpreter.invoke()

		# The function `get_tensor()` returns a copy of the tensor data.
		# Use `tensor()` in order to get a pointer to the tensor.
		output_data = interpreter.get_tensor(output_details[0]['index'])
		bestclass = 0
		output_data = output_data[0]
		for i in range(len(output_data)):
			if (output_data[i] > output_data[bestclass]):
				bestclass = i
		print(classes[bestclass], "Confidence : %.2f" % output_data[bestclass])
		#os.remove("input/"+f)


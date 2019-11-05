import tensorflow as tf
import numpy.expand_dims, np.array
#from tensorflow.keras.preprocessing import image
#import importlib
import os.listdir
import cv2
import capture, preprocess

# capture = getattr(importlib.import_module("capture"), "capture")
# init_cam = getattr(importlib.import_module("capture"), "init_cam")
# release_cam = getattr(importlib.import_module("capture"), "release_cam")
# preprocess_captured = getattr(importlib.import_module("preprocess"), "preprocess_captured")
#is_object_present = getattr(importlib.import_module("preprocess"), "is_object_present")

cam = capture.init_cam()

model_name = "cnn_l2_5_full"
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
		capture.release_cam(cam)
		break
	
	capture.capture(cam)
	preprocess.preprocess_captured()

	for f in os.listdir("preprocessed/"):
		#img = image.load_img("preprocessed/" + f, target_size=tuple(input_shape[1:3]))
		img = cv2.imread("preprocessed/" + f) 
		img = cv2.resize(img, tuple(input_shape[1:3]))
		input_data = np.array(img, dtype=np.float32)
		input_data /= 255.
		input_data = np.expand_dims(input_data, axis=0)
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


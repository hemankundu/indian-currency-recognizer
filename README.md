# Indian Paper Currency Recognizer
An image classification project done using ConvNet. This project is deployable to Raspberry Pi (or any mobile device with TensorFlow lite support). This tool will help visually impaired people to identify paper currency.

The model training part is done in Ipython notebook offered by [Google Colab](https://colab.research.google.com/). And dataset is used from [Google Drive](https://www.google.com/drive/), directly mounting drive to the virtual environment provided by Colab. Notebooks are shared in this repo. 

**There will be two parts of this project:**

# 1. Model building, training, testing, evaluating
## 1.1 Requirements
- [TensorFlow](https://www.tensorflow.org/) (To build the model)
- [shutil](https://docs.python.org/3/library/shutil.html) (Offers a number of high-level operations on files. Used to Copy, Move data files.) 
- [OpenCV](https://opencv.org/) (For processing and manipulating images)

## 1.2 Dataset  
Dataset can be found [here](https://drive.google.com/open?id=18QousObkRQCB-pTxHYid1Ju0ffgbX2OW) in my Google Drive. Kindly first see the directory structure below. 
### Setup
- Clone my data folder from the given link to your drive or download if using local machine
- Mount your drive if using cloud environment
- Set `drive_path` accordingly

### Directory structure:
<details><summary>See</summary>
  
    ├──  dataset_all
    │    ├── done
    │    ├── pending
    │    ├── tmp  
    │    │   └──currency
    │    │      ├── training
    │    │      │    ├── <image_name>.jpg
    │    │      │    └── ...
    │    │      └── testing
    │    │           ├── <image_name>.jpg
    │    │           └── ...
    │    ├── <model_name>.json
    │    ├── ...
    │    ├── <model_name>.h5
    │    ├── ...
    │    ├── <model_name>.tflite
    │    └── ...
    │
    ├──  dataset_plain
    │    ├── done
    │    ├── pending
    │    ├── tmp  
    │    │   └──currency
    │    │      ├── training
    │    │      │    ├── <image_name>.jpg
    │    │      │    └── ...
    │    │      └── testing
    │    │           ├── <image_name>.jpg
    │    │           └── ...
    │    ├── <model_name>.json
    │    ├── ...
    │    ├── <model_name>.h5
    │    ├── ...
    │    ├── <model_name>.tflite
    │    └── ...
    │
</details>
  
### Directory explained:
- `dataset_all` has images with natural background (eg. image containing currency as well as other objects in background)
- `dataset_plain` has images with only currency notes with a black background (cropping only the currency later will be easy)
- `done` has images has been used for training
- `pending` has images are left to train / test on (may be added new data later)
- `tmp` has the actual preprocessed (only currency cropped) images, containg train, test sub directories
- `currency` is sub directory of `tmp`, extra
- `training` has images to train on
- `testing` has images to test on

   
## 1.3 Modeling
### To train own model:
- Build a model
- Assign model to `built_model`

Example
```Python
built_model = tf.keras.models.Sequential([
tf.keras.layers.Conv2D(),
tf.keras.layers.MaxPool2D(), ...])
```
### To use trained model:
- Change `model_name` to target model's name
- Model with weights saved (.h5) 
     
     Choose a `saved_version` <details><summary>There are three versions of each model </summary>
       
     `full` - model architecture and weights, manually saved

     `auto` - model architecture and weights, automatic saved using `ModelCheckpoint` callback

     `w` - only weights are saved 
       
     </details>
  
  * Load the model
  
  * Example
     ```python
     saved_version = "full"
     loaded_model = tf.keras.models.load_model(drive_path + "dataset_plain/"  + model_name + '_'+ saved_version +'.h5')
     ```
   
- Model with only architecture saved (.json)
     
  * Load the model
  
  * Example
     ```python
     json_file = open(drive_path + "dataset_plain/" + model_name + ".json", 'r')
     loaded_model_json = json_file.read()
     json_file.close()
     built_model = tf.keras.models.model_from_json(loaded_model_json)
     ```
## 1.4 Converting model to tflite version
Here we will use `lite.TFLiteConverter.from_keras_model_file()` to convert our model to [lite](https://www.tensorflow.org/lite) version

- Choose a `model_name` (.h5) file
- Convert and save

 Example
```python
from tensorflow import lite
converter = lite.TFLiteConverter.from_keras_model_file(drive_path + "dataset_plain/" + model_name + '_full.h5')
tfmodel = converter.convert()
open (drive_path + "dataset_plain/" + model_name + "_full.tflite" , "wb").write(tfmodel)
``` 

# 2. Work on Raspberry Pi
## 2.1 Requirements
- [OpenCV](https://opencv.org/) (For capturing, processing and manipulating images)
- [tflite-runtime](https://www.tensorflow.org/lite/guide/build_rpi) (Build or use pre-compiled package for Raspberry Pi)
- [NumPy](https://pypi.org/project/numpy/)
- [espeak](https://www.dexterindustries.com/howto/make-your-raspberry-pi-speak/) (To convert text or strings into spoken words)
## 2.2 Directory Structure and purpose
- `captured` this directory contains images captured by the camera 
- `preprocessed` this directory contains cropped currency images
- `models` this directory contains trained `.tflite` models. `model_name` can be changed in `config.json`
- `config.json` contains configurations 
- `requrements.txt` has list of required packages
- `test.py` main program which handles all sub tasks like capturing image, processing image, predicting, and provide audio output
- `capture.py` handles image  capturing task
- `preprocess.py` cropping the currency from captured image and other adjustments
- `speak.py` handles audio output
## 2.3 Setup
- Install required packages (Using virtual env recommended see [here](https://www.geeksforgeeks.org/python-virtual-environment/))
	```bash
	pip3 install --user --requirement requirements.txt
	```
- Edit configuration file if necessary ( `config.json` )
- Run `test.py`
	
  ```Bash
	python3 test.py
	```

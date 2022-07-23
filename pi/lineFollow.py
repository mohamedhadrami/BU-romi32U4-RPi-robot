from tflite_runtime.interpreter import Interpreter 
from PIL import Image
import numpy as np
import cv2, time, sys, imutils, argparse
from a_star import AStar
a_star = AStar()
import subprocess
from time import sleep
from picamera.array import PiRGBArray
from picamera import PiCamera
#from keras.preprocessing.image import img_to_array

def predict(image):
    def load_labels(path): # Read the labels from the text file as a Python list.
        with open(path, 'r') as f:
            return [line.strip() for i, line in enumerate(f.readlines())]

    def set_input_tensor(interpreter, image):
        tensor_index = interpreter.get_input_details()[0]['index']
        input_tensor = interpreter.tensor(tensor_index)()[0]
        input_tensor[:, :] = image

    def classify_image(interpreter, image, top_k=1):
        set_input_tensor(interpreter, image)   

        interpreter.invoke()
        output_details = interpreter.get_output_details()[0]
        output = np.squeeze(interpreter.get_tensor(output_details['index']))

        scale, zero_point = output_details['quantization']
        output = scale * (output - zero_point)

        ordered = np.argpartition(-output, 1)
        return [(i, output[i]) for i in ordered[:top_k]][0]

    def control_robot(lbl):
        d = 1
        if lbl =='left':
            a_star.motors(0,50)
            sleep(d)
            a_star.motors(0,0)
        elif lbl =='right':
            a_star.motors(50,0)
            sleep(d)
            a_star.motors(0,0)
        elif lbl =='straight':
            a_star.motors(50,50)
            sleep(d)
            a_star.motors(0,0)
        elif lbl =='bag':
            a_star.motors(0,0)
        return ""

    data_folder = "/home/pi/RPi-Romi-Robot/pi/data/"

    model_path = data_folder + "new.tflite"
    label_path = data_folder + "labels.txt"

    interpreter = Interpreter(model_path)
    print("Model Loaded Successfully.")

    interpreter.allocate_tensors()
    _, height, width, _ = interpreter.get_input_details()[0]['shape']
    print("Image Shape (", width, ",", height, ")")

    # Load an image to be classified.
    img = image #Image.open(data_folder + "image.jpg").convert('RGB').resize((width, height))

    output_details = interpreter.get_output_details()
    input_data = np.expand_dims(img, axis=0)
    #print(input_data)

    # feed data to input tensor and run the interpreter
    #interpreter.set_tensor(input_details[0]['index'], input_data)
    set_input_tensor(interpreter, img)
    interpreter.invoke()

    # Obtain results and map them to the classes
    predictions = interpreter.get_tensor(output_details[0]['index'])[0]

    top_k_results = 4
    # Get indices of the top k results
    top_k_indices = np.argsort(predictions)[::-1][:top_k_results]

    with open(label_path, 'r') as f:
        labels = list(map(str.strip, f.readlines()))

    for i in range(top_k_results):
        pred=predictions[top_k_indices[i]]/255.0
        pred=round(pred,5)
        #pred=int(pred * 10000)/10000
        #'{:.4f}'.format(pred)
        lbl=labels[top_k_indices[i]]
        #print(lbl, "=", pred*100, "%")

    pred_max=predictions[top_k_indices[0]]/255.0
    lbl_max=labels[top_k_indices[0]]

    print("Guess: "+lbl_max)
    print("-----------------")
    control_robot(lbl_max)


if __name__ == "__main__":
    try:
        #mc.stop()
        # initialize the camera and grab a reference to the raw camera capture
        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 32
        rawCapture = PiRGBArray(camera, size=(640, 480))
        # allow the camera to warmup
        time.sleep(0.1)
        # capture frames from the camera

        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            # grab the raw NumPy array representing the image, then initialize the timestamp
            # and occupied/unoccupied text
            image = frame.array
            # show the frame
            #key = cv2.waitKey(1) & 0xFF
            image = cv2.resize(image, (180, 180))
            #image = img_to_array(image)
            #image = np.array(image, dtype="float") / 255.0
            #image = image.reshape(-1, 28, 28, 3)
            #cv2.imshow("Frame", image[0])
            predict(image)
            # clear the stream in preparation for the next frame
            rawCapture.truncate(0)
    except KeyboardInterrupt:
        sys.exit()
        a_star.motors(0,0)
        camera.close()
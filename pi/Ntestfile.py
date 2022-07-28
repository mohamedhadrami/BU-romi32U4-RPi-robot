from tflite_runtime.interpreter import Interpreter 
from PIL import Image
import numpy as np
import time
from a_star import AStar
a_star = AStar()
import subprocess
from time import sleep
import time
from picamera import PiCamera
from time import sleep
from PIL import Image
d=1

while True:
  start_time = time.time()
  subprocess.call(['/home/pi/RPi-Romi-Robot/pi/camera.py'])
  """camera = PiCamera()
  #take pictures every second for 10 seconds and store to known location
  #cmd = "raspistill -t 50000 -tl 500 -o /home/pi/RPi-Romi-Robot/pi/data/raspistill/image7%02d.jpg"
  #subprocess.call(cmd, shell=True)

  camera.resolution = (1600, 1200)
  #camera.crop = (0.25, 0.25, 0.5, 0.5)
  sleep(0.01)
  camera.capture('/home/pi/RPi-Romi-Robot/pi/data/image.jpg')
  
  
  im = Image.open('/home/pi/RPi-Romi-Robot/pi/data/image.jpg').convert('RGB')
  width, height = im.size
  left = width/10
  top = 4*height/6
  right = width-width/10
  bottom = height
  im = im.crop((left, top, right, bottom))
  im.save('/home/pi/RPi-Romi-Robot/pi/data/image.jpg')
  """
  #camera.close()

  #print("--- %s seconds ---" % (time.time() - start_time))
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

  def action(lbl):
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
  img = Image.open(data_folder + "image.jpg").convert('RGB').resize((width, height))
  """
  # Classify the image.
  time1 = time.time()
  label_id, prob = classify_image(interpreter, image)
  time2 = time.time()
  classification_time = np.round(time2-time1, 3)
  print("Classificaiton Time =", classification_time, "seconds.")
  # Read class labels.
  labels = load_labels(label_path)
  # Return the classification label of the image.
  classification_label = labels[label_id]
  print("Image Label is :", classification_label)
  """
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
  print("-")

  action(lbl_max)
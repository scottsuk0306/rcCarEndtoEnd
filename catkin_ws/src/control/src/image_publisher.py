#! /usr/bin/env python

import rospy
from std_msgs.msg import Int16, Image
import os
from tensorflow.keras.models import load_model
from keras.preprocessing import image
import cv2
import rospy
import numpy as np
from cv_bridge import CvBridge, CvBridgeError

def main():
    dataset_path = "~/rcCarEndtoEnd/"
    model_path = os.path.join(dataset_path,"model/PilotNet_v1-004-0.02398.h5")
    model = load_model("../PilotNet_v1-001-0.04877.h5")
    print("Model is ready!")

if __name__ == '__main__':
    dataset_path = "~/rcCarEndtoEnd/data01-26-test2/"
    
    df = pd.read_csv("./train_dataset.csv")
    for image_name in df['image_name']:
         = cv2.imread(os.path.join(dataset_path + image))
    X_train = np.array([img_to_arr(os.path.join(dataset_path, image_name)) for image_name in df['image_name']])
    
    model = load_model("../PilotNet_v1-001-0.04877.h5")
    print("Model is ready!")
    # df = pd.read_csv(dataset_path)
    # img_path = img_to_arr(os.path.join(dataset_path, df['image_name'][0]))
    image_name = "../sample_image.jpeg"
    sample_img = Image.open(image_name)
    sample_img = load_numpy_image(sample_img)
    result = model.predict(sample_img)
    # round result to integer value
    result = int(round((result*800)+1100))
    print result
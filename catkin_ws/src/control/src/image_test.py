#! /usr/bin/env python

from tensorflow.keras.models import load_model
import os
import pandas as pd
import numpy as np
from PIL import Image
import cv2

def img_to_arr(p):
    with image.load_img(p) as img:
        img = image.img_to_array(img)
    return img

def normalize(img):
    img[:,:,0] -= 100
    img[:,:,0] /= 64

    img[:,:,1] -= 99
    img[:,:,1] /= 63

    img[:,:,2] -= 98
    img[:,:,2] /= 65   
    return img

def load_numpy_image(img):
    num_img = np.array(img)
    num_img = normalize(num_img)
    num_img = np.expand_dims(num_img, 0)
    return num_img

def main():
    dataset_path = "~/rcCarEndtoEnd/"
    model_path = os.path.join(dataset_path,"model/PilotNet_v1-004-0.02398.h5")
    model = load_model("../PilotNet_v1-001-0.04877.h5")
    print("Model is ready!")

if __name__ == '__main__':
    dataset_path = "~/rcCarEndtoEnd/"
    model_path = os.path.join(dataset_path,"model/PilotNet_v1-004-0.02398.h5")
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
import numpy as np
import cv2
import os
import random
import matplotlib.pyplot as plt
import pickle
from rembg import remove
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import requests
from io import BytesIO
from urllib.request import urlopen


def predict_product(img_url):
    categories=['asustuf','cadbury','cocacola','colgate','dell','iphone','kitkat','lays','lifebuoy','milkbikis','nikeshoes','nivea','pepsi','rolexwatch','vicks']
    def preprocess_image(image_path):
          with urlopen(image_path) as response:
            img_data = response.read()
            img = cv2.imdecode(np.frombuffer(img_data, np.uint8), cv2.IMREAD_COLOR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (224, 224))
            img = remove(img)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            img = img / 255.0
            return img
    model = load_model('FlaskApp/ProductModel.h5')
    img = preprocess_image(img_url)
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    predictions = model.predict(img)
    print(predictions)
    predicted_class = np.argmax(predictions)
    print(f"Predicted Class: {predicted_class}")
    print("Predicted Product :",categories[predicted_class])
    return categories[predicted_class],np.max(predictions)
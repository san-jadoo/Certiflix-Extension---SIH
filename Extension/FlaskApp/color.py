import cv2
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

def color_detection(image_path, k=3):
    # Read the image
    image = cv2.imread(image_path)
   
    # Convert the image from BGR to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
   
    # Reshape the image to be a list of pixels
    pixels = image.reshape((-1, 3))
   
    # Apply KMeans clustering to find dominant colors
    kmeans = KMeans(n_clusters=k, n_init=10)
    kmeans.fit(pixels)
   
    # Get the dominant colors and their counts
    dominant_colors = kmeans.cluster_centers_.astype(int)
    color_counts = np.bincount(kmeans.labels_)
   
    # Get the index of the most dominant color
    dominant_color_index = np.argmax(color_counts)
   
    # Get the RGB values of the most dominant color
    dominant_color = dominant_colors[dominant_color_index]
   
    # Define a mapping of common color names to RGB triplets
    color_mapping = {
        "Yellow": [255, 255, 0],
        "Orange": [255, 165, 0],
        "Violet": [238, 130, 238],
        "Light Green": [144, 238, 144],
        "Brown": [165, 42, 42],
        "Pink": [255, 192, 203],
        "Sky Blue": [135, 206, 250],
        "Purple": [128, 0, 128],
        "Red":[255, 0, 0],
        "Green":[0, 255, 0],
        "Blue":[0, 0, 255],
        "White":[255, 255, 255],
        "Black":[0, 0, 0],
        "Golden": [255, 215, 0]
    }
   
    def find_closest_color_name(rgb_triplet):
        min_distance = float('inf')
        closest_color_name = None
        for name, color_value in color_mapping.items():
            distance = np.linalg.norm(np.array(color_value) - np.array(rgb_triplet))
            if distance < min_distance:
                min_distance = distance
                closest_color_name = name
        return closest_color_name
    common_color_name = find_closest_color_name(dominant_color)
   
    return common_color_name

def main(image_path,desc):
    dominant_common_color_name = color_detection(image_path)
    print(f"Color: {dominant_common_color_name}")
    if dominant_common_color_name in desc :
         print ("Colour Matched")
    else :
         print ("Colour Mismatch")
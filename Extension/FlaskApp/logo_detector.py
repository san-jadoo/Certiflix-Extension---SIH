import torch
from PIL import Image
import requests
from io import BytesIO
def detect_logo(img_url):
    categories=categories=['asustuf','cadbury','cocacola','colgate','dell','iphone','kitkat','lays','lifebuoy','milkbikis','nikeshoes','nivea','pepsi','rolexwatch','vicks']
    model=torch.hub.load('ultralytics/yolov5:master','custom','FlaskApp/best.pt')
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))
    results=model(img)
    predictions=results.xyxy[0].cpu().numpy()
    if(len(predictions)!=0):
        return categories[int(predictions[0][-1])]
    else:
        return ""
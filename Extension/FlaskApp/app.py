from flask import Flask, request, jsonify
import os
import requests
import cv2
import numpy as np
from color import main
from urllib.parse import urljoin
from selenium import webdriver
from bs4 import BeautifulSoup
from product_model import predict_product
from logo_detector import detect_logo
import easyocr
from textDesc import desc_match
from textDesc import imgtxt_match
from flask_cors import CORS
from io import BytesIO
from PIL import Image


app = Flask(__name__)
CORS(app)

@app.route('/receive-url', methods=['POST'])
def receive_url():
    try:
        data = request.get_json()
        url = data.get('url')

        if not url:
            raise ValueError('Missing URL in the request.')

        print(f'Received URL: {url}')
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        driver.implicitly_wait(10)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        img_tags = soup.find_all('img', class_='q6DClP')
        count=0
        p=[]
        ans=""
        for img_tag in img_tags:
            img_url = img_tag.get('src')
            new_dimensions = "832/832"
            img_url = img_url.replace("128/128", new_dimensions)
            img_url = urljoin(url, img_url)
            if(count<2):
                 predicted_product,productprob = predict_product(img_url)
                 p.append(predicted_product)
                 if(count==0):
                      predicted_logo=detect_logo(img_url)
                      print("Logo Detected : ",predicted_logo)
                      response = requests.get(img_url)
                      img = Image.open(BytesIO(response.content))
                      reader = easyocr.Reader(['en'])
                      result = reader.readtext(img)
                      recognized_text = [entry[1] for entry in result]
                      print(recognized_text)
                      for i in recognized_text:
                           ans+=" "
                           ans+=i
            count=count+1
            if(count==2):
                break
        print("Extracted Text : ",ans)
        name = soup.find_all('span', class_='B_NuCI')
        print(name[0].text)
      #  img_data = response.read()
       # img = cv2.imdecode(np.frombuffer(img_data, np.uint8), cv2.IMREAD_COLOR)
      #  a=main(img,name[0].text)
        driver.quit()
        if predicted_logo=="":
            predicted_logo="aaa"
        if(p[0]==p[1] and predicted_logo==p[1]):
            if (predicted_product=="dell" or predicted_product=="asustuf" or predicted_product=="iphone"):
                 tval=desc_match(name[0].text,predicted_product)
            else:
                 tval=imgtxt_match(name[0].text,ans)
            print("Threshold - ",tval)
            if(tval>=0.80):
                return jsonify({'status': 'success', 'message': f'Received Image URL: {img_url}', 'predicted_product': p[0],'probprod':productprob})
            else:
                return jsonify({'status': 'partial3', 'message': f'Received Image URL: {img_url}', 'predicted_product': p[0],'predicted_logo':predicted_logo})
        elif(p[0]==p[1] and predicted_logo!=p[1] and predicted_logo=="aaa"):
            return jsonify({'status': 'partial1', 'message': f'Received Image URL: {img_url}', 'predicted_product': p[0]})
        elif(p[0]==p[1] and predicted_logo!=p[1]):
            return jsonify({'status': 'partial2', 'message': f'Received Image URL: {img_url}', 'predicted_product': p[0],'predicted_logo':predicted_logo})
        elif(p[0]!=p[1]):
            return jsonify({'status': 'failed', 'message': f'Received Image URL: {img_url}', 'predicted_product1': p[0],'predicted_product2': p[1]})

    except Exception as e:
        # Example response indicating an error
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

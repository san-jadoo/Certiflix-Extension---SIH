from flask import Flask, request, jsonify
from product_model import predict_product
from logo_detector import detect_logo
import easyocr
from fuzzywuzzy import fuzz
from PIL import Image
from flask_cors import CORS
from PIL import Image


app = Flask(__name__)
CORS(app)

@app.route('/receive-image', methods=['POST'])
def receive_image():
        try:
             uploaded_file = request.files['image']
             pname = request.form['name']
             pdesc = request.form['description']
             uploaded_file.save('image/temp_image.jpg')
             print(uploaded_file)
             img_path = r'image/temp_image.jpg'
             predicted_product = predict_product(img_path)
             print("Predicted Product : ",predicted_product)
             if(predicted_product.lower()==pname.lower()):
                   predicted_logo=detect_logo(img_path)
                   print("Logo Detected : ",predicted_logo)
                   if(predicted_logo.lower()==pname.lower()):
                        reader = easyocr.Reader(['en'])
                        img = Image.open(img_path)
                        print("")
                        result = reader.readtext(img,detail=0)
                        print(result)
                        ans=""
                        for i in result:
                             ans+=i
                             ans+=" "
                        if(fuzz.ratio(ans.lower(),pdesc.lower())>=45):
                            return jsonify({'status': 'success','predicted_product': pname})
                        else:
                            return jsonify({'status': 'partial3'})
                   else:
                        if(len(predicted_logo)==0):
                            return jsonify({'status': 'partial2'})
                        else:
                            return jsonify({'status': 'partial1'})
             else:
                  return jsonify({'status': 'failed'})     
        except Exception as e:
                  return jsonify({'status': 'error', 'message': str(e)})
            

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

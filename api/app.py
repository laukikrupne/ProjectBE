import os
from flask import Flask, flash, request, redirect, url_for, jsonify, render_template
from werkzeug.utils import secure_filename
from flask_restful import Api, Resource
import numpy as np
import cv2
import keras
from keras.models import load_model
from keras import backend as K

app = Flask(__name__)
api = Api(app)

class plant_deficiency(Resource):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    dict = {"[0]": "Apple___Apple_scab", 
            "[1]": "Apple___Black_rot",
            "[2]": "Apple___Cedar_apple_rust",
            "[3]": "Apple___healthy",
            "[4]": "Blueberry___healthy",
            "[5]": "Cherry_(including_sour)___Powdery_mildew",
            "[6]": "Cherry_(including_sour)___healthy",
            "[7]": "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
            "[8]": "Corn_(maize)___Common_rust_",
            "[9]": "Corn_(maize)___Northern_Leaf_Blight",
            "[10]": "Corn_(maize)___healthy",
            "[11]": "Grape___Black_rot",
            "[12]": "Grape___Esca_(Black_Measles)",
            "[13]": "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
            "[14]": "Grape___healthy",
            "[15]": "Orange___Haunglongbing_(Citrus_greening)",
            "[16]": "Peach___Bacterial_spot",
            "[17]": "Peach___healthy",
            "[18]": "Pepper,_bell___Bacterial_spot",
            "[19]": "Pepper,_bell___healthy",
            "[20]": "Potato___Early_blight",
            "[21]": "Potato___Late_blight",
            "[22]": "Potato___healthy",
            "[23]": "Raspberry___healthy",
            "[24]": "Soybean___healthy",
            "[25]": "Squash___Powdery_mildew",
            "[26]": "Strawberry___Leaf_scorch",
            "[27]": "Strawberry___healthy",
            "[28]": "Tomato___Bacterial_spot",
            "[29]": "Tomato___Early_blight",
            "[30]": "Tomato___Late_blight",
            "[31]": "Tomato___Leaf_Mold",
            "[32]": "Tomato___Septoria_leaf_spot",
            "[33]": "Tomato___Spider_mites Two-spotted_spider_mite",
            "[34]": "Tomato___Target_Spot",
            "[35]": "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
            "[36]": "Tomato___Tomato_mosaic_virus",
            "[37]": "Tomato___healthy"}
    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    def post(self):
        # receives posted image
        #   file = request.files['file'].read()
        r = request
        # convert string of image data to uint8
        nparr = np.fromstring(r.data, np.uint8)
        # decode image
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        classifier = load_model('./models/128_vgg_16.h5')
        image = cv2.resize(img, (128, 128), interpolation = cv2. INTER_LINEAR)
        image = image / 255.
        image = image.reshape(1,128,128,3)
        res = str(np.argmax(classifier.predict(image, 1, verbose = 0), axis=1))
        K.clear_session()
        result = self.dict[res]
        ret = "OK"
        retMap = {
            'Message': ret,
            'Status Code': 200,
            'Deficiency': result
        }
        return jsonify(retMap)

api.add_resource(plant_deficiency,"/plant_deficiency")

@app.route('/')
def hello_world():
    return "Hello World!"

if __name__=="__main__":
    app.run(debug=True)

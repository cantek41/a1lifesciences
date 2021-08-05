# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 12:27:37 2021

@author: cantek
"""
from flask import Flask
from flask import jsonify, request
from joblib import dump, load
from flask_cors import CORS, cross_origin

bins = [0,2,4,7,13,18,30,45,110]
labels = [1,2,3,4,5,6,7,8]

model = load(r"model.joblib")
scaler = load(r"scaler.joblib")

def pred(data):    
    #preprocess       
    for i,e in enumerate(bins):
        if data[0]<=e:
            data.append(labels[i])
            break           
    
    data.append(-0.04*data[0]+2.5) 
    
    data = scaler.transform([data])
    
    pred = model.predict_proba(data.reshape(1,-1))
    return pred
    
    
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@cross_origin()
@app.route('/predict', methods = ["POST"])
def predict():
    print("predict")
    json_data = request.json
    data = json_data["data"]
    data = pred(data)
    print(data)
    data = {"No":data[0][0],"Yes":data[0][1]}
    return data


if __name__ == '__main__':
    app.run(debug=True)

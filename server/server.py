from flask import Flask, request, jsonify, send_from_directory
from . import util
import os

# app = Flask(__name__)
app = Flask(__name__, static_folder='../client', static_url_path='/')

util.load_saved_artifacts()

@app.route('api/get_location_names')
def get_location_names():
    response = jsonify({
        'locations':util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('api/predict_home_price', methods=['POST'])
def get_estimated_price():
    total_sqft = float(request.form['total_sqft'])
    location = request.form['location']
    bath = int(request.form['bath'])
    bhk = int(request.form['bhk'])
  
    response = jsonify({
        'estimated_price':util.get_estimated_price(location, total_sqft, bhk, bath)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/hello')
def hello():
    return "Hello World from Flask Server!"

@app.route("/", defaults={'path': ''})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'app.html')

# if __name__ == "__main__":
#     print("Starting Python Flask Server for Home Price Prediction...")
#     util.load_saved_artifacts()
#     app.run()
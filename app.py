from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json
import os
import pandas as pd

DATA_FOLDER = './data/'
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)
app = Flask(__name__)
cors = CORS(app)
CORS(app, resources={r"/api": {"origins": "*"}})
#CORS(app, resources={r"/api/*": {"origins": "https://cheery-licorice-787f04.netlify.app/"}})
app.config['CORS_HEADERS'] = 'Content-Type'

# Load your TTL data into the RDFLib Graph
""" @app.route('/api', methods=['GET'])
@cross_origin()
def api():
    print("I got you")
    return jsonify({'data': 'from the other side'}) """

@app.route('/api', methods=['POST', 'OPTIONS'])
#@cross_origin()
def putActivityData():
    if request.method == 'OPTIONS':
        response = jsonify({})
    elif request.method == 'POST':
        data = request.get_json()  # Assuming the data is sent as JSON
        #
        for sample in data:
            gyro_df = pd.DataFrame(sample['gyroscope_data'])
            gyro_df['label'] = sample['label']

            timestamp = sample['gyroscope_data'][0]['timestamp'] if len(sample['gyroscope_data']) > 0 else 0
            gyro_df.to_csv(os.path.join(DATA_FOLDER, 'gyro_' + str(timestamp) + '.csv'), index=False)

            motion_df = pd.DataFrame(sample['motion_data']) 
            motion_df['label'] = sample['label']

            timestamp = sample['motion_data'][0]['timestamp'] if len(sample['motion_data']) > 0 else 1
            motion_df.to_csv(os.path.join(DATA_FOLDER, 'motion_' + str(timestamp) + '.csv'), index=False)
        # Process the data as needed
        response = jsonify({
            'data': "Done!"#
        })
    else:
        response = jsonify({
            'data': "Invalid request method"#
        })
    
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5999)
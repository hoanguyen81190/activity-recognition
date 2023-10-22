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
            print("I got a query", sample)
            df = pd.DataFrame(sample['data'])
            df['label'] = sample['label']

            timestamp = sample['data'][0]['timestamp']
            df.to_csv(os.path.join(DATA_FOLDER, str(timestamp) + '.csv'), index=False)
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
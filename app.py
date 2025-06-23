from flask import Flask, request, jsonify
from model import predict_log

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    if not request.json:
        return jsonify({'error': 'No input data provided'}), 400

    try:
        # Example expected input:
        # {
        #   "url": "/search?q='OR 1=1-- -",
        #   "firedtimes": 1,
        #   "level": 6
        # }

        input_data = {
            "url": request.json['url'],
            "firedtimes": request.json['firedtimes'],
            "level": request.json['level']
        }

        result = predict_log(input_data)
        return jsonify({'prediction': result})

    except KeyError as e:
        return jsonify({'error': f'Missing field: {str(e)}'}), 400

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

EXPECTED_FEATURES = 45

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/herb/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        if 'features' not in data:
            return jsonify({
                "code": "400",
                "message": "Missing 'features' in request data",
                "result data": None
            }), 400

        features = data['features']

        if len(features) != EXPECTED_FEATURES:
            return jsonify({
                "code": "400",
                "message": f"Expected {EXPECTED_FEATURES} features, but got {len(features)}.",
                "result data": None
            }), 400

        features_array = np.array(features)

        features_array = features_array.reshape(1, -1)

        prediction = model.predict(features_array)

        return jsonify({
            "code": "200",
            "message": "Prediction successful",
            "result data": {
                "prediction": prediction.tolist()
            }
        }), 200

    except Exception as e:
        return jsonify({
            "code": "500",
            "message": str(e),
            "result data": None
        }), 500

if __name__ == '__main__':
    app.run(debug=True)

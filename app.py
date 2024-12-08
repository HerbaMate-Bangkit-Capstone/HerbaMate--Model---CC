from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

df = pd.read_csv('dataset.csv')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/herb/predict', methods=['POST'])
def recommend_plants():
    selected_symptoms = request.json.get('symptoms', [])

    if not selected_symptoms:
        return jsonify({
            'code': 400,
            'message': 'No symptoms provided',
            'data': None
        }), 400

    recommended_plants = []

    for index, row in df.iterrows():
        plant_symptoms = row['symptoms'].split(',')
        if any(symptom in plant_symptoms for symptom in selected_symptoms):
            recommended_plants.append({
                'herbs': row['herbs'],
                'latin_name': row['latin_name'],
                'symptoms': plant_symptoms,
                'usage_method': row['usage_method']
            })

    if not recommended_plants:
        return jsonify({
            'code': 404,
            'message': 'No plants match the selected symptoms',
            'data': None
        }), 404

    recommended_plants.sort(key=lambda x: x['latin_name'], reverse=True)

    return jsonify({
        'code': 200,
        'message': 'Successfully recommended plants',
        'data': recommended_plants
    }), 200

if __name__ == '__main__':
    app.run(debug=True)

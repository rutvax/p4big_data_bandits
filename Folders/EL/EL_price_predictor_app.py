from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import pickle
from keras.models import load_model

app = Flask(__name__, static_url_path='/static')
CORS(app)

# @app.route('/', methods=['GET'])
# def home():
#     return 'copy/paste this to the end: /predict'

@app.route('/', methods=['POST'])
def predict():
    if request.method == 'POST':
        input_data = request.json

        # Load the model
        with open('EL_machine_learning_model.pkl', 'rb') as file:
            model = pickle.load(file)

        def predict_nightly_rate(input_data):
            preprocessed_df = pd.DataFrame([input_data])

            preprocessed_df = pd.get_dummies(preprocessed_df, columns=['room_type', 'bathroom_type', 'neighbourhood'], prefix=['room_type', 'bathroom_type', 'neighbourhood'])
        
            preprocessed_df = preprocessed_df[['room_type_Entire home/apt', 'room_type_Hotel room', 'room_type_Private room', 'room_type_Shared room', 'accommodates', 'bedrooms',
                            'beds', 'bathrooms', 'bathroom_type_private', 'bathroom_type_shared', 'neighbourhood_Brooklyn', 'neighbourhood_Manhattan', 'neighbourhood_Queens',
                            'wifi', 'smoke_alarm', 'carbon_monoxide_alarm', 'kitchen', 'air_conditioning', 'tv', 'iron','essentials', 'hangers', 'shampoo', 'refrigerator', 
                            'hair_dryer', 'dishes_and_silverware', 'hot_water', 'cooking_basics', 'heating', 'bed_linens', 'microwave', 'oven', 'fire_extinguisher', 'coffee_maker',
                            'free_street_parking', 'first_aid_kit', 'self_check_in', 'dedicated_workspace']]

            cols_to_int = ['room_type_Entire home/apt', 'room_type_Hotel room', 'room_type_Private room', 'room_type_Shared room', 'accommodates', 'bedrooms',
                            'beds', 'bathroom_type_private', 'bathroom_type_shared', 'neighbourhood_Brooklyn', 'neighbourhood_Manhattan', 'neighbourhood_Queens',
                            'wifi', 'smoke_alarm', 'carbon_monoxide_alarm', 'kitchen', 'air_conditioning', 'tv', 'iron','essentials', 'hangers', 'shampoo', 'refrigerator', 
                            'hair_dryer', 'dishes_and_silverware', 'hot_water', 'cooking_basics', 'heating', 'bed_linens', 'microwave', 'oven', 'fire_extinguisher', 'coffee_maker',
                            'free_street_parking', 'first_aid_kit', 'self_check_in', 'dedicated_workspace']
        
            preprocessed_df[cols_to_int] = preprocessed_df[cols_to_int].astype('int64')
            preprocessed_df['bathrooms'] = preprocessed_df['bathrooms'].astype('float64')

            # Convert the preprocessed DataFrame to JSON
            input_json = preprocessed_df.to_json(orient='records')
            input_json = json.loads(input_json)  # Convert to Python object

            # Make the prediction
            prediction = model.predict(input_json)

            return prediction

        prediction = predict_nightly_rate(input_data)
        
        return jsonify({'predicted_rate': prediction[0]})

        pass

if __name__ == '__main__':
    app.run(debug=True)

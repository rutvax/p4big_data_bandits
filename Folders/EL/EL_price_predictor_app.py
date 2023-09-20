from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import pandas as pd
from keras.models import load_model
# import traceback
# import joblib
# import pickle


app = Flask(__name__)
CORS(app)

nn = load_model('EL_machine_learning_model.h5')
print('Model loaded successfully!')

@app.route('/', methods=['GET'])
def home():
    return (
        f"Home Page.</br>"
        f"This is where the model should load and predict: /predict"
    )

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if nn:    
            json_ = request.json
            print(json_)

            query = pd.DataFrame([json_])
            print(f"Converted JSON to Pandas DataFrame for preprocessing...")
            # print(query.head(5))

            ### Preprocess input data
            # One-hot encoding for 'room_type'
            query['room_type_Entire home/apt'] = (query['room_type'] == 'Entire home/apt').astype(int)
            query['room_type_Hotel room'] = (query['room_type'] == 'Hotel room').astype(int)
            query['room_type_Private room'] = (query['room_type'] == 'Private room').astype(int)
            query['room_type_Shared room'] = (query['room_type'] == 'Shared room').astype(int)

            # One-hot encoding for 'bathroom_type'
            query['bathroom_type_private'] = (query['bathroom_type'] == 'Private').astype(int)
            query['bathroom_type_shared'] = (query['bathroom_type'] == 'Shared').astype(int)

            # One-hot encoding for 'neighbourhood'
            query['neighbourhood_Brooklyn'] = (query['neighbourhood'] == 'Brooklyn').astype(int)
            query['neighbourhood_Manhattan'] = (query['neighbourhood'] == 'Manhattan').astype(int)
            query['neighbourhood_Queens'] = (query['neighbourhood'] == 'Queens').astype(int)

            # Drop the original categorical columns
            query = query.drop(['room_type', 'bathroom_type', 'neighbourhood'], axis=1)
            print(f"Completed get_dummies processing...")
            print(query.dtypes)

            # Reorder columns 
            query = query[['room_type_Entire home/apt', 'room_type_Hotel room', 'room_type_Private room', 'room_type_Shared room', 'accommodates', 'bedrooms',
                                'beds', 'bathrooms', 'bathroom_type_private', 'bathroom_type_shared', 'neighbourhood_Brooklyn', 'neighbourhood_Manhattan', 'neighbourhood_Queens',
                                'wifi', 'smoke_alarm', 'carbon_monoxide_alarm', 'kitchen', 'air_conditioning', 'tv', 'iron','essentials', 'hangers', 'shampoo', 'refrigerator', 
                                'hair_dryer', 'dishes_and_silverware', 'hot_water', 'cooking_basics', 'heating', 'bed_linens', 'microwave', 'oven', 'fire_extinguisher', 'coffee_maker',
                                'free_street_parking', 'first_aid_kit', 'self_check_in', 'dedicated_workspace']]
            print(f"Reordered columns to align with machine learning model...")
            
            # Reset data types 
            query = query.astype('int64')
            query['bathrooms'] = query['bathrooms'].astype('float64')
            print(f"Changed datatypes of most columns to integers, of 'bathrooms' to float...")

            # Make the prediction
            prediction = float(nn.predict(query)[0][0])
            print(f"Prediction: {prediction}")

            app.logger.info(f'Input Data: {json_}')
            app.logger.info(f'Processed Input: {query}')
            app.logger.info(f'Prediction: {prediction}')

            return jsonify({'prediction': str(prediction)})

        else:
            return jsonify({'error': 'Model not loaded'})

    except Exception as e:
        print ('Train the model first')
        return jsonify({'error': str(e)})
    

if __name__ == '__main__':
    try:
        port = int(sys.argv[1]) # This is for a command-line input
    except:
        port = 12345 # If you don't provide any port the port will be set to 12345

    print ('Model loaded successfully - I think.')
    
    app.run(port=port, debug=True)

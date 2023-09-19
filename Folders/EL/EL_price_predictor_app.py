from flask import Flask, request, jsonify
import pandas as pd
import pickle
import joblib

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predictPrice():
    # Load the machine learning model
    model = joblib.load('EL_machine_learning_model.pkl')
    
    json_ = request.json
    print(json_)
    
    # Process the input data and prepare it for prediction
    input_df = pd.DataFrame([json_])
    preprocessed_df = input_data.copy()

    preprocessed_df = pd.get_dummies(preprocessed_df, columns=['room_type', 'bathroom_type', 'neighbourhood_group'], prefix=['room_type', 'bathroom_type', 'neighbourhood'])
    
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

    # Model expects a list of features in a specific order
    model_input_data = [preprocessed_df['room_type_Entire home/apt'], 
                preprocessed_df['room_type_Hotel room'],
                preprocessed_df['room_type_Private room'],
                preprocessed_df['room_type_Shared room'],
                preprocessed_df['accommodates'],
                preprocessed_df['bedrooms'],
                preprocessed_df['beds'],
                preprocessed_df['bathrooms'],
                preprocessed_df['bathroom_type_private'],
                preprocessed_df['bathroom_type_shared'],
                preprocessed_df['neighbourhood_Brooklyn'],
                preprocessed_df['neighbourhood_Manhattan'],
                preprocessed_df['neighbourhood_Queens'],
                preprocessed_df['wifi'],
                preprocessed_df['smoke_alarm'],
                preprocessed_df['carbon_monoxide_alarm'],
                preprocessed_df['kitchen'],
                preprocessed_df['air_conditioning'],
                preprocessed_df['tv'],
                preprocessed_df['iron'],
                preprocessed_df['essentials'],
                preprocessed_df['hangers'],
                preprocessed_df['shampoo'],
                preprocessed_df['refrigerator'],
                preprocessed_df['hair_dryer'],
                preprocessed_df['dishes_and_silverware'],
                preprocessed_df['hot_water'],
                preprocessed_df['cooking_basics'],
                preprocessed_df['heating'],
                preprocessed_df['bed_linens'],
                preprocessed_df['microwave'],
                preprocessed_df['oven'],
                preprocessed_df['fire_extinguisher'],
                preprocessed_df['coffee_maker'],
                preprocessed_df['free_street_parking'],
                preprocessed_df['first_aid_kit'],
                preprocessed_df['self_check_in'],
                preprocessed_df['dedicated_workspace']
    ]

    # Make the prediction
    predicted_price = list(model.predict(preprocessed_df))

    return jsonify({'data': predicted_price})

if __name__ == '__main__':
    app.run(debug=True)

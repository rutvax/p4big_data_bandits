document.getElementById('inputForm').addEventListener('submit', function(event) {
    event.preventDefault();
        // Log a message to the console
        console.log('Button clicked!');
        // Gather the input values
        var room_type = document.getElementById('room_type').value;
        var accommodates = parseInt(document.getElementById('accommodates').value);
        var bedrooms = parseInt(document.getElementById('bedrooms').value);
        var beds = parseInt(document.getElementById('beds').value);
        var bathrooms = parseInt(document.getElementById('bathrooms').value);
        var bathroom_type = document.getElementById('bathroom_type').value;
        var neighbourhood = document.getElementById('neighbourhood').value;
        var wifi = document.getElementById('wifi').checked ? 1 : 0;
        var smoke_alarm = document.getElementById('smoke_alarm').checked ? 1 : 0;
        var carbon_monoxide_alarm = document.getElementById('carbon_monoxide_alarm').checked ? 1 : 0;
        var kitchen = document.getElementById('kitchen').checked ? 1 : 0;
        var air_conditioning = document.getElementById('air_conditioning').checked ? 1 : 0;
        var tv = document.getElementById('tv').checked ? 1 : 0;
        var iron = document.getElementById('iron').checked ? 1 : 0;
        var essentials = document.getElementById('essentials').checked ? 1 : 0;
        var hangers = document.getElementById('hangers').checked ? 1 : 0;
        var shampoo = document.getElementById('shampoo').checked ? 1 : 0;
        var refrigerator = document.getElementById('refrigerator').checked ? 1 : 0;
        var hair_dryer = document.getElementById('hair_dryer').checked ? 1 : 0;
        var dishes_and_silverware = document.getElementById('dishes_and_silverware').checked ? 1 : 0;
        var hot_water = document.getElementById('hot_water').checked ? 1 : 0;
        var cooking_basics = document.getElementById('cooking_basics').checked ? 1 : 0;
        var heating = document.getElementById('heating').checked ? 1 : 0;
        var bed_linens = document.getElementById('bed_linens').checked ? 1 : 0;
        var microwave = document.getElementById('microwave').checked ? 1 : 0;
        var oven = document.getElementById('oven').checked ? 1 : 0;
        var fire_extinguisher = document.getElementById('fire_extinguisher').checked ? 1 : 0;
        var coffee_maker = document.getElementById('coffee_maker').checked ? 1 : 0;
        var free_street_parking = document.getElementById('free_street_parking').checked ? 1 : 0;
        var first_aid_kit = document.getElementById('first_aid_kit').checked ? 1 : 0;
        var self_check_in = document.getElementById('self_check_in').checked ? 1 : 0;
        var dedicated_workspace = document.getElementById('dedicated_workspace').checked ? 1 : 0;

        // Call your function with the gathered inputs
        var inputData = {
            room_type,
            accommodates,
            bedrooms,
            beds,
            bathrooms,
            bathroom_type,
            neighbourhood,
            wifi,
            smoke_alarm,
            carbon_monoxide_alarm,
            kitchen,
            air_conditioning,
            tv,
            iron,
            essentials,
            hangers,
            shampoo,
            refrigerator,
            hair_dryer,
            dishes_and_silverware,
            hot_water,
            cooking_basics,
            heating,
            bed_linens,
            microwave,
            oven,
            fire_extinguisher,
            coffee_maker,
            free_street_parking,
            first_aid_kit,
            self_check_in,
            dedicated_workspace
        };
        
        // Call the function to send input data for prediction
        predictNightlyRate(inputData)
        .then(data => {
            console.log("Response from server:", data);
            
            if ('prediction' in data) {
                const prediction = parseFloat(data.prediction);
                
                if (!isNaN(prediction)) {
                    console.log("Suggested Nightly Rate:", prediction);
                    const roundedPrediction = Math.round(prediction); // Round to nearest whole number
                    const formattedPrediction = `$${roundedPrediction}`; // Add dollar sign

                    // Update the predictionValue element
                    document.getElementById('predictionValue').textContent = formattedPrediction;

                    // Show the predictionResult element
                    document.getElementById('predictionResult').style.display = 'block';

                } else {
                    console.error('Error: Invalid prediction value');
                }
            } else {
                console.error('Error: No prediction in response');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
});

// Function to send input data to the server for prediction
function predictNightlyRate(inputData) {
    return fetch('http://127.0.0.1:12345/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(inputData),
    })
    .then(response => response.json())
    .then(data => {
        console.log("Response from server:", data);

        if (typeof data.prediction === 'string') {
            data.prediction = JSON.parse(data.prediction);
        }

        return data;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

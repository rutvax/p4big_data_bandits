async function predictPrice() {
    // Get input values
    const room_type = document.getElementById('room_type').value;
    const accommodates = parseInt(document.getElementById('accommodates').value);
    const bedrooms = parseInt(document.getElementById('bedrooms').value);
    const beds = parseInt(document.getElementById('beds').value);
    const bathrooms = parseFloat(document.getElementById('bathrooms').value);
    const bathroom_type = document.getElementById('bathroom_type').value;
    const neighbourhood = document.getElementById('neighbourhood').value;

    // Get the state of each amenity
    const wifi = document.getElementById('wifi').checked ? 1 : 0;
    const smoke_alarm = document.getElementById('smoke_alarm').checked ? 1 : 0;
    const carbon_monoxide_alarm = document.getElementById('carbon_monoxide_alarm').checked ? 1 : 0;
    const kitchen = document.getElementById('kitchen').checked ? 1 : 0;
    const air_conditioning = document.getElementById('air_conditioning').checked ? 1 : 0;
    const tv = document.getElementById('tv').checked ? 1 : 0;
    const iron = document.getElementById('iron').checked ? 1 : 0;
    const essentials = document.getElementById('essentials').checked ? 1 : 0;
    const hangers = document.getElementById('hangers').checked ? 1 : 0;
    const shampoo = document.getElementById('shampoo').checked ? 1 : 0;
    const refrigerator = document.getElementById('refrigerator').checked ? 1 : 0;
    const hair_dryer = document.getElementById('hair_dryer').checked ? 1 : 0;
    const hot_water = document.getElementById('hot_water').checked ? 1 : 0;
    const cooking_basics = document.getElementById('cooking_basics').checked ? 1 : 0;
    const heating = document.getElementById('heating').checked ? 1 : 0;
    const bed_linens = document.getElementById('bed_linens').checked ? 1 : 0;
    const microwave = document.getElementById('microwave').checked ? 1 : 0;
    const oven = document.getElementById('oven').checked ? 1 : 0;
    const fire_extinguisher = document.getElementById('fire_extinguisher').checked ? 1 : 0;
    const coffee_maker = document.getElementById('coffee_maker').checked ? 1 : 0;
    const free_street_parking = document.getElementById('free_street_parking').checked ? 1 : 0;
    const first_aid_kit = document.getElementById('first_aid_kit').checked ? 1 : 0;
    const self_check_in = document.getElementById('self_check_in').checked ? 1 : 0;
    const dedicated_workspace = document.getElementById('dedicated_workspace').checked ? 1 : 0;

    // Send data to server for prediction
    const response = await fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
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
        })
    });

    if (response.ok) {
        const response_data = await response.json();
        const predictedPriceElement = document.getElementById('predictedPrice');
        predictedPriceElement.innerText = `Suggested Nightly Rate: $${response_data.predictedPrice}`;
    } else {
        console.error('Error:', response);
    }    
    
    // Display the predicted price
    // const predictedPriceElement = document.getElementById('predictedPrice');
    // predictedPriceElement.innerText = `Suggested Nightly Rate: $${data.predictedPrice}`;
}

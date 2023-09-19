import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import pandas as pd
from flask_cors import CORS
from flask import Flask, jsonify, Request


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/ny_airbnb.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Listings = Base.classes.merged_cleaned_ny
Reviews = Base.classes.reviews_cleaned_ny

df_amenities = pd.read_csv('//Resources/amenities.csv')

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
CORS(app)

#################################################
# Flask Routes
#################################################

@app.route("/")

def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/BigDataBandits/Listings<br/>"
        f"/api/BigDataBandits/Reviews<br/>"
        f"/api/BigDataBandits/Listings_unique<br/>"
        f"/api/BigDataBandits/amenities<br/>"
    )


@app.route("/api/BigDataBandits/Listings")
def listings():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of Listings data"""
    # Query all Listing data
    results = session.query(Listings.listing_id, Listings.listing_url, Listings.name, Listings.host_id, Listings.host_url, Listings.host_name, Listings.host_since, 
                            Listings.host_is_superhost, Listings.host_listings_count, Listings.host_total_listings_count, Listings.latitude, Listings.longitude, 
                            Listings.room_type, Listings.accommodates, Listings.bedrooms, Listings.beds, Listings.price, 
                            Listings.minimum_nights, Listings.maximum_nights, Listings.has_availability, Listings.number_of_reviews, Listings.number_of_reviews_ltm, 
                            Listings.number_of_reviews_l30d, Listings.first_review, Listings.last_review, Listings.review_scores_rating, Listings.calculated_host_listings_count, 
                            Listings.reviews_per_month, Listings.date, Listings.available, Listings.price, Listings.adjusted_price 
                            ).all()

    session.close()

    # Create a dictionary from the row data and append to a list of listing_data
    listing_data = []
    for listing_id, listing_url, name, host_id, host_url, host_name, host_since, host_is_superhost, host_listings_count, host_total_listings_count, latitude, longitude, room_type, accommodates, bedrooms, beds, price, minimum_nights, maximum_nights, has_availability, number_of_reviews, number_of_reviews_ltm, number_of_reviews_l30d, first_review, last_review, review_scores_rating, calculated_host_listings_count, reviews_per_month, date, available, price, adjusted_price in results:
        data_dict = {}
        data_dict["listing_id"] = listing_id
        data_dict["listing_url"] = listing_url
        data_dict["name"] = name
        data_dict["host_id"] = host_id
        data_dict["host_url"] = host_url
        data_dict["host_name"] = host_name
        data_dict["host_since"] = host_since
        data_dict["host_is_superhost"] = host_is_superhost
        data_dict["host_listings_count"] = host_listings_count
        data_dict["host_total_listings_count"] = host_total_listings_count
        data_dict["latitude"] = latitude
        data_dict["longitude"] = longitude
        data_dict["room_type"] = room_type
        data_dict["accommodates"] = accommodates
        data_dict["bedrooms"] = bedrooms
        data_dict["beds"] = beds
        data_dict["price"] = price
        data_dict["minimum_nights"] = minimum_nights
        data_dict["maximum_nights"] = maximum_nights
        data_dict["has_availability"] = has_availability
        data_dict["number_of_reviews"] = number_of_reviews
        data_dict["number_of_reviews_ltm"] = number_of_reviews_ltm
        data_dict["number_of_reviews_l30d"] = number_of_reviews_l30d
        data_dict["first_review"] = first_review
        data_dict["last_review"] = last_review
        data_dict["review_scores_rating"] = review_scores_rating
        data_dict["calculated_host_listings_count"] = calculated_host_listings_count
        data_dict["reviews_per_month"] = reviews_per_month
        data_dict["date"] = date
        data_dict["available"] = available
        data_dict["price"] = price
        data_dict["adjusted_price"] = adjusted_price
        listing_data.append(data_dict)

    return jsonify(listing_data)

@app.route("/api/BigDataBandits/Listings_unique")
def listings_unique():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a list of Listings data"""
    # Query all Listing data
    results = session.query(Listings.listing_id, Listings.listing_url, Listings.name, Listings.host_id, Listings.host_url, Listings.host_name, Listings.host_since,
                            Listings.host_is_superhost, Listings.host_listings_count, Listings.host_total_listings_count, Listings.latitude, Listings.longitude,
                            Listings.room_type, Listings.accommodates, Listings.bedrooms, Listings.beds, Listings.price,
                            Listings.minimum_nights, Listings.maximum_nights, Listings.has_availability, Listings.number_of_reviews, Listings.number_of_reviews_ltm,
                            Listings.number_of_reviews_l30d, Listings.first_review, Listings.last_review, Listings.review_scores_rating, Listings.calculated_host_listings_count,
                            Listings.reviews_per_month, Listings.date, Listings.available, Listings.price, Listings.adjusted_price
                            ).all()
    session.close()
    # Create a dictionary from the row data and append to a list of listing_data
    listing_data2 = []
    
    cols = ["adjusted_price", "accommodates", "number_of_reviews"]
    df = pd.DataFrame(results)
    # print(df[cols])
    df2 = df[cols].drop_duplicates(subset= cols)
    for ind in df2.index:
        data_dict = {}
        data_dict["adjusted_price"] = str(df['adjusted_price'][ind])
        data_dict["accommodates"] = str(df['accommodates'][ind])
        data_dict["number_of_reviews"] = str(df['number_of_reviews'][ind])
        data_dict["listing_url"] = str(df['listing_url'][ind])
        listing_data2.append(data_dict)
    return jsonify(listing_data2)


@app.route("/api/BigDataBandits/Reviews")
def reviews():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of review data"""
    # Query all Reviews data
    results = session.query(Reviews.listing_id, Reviews.id, Reviews.date, Reviews.reviewer_id, Reviews.reviewer_name).all()

    session.close()

    # Create a dictionary from the row data and append to a list of reviews_data
    reviews_data = []
    for listing_id, id, date, reviewer_id, reviewer_name in results:
        reviews_dict = {}
        reviews_dict["listing_id"] = listing_id
        reviews_dict["id"] = id
        reviews_dict["date"] = date
        reviews_dict["reviewer_id"] = reviewer_id
        reviews_dict["reviewer_name"] = reviewer_name
        reviews_data.append(reviews_dict)

    return jsonify(reviews_data)


@app.route("/api/BigDataBandits/amenities")
def amenities():
    # Converting DataFrame to JSON
    amenities_data = df_amenities.to_dict(orient='records')
    return jsonify(amenities_data)


if __name__ == '__main__':
    #app.run(host="0.0.0.0", port=8000)
    app.run(debug=True)

# -*- coding: utf-8 -*-
"""ny_airbnb_data_raw_colab_AN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QuB802MJeKN1LrYwFFqPW3RrSTZ8T7ut
"""

import os
# Find the latest version of spark 3.x  from http://www.apache.org/dist/spark/ and enter as the spark version
# For example:
# spark_version = 'spark-3.4.0'
spark_version = 'spark-3.4.0'
os.environ['SPARK_VERSION']=spark_version

# Install Spark and Java
!apt-get update
!apt-get install openjdk-11-jdk-headless -qq > /dev/null
!wget -q http://www.apache.org/dist/spark/$SPARK_VERSION/$SPARK_VERSION-bin-hadoop3.tgz
!tar xf $SPARK_VERSION-bin-hadoop3.tgz
!pip install -q findspark

# Set Environment Variables
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64"
os.environ["SPARK_HOME"] = f"/content/{spark_version}-bin-hadoop3"

# Start a SparkSession
import findspark
findspark.init()

# Import packages
from pyspark.sql import SparkSession
import time

# Create a SparkSession
spark = SparkSession.builder\
    .appName("SparkSQL")\
    .config("spark.sql.debug.maxToStringFields", 2000)\
    .config("spark.driver.memory", "2g")\
    .getOrCreate()

# Set the partitions to 4 or 8.
spark.conf.set("spark.sql.shuffle.partitions", 8)

# Read in data from S3 Bucket
from pyspark import SparkFiles
url_listings = "http://data.insideairbnb.com/united-states/ny/new-york-city/2023-09-05/data/listings.csv.gz"
spark.sparkContext.addFile(url_listings)
listings_df = spark.read.csv(SparkFiles.get("listings.csv.gz"), sep=",", header=True, quote ='"', multiLine=True, escape = '"')

# Create a lookup table for calendar.
url_calendar="http://data.insideairbnb.com/united-states/ny/new-york-city/2023-09-05/data/calendar.csv.gz"
spark.sparkContext.addFile(url_calendar)
calendar_df = spark.read.csv(SparkFiles.get("calendar.csv.gz"), sep=",", header=True, quote ='"', multiLine=True, escape = '"')

# Create a lookup table for the airport codes.
url_reviews ="http://data.insideairbnb.com/united-states/ny/new-york-city/2023-09-05/data/reviews.csv.gz"
spark.sparkContext.addFile(url_reviews)
reviews_df = spark.read.csv(SparkFiles.get("reviews.csv.gz"), sep=",", header=True, quote ='"', multiLine=True, escape = '"')

# Look over the listings data.
listings_df.show()

# Look over the data for calendar.
calendar_df.show()

# Look over the review data.
reviews_df.show()

import pandas as pd

listings_df.count()

calendar_df.count()

reviews_df.count()

unique_neighbourhoods = listings_df.select('neighbourhood_cleansed').distinct()
unique_neighbourhoods_count = unique_neighbourhoods.count()
print("Count of unique neighbourhoods:", unique_neighbourhoods_count)

accepted_neighborhoods = ["Manhattan", "Queens", "Brooklyn"]

filtered_listings_df = listings_df[listings_df['neighbourhood_group_cleansed'].isin(accepted_neighborhoods)]

filtered_listings_df.show()

filtered_listings_df.count()

listing_columns = ['id','listing_url','name','host_id','host_url','host_name','host_since','host_is_superhost','host_listings_count','host_total_listings_count','neighbourhood_cleansed','neighbourhood_group_cleansed','latitude','longitude','room_type','accommodates','bathrooms_text','bedrooms','beds','amenities','price','minimum_nights','maximum_nights','has_availability','number_of_reviews','number_of_reviews_ltm','number_of_reviews_l30d','first_review','last_review','review_scores_rating','review_scores_accuracy','review_scores_cleanliness','review_scores_checkin','review_scores_communication','review_scores_location','review_scores_value','calculated_host_listings_count','reviews_per_month']
calendars_columns = ['listing_id','date','available','price','adjusted_price']
reviews_columns = ['listing_id','id','date','reviewer_id','reviewer_name','comments']

column_listings_df = filtered_listings_df[listing_columns]
column_calendars_df = calendar_df[calendars_columns]
column_reviews_df = reviews_df[reviews_columns]

column_listings_df = column_listings_df.withColumnRenamed('id', 'listing_id')

column_listings_df.show()

from pyspark.sql import SparkSession

# Initialize Spark session
spark = SparkSession.builder.appName("example").getOrCreate()

# Assuming you have a PySpark DataFrame named 'column_listings_df'
# Drop rows with null values in the 'listing_id' column
column_listings_df = column_listings_df.dropna(subset=['first_review'])

# Show the DataFrame after dropping null values
column_listings_df.show()

column_listings_df.count()

column_reviews_df = column_reviews_df.dropna(subset=['comments'])
column_reviews_df.show()

column_reviews_df.count()

"""# Clean lists of amenities"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
import json

# Initialize a Spark session
spark = SparkSession.builder.appName("DataFrameCleanAmenities").getOrCreate()

# Assuming you have a PySpark DataFrame named 'cleaned_joined_df'
amenities_replaced_df = column_listings_df.select('*')

# List of amenity names to search for and replace
amenities_to_replace = ["Wifi", "TV", "Oven", "Stove", "Soap", "Shampoo", "Conditioner", "Sound system", "Refrigerator", "Backyard", "Patio", "BBQ grill",
                        "Free parking", "Paid parking", "Free street parking", "Paid street parking"]

# Define a UDF to perform the amenities replacement
def replace_amenities(amenities):
    amenities_list = json.loads(amenities)
    for i, amenity in enumerate(amenities_list):
        for amenity_to_replace in amenities_to_replace:
            if amenity_to_replace.lower() in amenity.lower():
                amenities_list[i] = amenity_to_replace
    return json.dumps(amenities_list)

# Register the UDF
replace_amenities_udf = udf(replace_amenities, StringType())

# Apply the UDF to replace amenities
amenities_replaced_df = amenities_replaced_df.withColumn('amenities', replace_amenities_udf('amenities'))

# Print or display the modified DataFrame
amenities_replaced_df.show()

# Define the string to find and the string to replace it with
string_to_find = "AC "
replacement_string = "Air conditioning"

# Define a UDF to perform the string replacement
def replace_string(amenities):
    amenities_list = json.loads(amenities)
    for i, amenity in enumerate(amenities_list):
        if string_to_find.lower() in amenity.lower():
            amenities_list[i] = replacement_string
    return json.dumps(amenities_list)

# Register the UDF
replace_string_udf = udf(replace_string, StringType())

# Apply the UDF to replace strings
amenities_replaced_df = amenities_replaced_df.withColumn('amenities', replace_string_udf('amenities'))

# Print or display the modified DataFrame
amenities_replaced_df.show()

# Create a copy of the DataFrame
amenities_cleaned_df = amenities_replaced_df.select('*')

# Define a UDF to perform the amenities cleaning
def clean_amenities(amenities):
    amenities_list = json.loads(amenities)
    for i, amenity in enumerate(amenities_list):
        # Split amenity at colon, if present
        amenity_parts = amenity.split(':')

        # Take the first part as the cleaned amenity (remove characters after colon)
        cleaned_amenity = amenity_parts[0].strip()

        # Update the amenities list
        amenities_list[i] = cleaned_amenity

    return json.dumps(amenities_list)

# Register the UDF
clean_amenities_udf = udf(clean_amenities, StringType())

# Apply the UDF to clean amenities
amenities_cleaned_df = amenities_cleaned_df.withColumn('amenities', clean_amenities_udf('amenities'))

# Print or display the modified DataFrame
amenities_cleaned_df.show()

column_listings_df = amenities_cleaned_df
column_listings_df.show()

column_calendars_df.show()

from pyspark.sql import functions as F

# Assuming column_calendars_df is your DataFrame
# Remove dollar signs and convert price and adjusted_price to float
clean_column_calendars_df = column_calendars_df.withColumn("price",
                                                     F.regexp_replace(F.col("price"), "[$,]", "").cast("float"))
clean_column_calendars_df = clean_column_calendars_df.withColumn("adjusted_price",
                                                     F.regexp_replace(F.col("adjusted_price"), "[$,]", "").cast("float"))

# Show the DataFrame to verify changes
clean_column_calendars_df.show()

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, month, dayofmonth, dayofweek
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import RegressionEvaluator

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("AirbnbPricePrediction") \
    .getOrCreate()

# Convert the price columns to float
clean_column_calendars_df = clean_column_calendars_df.withColumn("price", col("price").cast("float"))
clean_column_calendars_df = clean_column_calendars_df.withColumn("adjusted_price", col("adjusted_price").cast("float"))

# Drop rows where either 'price' or 'adjusted_price' is null
clean_column_calendars_df = clean_column_calendars_df.dropna(subset=['price', 'adjusted_price'])

# Convert 'available' to numerical (1 for 't', 0 for 'f')
clean_column_calendars_df = clean_column_calendars_df.withColumn("available", (col("available") == "t").cast("integer"))

# Convert 'date' from string to date type
clean_column_calendars_df = clean_column_calendars_df.withColumn("date", col("date").cast("date"))

# Add 'month' and 'day_of_week' features
clean_column_calendars_df = clean_column_calendars_df.withColumn("month", month("date")) \
                                         .withColumn("day_of_week", dayofweek("date"))

# Features and Assembler
feature_columns = ['month', 'day_of_week', 'available']
assembler = VectorAssembler(inputCols=feature_columns, outputCol="features")

# Model
rf = RandomForestRegressor(labelCol="price", featuresCol="features")

# Pipeline
pipeline = Pipeline(stages=[assembler, rf])

# Split data into training and test sets
train_data, test_data = clean_column_calendars_df.randomSplit([0.8, 0.2])

# Fit model to training data
model = pipeline.fit(train_data)

# Make predictions on test data
predictions = model.transform(test_data)

# Evaluate the model
evaluator = RegressionEvaluator(labelCol="price", predictionCol="prediction", metricName="rmse")
rmse = evaluator.evaluate(predictions)
print("Root Mean Squared Error (RMSE) on test data = %g" % rmse)

clean_column_calendars_df.show(400)

predictions.show(400)

!ls /content/

!zip -r /content/model.zip /content/model

from google.colab import files
files.download("/content/model.zip")

# End the Spark session
spark.stop()

# Don't forget to stop the Spark session when you're done
spark.stop()
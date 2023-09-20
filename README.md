# p4big_data_bandits
# Project 4 
# New York City AirBnB Analysis

## To use
Use link: https://bigdatabandits2.z5.web.core.windows.net/

## Deployment
Link to website: https://bigdatabandits2.z5.web.core.windows.net/

## Data and Delivery
We started with three CSV files from the source (http://insideairbnb.com/get-the-data/), specifically about New York City.

- Listings.csv.gz
- Reviews.csv.gz
- Calendars.csv.gz

Out of these three original files, calendars contained 15.9M rows of data, reviews contained 1.1M rows, and listings contained 44K rows.
We cleaned this data down by removing null values from all three files.
We used pyspark to read the data into Google Colab

The three dataframes we cleaned down to 

- Listings - 27,343 rows
- Reviews - 1,019,573 rows
- Calendar - 14,399,996 rows

We hosted the website using Microsoft Azure. We also deployed a flask app so that we can reference project 3 and json data for project 4.

## Back End
...

## Visualizations
...

# Analysis Ownership

## Elena Lucherini - Host Price Predictor:
Host Price Predictor
Using a simple machine learning model, I developed a calculator that will suggest a nightly rate to someone looking to host their New York City property on AirBnb. The price predictor takes in inputs such as the property's borough, the number of people accommodated, and relevant property features and amenities.

Please note that the Host Price Predictor is not hosted on the Azure site. To open it, within this GitHub repository, go to Folders/EL:
-	Open EL_price_predictor_app.py in an integrated terminal.
-	Then open EL_price_predictor_index.html in a Live Server. 

Machine Learning
I made four attempts to optimize my simple machine learning model, before selecting the best approach of the four so I could move on to build the price predictor. 
Linear Regression Model: Using the cleaned data from Google Colab, specifically with the top 25 amenities columns, I started with a linear regression, specifically because I wanted to train a model based on price against many other factors. We found the R-squared value (which ideally should be above 0.8) to be 0.45 - not great.
Neural Network Keras Model: Wanting and needing to try a different approach, I moved on to TensorFlow and a neural network deep learning model. I tried three approaches to get the R-squared value above 0.8, but ultimately I had to settle for the approach that brought me closest but was still below 0.8.
Attempt #1 - My first neural network approach was to use five Keras layers, all relu, and 100 epochs. The resulting R-squared value was 0.54, which was better than the linear regression's output of 0.45, but still not ideal. 
Attempt #2 - My second attempt included using eight layers, all still relu, and 150 epochs. Unfortunately, I think I overtrained the model, since the R-squared value declined back down to 0.47.
Attempt #3 - In my third attempt I went back to 5 layers and 100 epochs, but incorporated tanh into three of those layers. But unfortunately, I only got to a 0.50 R-squared value. 
Final choice - I chose to save the first neural network model as a .h5 file, as it had the highest R-squared value of the four models. In a real work scenario (and with more time), I would have utilized Andrea’s random forest regressor model, since it produced a much better R-squared value.

## Andrea Paredes - ML Model Implementation and Optimization:
Using clean merged data I selected 4 features that I believed would be the most relevant to train my model. After encoding and making sure all columns formats were correct, I started experimenting and got bad results from initial models, with 0.13 R-squared score.
Added Linear Regression and later Random Forest Regression. The Random Forest gave me a 0.81 R-squared score. Having this as my base, I moved to train a neural network model that initially improved very little with a 0.23 R-squared. After adding many new feature columns, layers and neurons the best score I was able to reach was 0.78 R-squared.
Unfortunately, since too much time was spent training a model with the goal to reach at least 0.80 R-squared, I was not able to work on deploying the model to our website.

## Rutva Korat - :
Tableau Dashboard:
    https://public.tableau.com/views/P4DashboardFinal/P4dashboard?:language=en-US&:display_count=n&:origin=viz_share_link


Natural Language Processing
	
Within our database we have data on over 1 million reviews that have been left by those who have stayed at Airbnb’s of New York City. With this data I wanted to see what the top 25 word-choices were used to describe in the reviews left and I did so by using Natural Language Processing to take apart each review and clean it up to determine what were the top words used. I took the column named comments, where the reviews were stored, and split the reviews down to each word and converted them down to lower case format. After that I took out the stop words as well as filtering out punctuations, tags, and spaces. Once that was completed, I was left with just a single file line of words. I then took only the first 200,000 words from the full data set for this project, in reality, you would want to run NLP on the full data set, I was having to deal with long run times which is why I decided to take the first 200,000 words only. After, all of this I was able to count the total for each word and then displayed the 25 most used words into a bar graph. Here we can see “great”, “place”, and “stay” were the top three most used words. Great being the most used tell us that the reviews over all are leaning toward being positive review set. As we go down the list of words, we can see that most of the words are used in a positive connotation which gives us an idea that the reviews left show a positive trend overall. 

Sentiment Analysis

With that we also wanted to see if pricing of the Airbnb’s reviewed held any influence on the reviews left itself, mainly trying to determine if there is a trend following the reviews being better as the Airbnb’s gets more expensive. We decided to do a sentiment analysis where we take each review left on the Airbnb’s and run it through the Vader sentiment intensity analyzer to see what the sentiment score of each review is. In this test, we produced four scores that are positive, neutral, negative, and a compound score. Here after running the test, I placed each compound score of the Airbnb’s into a scatter plot. I used the compound score to display here because this score provides the overall sentiment value of the text. As we can see here in this chart, that we have scores placed from negative one to one. The color change determines how heavy the score is, blue telling us it is a positive score, tan being neutral, and red being a negative score. As mentioned before, the scores are being compared to the pricing and we can see that over all there are more positive reviews as the price gets bigger for the Airbnb. 

This could be because the more expensive AirBnb’s get, they could have better amenities, better location of the property itself, such as better views, as well as using higher level vocabulary to describe their stay. We can see how dense the area is at the bottom portion of the chart is, this can tell us that regardless of price, there are positive scores being attained to those who have stayed at Airbnb’s that are less expensive. This can be determined by also be from the Airbnb’s being able to meet the demand of a quality stay. The reviews that have a negative to neutral score can see what their reviewers are rating the Airbnb’s at and can improve their stays for future guest based on the scores. 



## Adam Nguyen - :


...

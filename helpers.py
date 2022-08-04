import yaml
import psycopg2

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

def connect_to_db(config):
    try:
        connect = psycopg2.connect(
                user=config["user"], 
                password=config["password"], 
                host=config["hostname"], 
                database=config["database"])
        print("Successful connection!")

    except Exception as e:
        print("Connection could not be established")
        print(e)

    cursor = connect.cursor()
    return connect, cursor 

def setup_nltk():
    nltk.download([
        "names",
        "stopwords",
        "punkt",
        "averaged_perceptron_tagger",
        "vader_lexicon",])
    unwanted = nltk.corpus.stopwords.words("english")
    unwanted.extend([w.lower() for w in nltk.corpus.names.words()])
    return unwanted

def get_sentiment(text):
    sia = SentimentIntensityAnalyzer() 
    return sia.polarity_scores(text)


setup_nltk()

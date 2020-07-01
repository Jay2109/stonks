#importing all the libs
import nltk
#nltk.download('twitter_samples')
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier
import pandas as pd

from sentimentor.models import Sentimentor,Tickersentiment


import re, string, random
import joblib

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

#NLP PART cleaning the data 

def remove_noise(tweet_tokens, stop_words = ()):

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens



def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token


def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)

#This will get the sentiment from the text whether its positive or negative
def getting_sentiment(news_data):
    news = remove_noise(word_tokenize(news_data))
    model_file_name='sentimentor.sav'
    #The line below loads the classifier stored 
    loaded_model = joblib.load(model_file_name)

    sentiment=loaded_model.classify(dict([token, True] for token in news))
    return sentiment


#Loading Model 

#cron job 1 to get general sentiment score
def sentiment(): 
    sentiment_score=[]

    market_watch_data = market_watch()
    market_watch_str = string_convert_new(market_watch_data)

    sentiment_score.append(getting_sentiment(market_watch_str))


    daily_fx_data = daily_fx()
    daily_fx_str = string_convert_new(daily_fx_data)

    sentiment_score.append(getting_sentiment(daily_fx_str))


    yahoo_fin_data = yahoo_fin()
    yahoo_fin_str = string_convert_new(yahoo_fin_data)

    sentiment_score.append(getting_sentiment(yahoo_fin_str))

    investors_business_data = investors_business()
    investors_business_str = string_convert_new(investors_business_data)

    sentiment_score.append(getting_sentiment(investors_business_str))

    ect_times_data = ect_times()
    ect_times_str = string_convert_new(ect_times_data)

    sentiment_score.append(getting_sentiment(ect_times_str))

    score(sentiment_score)

    
    #all_news_data_combine=market_watch_str+daily_fx_str+yahoo_fin_str+investors_business_str+ect_times_str
    
    #print(sentiment)



#cron job 2 to get sentiment ticker wise



#This function is especially used to get the news specific to a ticker
def ticker_yahoo():

    symbol_details=pd.read_csv('company.csv')

    sym=symbol_details['symbol']

    for i in range(len(sym)):
        text_title=[]
        url="https://in.finance.yahoo.com/quote/"+sym[i]+"?p="+sym[i]+"&.tsrc=fin-srch"
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        #print(url)
        soup = BeautifulSoup(webpage)
        
        #title = soup.find_all('li',class_='js-stream-content')
        #text_title=[f.get_text() for f in title]

    
        title_head = soup.find_all('p')
        head=[g.get_text() for g in title_head]
    
    
        text_title.append(head)

        ticker_yahoo_data = string_convert_new(text_title)
               

        sentiment_ticker=getting_sentiment(ticker_yahoo_data)
        value=""
        if sentiment_ticker=="Positive":
            value="Bullish"
        elif sentiment_ticker=="Negative":
            value="Bearish"
        
        
        store_score_ticker(sym[i],value)

    





    
    
    

#conversion of the score generated

def score(sentiment_score):


    bear=sentiment_score.count("Negative")
    bull=sentiment_score.count("Positive")
    sentiment=""
    if bear>bull:
        sentiment="Bullish"
    elif bull>bear :
        sentiment="Bearish"
    elif bear==bull:
        sentiment="Neutral"
    else :
        sentiment="No effect"

    store_score_general(sentiment)

#store general sentiment score
def store_score_general(sentiment):

    score=Sentimentor(
      general_sentiment=sentiment
    )
    score.save(force_insert=True)

#store sentiment score of a specific ticker in to database
def store_score_ticker(ticker,value):
    score=Tickersentiment(
        sym_name=ticker,
        sentiment=value
    )

    score.save(force_insert=True)










#following functions load all data from different sources on internet 



def market_watch():
    req = Request("https://www.marketwatch.com/latest-news?mod=side_nav",
                  headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage)

    title = soup.find_all('h3', class_='article__headline')
    text_title = [f.get_text() for f in title]
    '''seperator=','
    seperator.join(text_title)'''
    return text_title

def daily_fx():
    req = Request("https://www.dailyfx.com/market-news",
                  headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage)

    title = soup.find_all('p', class_='dfx-articleHero__text')
    text_title = [f.get_text() for f in title]

    title_head = soup.find_all('span', class_='dfx-articleListItem__title')
    head = [g.get_text() for g in title_head]

    text_title.append(head)

    return text_title


def investors_business():
    req = Request("https://www.investors.com/news/",
                  headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage)

    title = soup.find_all('h4')
    text_title = [f.get_text() for f in title]

    title_head = soup.find_all('h6')
    head = [g.get_text() for g in title_head]

    text_title.append(head)

    return text_title


def ect_times():
    req = Request("https://economictimes.indiatimes.com/markets/stocks/news",
                  headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage)

    title = soup.find_all('h3')
    text_title = [f.get_text() for f in title]
    return text_title


def yahoo_fin():
    req = Request("https://finance.yahoo.com/quote/%5EGSPC/",
                  headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage)

    title = soup.find_all('li', class_='js-stream-content')
    text_title = [f.get_text() for f in title]
    return text_title



#functions to convert the the extracted from list to a string 

def string_convert(news_data):
    str_news = ''
    for content in news_data:
        str_news += content
    return str_news

def string_convert_new(news_data):
	str_news = ' '.join([str(item) for item in news_data ])
	return str_news



sentiment()






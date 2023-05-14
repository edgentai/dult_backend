import json
from constants import *
import pymysql


# Connecting to the database
db = pymysql.connect(
    host=aws_rds_host, user=aws_rds_username, password=aws_rds_password, db=aws_rds_db
)
cursor = db.cursor()


def lambda_handler(event, context):

    # Query for tweets count 
    count_card_query = """select count(*) from dult_grievance_classification"""
    cursor.execute(count_card_query)
    tweets_count = cursor.fetchall()[0][0]

    # Query for tweets count 
    today_count_card_query = """select count(*) from dult_grievance_classification where DATE(date) = curdate()"""
    cursor.execute(today_count_card_query)
    today_tweets_count = cursor.fetchall()[0][0]

    # Query for showing sentiment chart
    sentiment_graph_query = """select Sentiment, count(Sentiment) as cnt from dult_grievance_classification where DATE(date) = curdate() group by Sentiment"""
    cursor.execute(sentiment_graph_query)
    sentiment_count = cursor.fetchall()
    sentiment_data_dict = {}
    for sentiment_data in sentiment_count:
        sentiment_data_dict[sentiment_data[0]] = sentiment_data[1]

    # Query for showing intent chart
    intent_data_dict = {}
    intent_data_query = """select intent, count(intent) as cnt from dult_grievance_classification where DATE(date) = curdate() group by intent"""
    cursor.execute(intent_data_query)
    intent_count = cursor.fetchall()
    for intent_count_data in intent_count:
        intent_key = intent_count_data[0]
        if intent_key == 'Urget Actionable':
            intent_key = "Actionable"
        intent_data_dict[intent_key] = intent_count_data[1]
    # for intent_count_data in intent_count:
    #     date_value = str(intent_count_data[0])
    #     class_value = str(intent_count_data[1])
    #     frequency_value = str(intent_count_data[2])
    #     if date_value not in intent_data_dict:
    #         intent_data_dict[date_value] = [(class_value, frequency_value)]
    #     else:
    #         intent_data_dict[date_value].append((class_value, frequency_value))

    # Query for showing classification chart
    sub_super_count_dict = {}
    sub_super_query = """select Super_Class, Sub_Class, count(*) from dult_grievance_classification where
      DATE(date) = curdate() group by Super_Class, Sub_Class"""
    cursor.execute(sub_super_query)
    sub_super_count = cursor.fetchall()
    for sub_super_count_data in sub_super_count:
        super_value = str(sub_super_count_data[0])
        sub_value = str(sub_super_count_data[1])
        frequency_value = str(sub_super_count_data[2])
        if super_value not in sub_super_count_dict:
            sub_super_count_dict[super_value] = [(sub_value, frequency_value)]
        else:
            sub_super_count_dict[super_value].append((sub_value, frequency_value))

    tweet_data_query = """select * from dult_grievance_classification where DATE(date) = curdate()"""
    cursor.execute(tweet_data_query)
    cols_list = ["id","Date","Intent","Sentiment","Sub_Class","Super_Class","user_message"]
    tweet_data = cursor.fetchall()
    tweet_data_dict = {
        cols_list[0] : [],
        cols_list[1] : [],
        cols_list[2] : [],
        cols_list[3] : [],
        cols_list[4] : [],
        cols_list[5] : [],
        cols_list[6] : [],

    }
    for tweet_data_object in tweet_data:
        idx = 0
        for value in tweet_data_object:
            tweet_data_dict[cols_list[idx]].append(str(value))
            idx = idx + 1




    final_data = {
        "count_card": tweets_count,
        "today_count_card" : today_tweets_count,
        "sentiment": sentiment_data_dict,
        "intent": intent_data_dict,
        "sub_super": sub_super_count_dict,
        "tweet_data":tweet_data_dict
    }

    return {"statusCode": 200, "body": json.dumps({"message": final_data})}

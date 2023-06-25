from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from dashboard_data.constants import *
import pymysql
from datetime import datetime
from datetime import timezone, timedelta

# API for line chart
class LineChartDataQuery(APIView):
    
    db = pymysql.connect(
    host=aws_rds_host, user=aws_rds_username, password=aws_rds_password, db=aws_rds_db
    )
    cursor = db.cursor()

    def post(self, request):

        data = request.data
        start_date = data.get("start_date", "")
        end_date = data.get("end_date", "")
        group_range = data.get("group_range","")


        # convert date to utc datetime zone
        start_formatted_datetime = datetime.fromisoformat(start_date).astimezone(
            timezone.utc
        )
        start_formatted_datetime = start_formatted_datetime.strftime("%Y-%m-%d %H:%M:%S")
        start_formatted_datetime_obj = datetime.strptime(
            start_formatted_datetime, "%Y-%m-%d %H:%M:%S"
        )

        end_formatted_datetime = datetime.fromisoformat(end_date).astimezone(
            timezone.utc
        )
        end_formatted_datetime = end_formatted_datetime.strftime("%Y-%m-%d %H:%M:%S")
        end_formatted_datetime_obj = datetime.strptime(
            end_formatted_datetime, "%Y-%m-%d %H:%M:%S"
        )

        if group_range == "daily":
            query = '''SELECT DATE(date),intent,  COUNT(intent) AS cnt
                    FROM dult_grievance_classification
                    WHERE date BETWEEN '%s' AND '%s'
                    GROUP BY  DATE(date), intent'''%(start_formatted_datetime_obj, end_formatted_datetime_obj)
        
        if group_range == "week":
            query = '''SELECT WEEK(date),intent,  COUNT(intent) AS cnt
                    FROM dult_grievance_classification
                    WHERE date BETWEEN '%s' AND '%s'
                    GROUP BY  WEEK(date), intent'''%(start_formatted_datetime_obj, end_formatted_datetime_obj)
        
        if group_range == 'month':
            query = '''SELECT MONTH(date),intent,  COUNT(intent) AS cnt
                    FROM dult_grievance_classification
                    WHERE date BETWEEN '%s' AND '%s'
                    GROUP BY  MONTH(date), intent'''%(start_formatted_datetime_obj, end_formatted_datetime_obj)
        
        self.cursor.execute(query)
        intent_count = self.cursor.fetchall()
        intent_data_dict = {}

        for intent_count_data in intent_count:
            intent_key = str(intent_count_data[0])
            if intent_key in intent_data_dict.keys():
                intent_data_dict[intent_key].append((intent_count_data[1], intent_count_data[2]))
            else:
                intent_data_dict[intent_key] = [(intent_count_data[1], intent_count_data[2])]
        
        current_date = start_formatted_datetime_obj
        delta = timedelta(days=1)
        date_list = []
        while current_date <= end_formatted_datetime_obj:
            date_list.append(current_date.date())
            current_date += delta
        
        for date_range in date_list:
            if str(date_range) not in intent_data_dict:
                intent_data_dict[str(date_range)] = []

        return Response(data=intent_data_dict, status=status.HTTP_200_OK)



# API for bargraph
class BarGraphDataQuery(APIView):
    
    db = pymysql.connect(
    host=aws_rds_host, user=aws_rds_username, password=aws_rds_password, db=aws_rds_db
    )
    cursor = db.cursor()

    def post(self, request):

        data = request.data
        start_date = data.get("start_date", "")
        end_date = data.get("end_date", "")

        # convert date to utc datetime zone
        start_formatted_datetime = datetime.fromisoformat(start_date).astimezone(
            timezone.utc
        )
        start_formatted_datetime = start_formatted_datetime.strftime("%Y-%m-%d %H:%M:%S")
        start_formatted_datetime_obj = datetime.strptime(
            start_formatted_datetime, "%Y-%m-%d %H:%M:%S"
        )

        end_formatted_datetime = datetime.fromisoformat(end_date).astimezone(
            timezone.utc
        )
        end_formatted_datetime = end_formatted_datetime.strftime("%Y-%m-%d %H:%M:%S")
        end_formatted_datetime_obj = datetime.strptime(
            end_formatted_datetime, "%Y-%m-%d %H:%M:%S"
        )

        query = '''SELECT Super_Class, Sub_Class, COUNT(*) FROM dult_grievance_classification
                WHERE date BETWEEN '%s' AND '%s'
                GROUP BY Super_Class, Sub_Class'''%(start_formatted_datetime_obj, end_formatted_datetime_obj)
        
        self.cursor.execute(query)
        sub_super_count = self.cursor.fetchall()
        sub_super_count_dict = {}

        for sub_super_count_data in sub_super_count:
            super_value = str(sub_super_count_data[0])
            sub_value = str(sub_super_count_data[1])
            frequency_value = str(sub_super_count_data[2])
            if super_value not in sub_super_count_dict:
                sub_super_count_dict[super_value] = [(sub_value, frequency_value)]
            else:
                sub_super_count_dict[super_value].append((sub_value, frequency_value))

        return Response(data=sub_super_count_dict, status=status.HTTP_200_OK)

class CardDataAPI(APIView):

    db = pymysql.connect(
    host=aws_rds_host, user=aws_rds_username, password=aws_rds_password, db=aws_rds_db
    )
    cursor = db.cursor()

    def get(self):

        # Query for tweets count 
        today_count_card_query = """select count(*) from dult_grievance_classification where DATE(date) >= curdate() - 7"""
        self.cursor.execute(today_count_card_query)
        today_tweets_count = self.cursor.fetchall()[0][0]

        # Query for showing sentiment chart
        sentiment_graph_query = """select Sentiment, count(Sentiment) as cnt from dult_grievance_classification where DATE(date) >= curdate() - 7 group by Sentiment"""
        self.cursor.execute(sentiment_graph_query)
        sentiment_count = self.cursor.fetchall()
        sentiment_data_dict = {}
        for sentiment_data in sentiment_count:
            sentiment_data_dict[sentiment_data[0]] = sentiment_data[1]
        
        intent_data_dict = {}
        intent_data_query = """select intent, count(intent) as cnt from dult_grievance_classification where DATE(date)  >= curdate() - 7 group by intent"""
        self.cursor.execute(intent_data_query)
        intent_count = self.cursor.fetchall()
        for intent_count_data in intent_count:

            intent_key = intent_count_data[0]
            if intent_key == 'Others':
                continue
            intent_data_dict[intent_key] = intent_count_data[1]
        
        final_data = {
            "today_count_card" : today_tweets_count,
            "sentiment": sentiment_data_dict,
            "intent": intent_data_dict,
        }
        

        return Response(data=final_data, status=status.HTTP_200_OK)


class TweetDataAPI(APIView):

    db = pymysql.connect(
    host=aws_rds_host, user=aws_rds_username, password=aws_rds_password, db=aws_rds_db
    )
    cursor = db.cursor()

    def get(self):

        tweet_data_query = """select * from dult_grievance_classification where DATE(date)  >= curdate() - 7"""
        self.cursor.execute(tweet_data_query)
        cols_list = ["id","Date","Intent","Sentiment","Sub_Class","Super_Class","user_message"]
        tweet_data = self.cursor.fetchall()
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
        

        return Response(data=tweet_data_dict, status=status.HTTP_200_OK)

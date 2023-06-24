from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from dashboard_data.constants import *
import pymysql
from datetime import datetime
from datetime import timezone

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

        return Response(data=intent_data_dict, status=status.HTTP_200_OK)






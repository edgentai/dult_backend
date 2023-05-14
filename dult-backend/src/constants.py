aws_rds_host = "dult-database.cndfa7fhtn3n.us-east-1.rds.amazonaws.com"
aws_rds_username = "admin"
aws_rds_password = "dult__2023"
aws_rds_db = "kTestDb"


'''from datetime import datetime
from datetime import timezone
formatted_datetime = datetime.fromisoformat("2023-05-04T15:44:12.000Z"[:-1]).astimezone(
    timezone.utc
)
formatted_datetime = formatted_datetime.strftime("%Y-%m-%d %H:%M:%S")
formatted_datetime_obj = datetime.strptime(
    formatted_datetime, "%Y-%m-%d %H:%M:%S"
)
sql = (
    """ insert into dult_grievance_classification(id,Date,Intent,Sentiment,Sub_Class,Super_Class,user_message) values('%s','%s', '%s', '%s','%s','%s','%s')"""
    % (
        "2023-05-05T07:01:21.000Z_Rajat ಕುಮಾರ್@SunilKumar_J14_twitter",
        formatted_datetime_obj,
        "Urget Actionable",
        "Negative",
        "Recharge",
        "PASS/Reserved Seat Issue",
        "user_message",
    )
)
cursor.execute(sql)
db.commit()

In [17]: from datetime import datetime                                                                                              

In [18]: from datetime import timezone                                                                                              

In [19]: datetime.fromisoformat('2020-01-06T00:00:00.000Z'[:-1]).astimezone(timezone.utc) 

In [22]: a = _                                                                                                                      

In [23]: a.strftime('%Y-%m-%d %H:%M:%S')  
b = _
date_time_obj = datetime.strptime(b, '%Y-%m-%d %H:%M:%S')  
Out[34]: datetime.datetime(2023, 5, 4, 22, 0, 32)

SELECT * FROM dult_grievance_classification
WHERE Date >= curdate() - INTERVAL DAYOFWEEK(curdate())+6 DAY
AND Date < curdate() - INTERVAL DAYOFWEEK(curdate()) DAY

select * from dult_grievance_classification
where date between date_sub(now(),INTERVAL 1 WEEK) and now();
'''

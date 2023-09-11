import pandas as pd
import boto3
from datetime import datetime
import mysql.connector
from io import StringIO
from airflow.contrib.hooks.aws_hook import AwsHook

current_date = datetime.now().strftime("%Y-%m-%d")
month = datetime.now().strftime("%b")
bucket_name = "openweather-project"
file_key = f"trusted/{month}/{current_date}.csv"
rds_endpoint = 'INSERT RDS ENDPOINT'
rds_dbname = 'INSERT DB NAME'
rds_username = 'INSERT DB USERNAME'
rds_password = 'INSERT DB PASSWORD'

def load_rds():
    aws_hook = AwsHook("aws_credentials_id")
    credentials = aws_hook.get_credentials()

    client = boto3.client("s3", aws_access_key_id= credentials.access_key, aws_secret_access_key= credentials.secret_key)

    s3_object = client.get_object(Bucket = bucket_name, Key = file_key)

    csv_data = s3_object["Body"].read().decode("utf-8")

    df = pd.read_csv(StringIO(csv_data))

    conn = mysql.connector.connect(
        host = rds_endpoint,
        user = rds_username,
        password = rds_password,
        database = rds_dbname
        )

    cursor = conn.cursor()

    for index, row in df.iterrows():
        
        insert_query = "INSERT INTO brazil_weather (id, nome, temp, feels_like, temp_min, temp_max, sun_rise, sunset, weather_condition, date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        
        data = (
        row["id"],
        row["nome"],
        row["temp"],
        row["feels_like"],
        row["temp_min"],
        row["temp_max"],
        row["sun_rise"],
        row["sunset"],
        row["weather_condition"],
        row["date"]
        )
        
        cursor.execute(insert_query, data)

    conn.commit()

    cursor.close()
    conn.close()
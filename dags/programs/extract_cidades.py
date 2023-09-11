import requests
import pandas as pd
from datetime import datetime
from io import StringIO
import boto3
from airflow.contrib.hooks.aws_hook import AwsHook

API_KEY = "INSERT YOUR API KEY HERE"
cidades = ["sao paulo","rio de janeiro", "brasilia", "fortaleza", "salvador", "manaus", "curitiba", "recife", "goiania", "porto alegre"]
bucket_name = "openweather-project"
current_date = datetime.now().strftime("%Y-%m-%d")

def extract_api():
    for cidade in cidades:
        
        link = f"https://api.openweathermap.org/data/2.5/weather?q={cidade},br&appid={API_KEY}"
        file_name = f"{cidade}-{current_date}"
        
        resp = requests.get(link)

        raw_data = resp.json()
        
        selected_data = {
            "id": raw_data["id"],
            "nome": raw_data["name"],
            "temp": raw_data["main"]["temp"],
            "feels_like": raw_data["main"]["feels_like"],
            "temp_min": raw_data["main"]["temp_min"],
            "temp_max": raw_data["main"]["temp_max"],
            "sun_rise": raw_data["sys"]["sunrise"],
            "sunset": raw_data["sys"]["sunset"],
            "weather_condition": raw_data["weather"][0]["description"],
            "date": raw_data["dt"]
            }
        
        df = pd.DataFrame([selected_data])

        csv_buffer = StringIO()

        df.to_csv(csv_buffer, index=False)

        aws_hook = AwsHook("aws_credentials_id")
        credentials = aws_hook.get_credentials()

        client = boto3.client("s3", aws_access_key_id= credentials.access_key, aws_secret_access_key= credentials.secret_key)

        client.put_object(
            Body= csv_buffer.getvalue(),
            Bucket=bucket_name,
            Key= f"raw/{current_date}/{file_name}.csv"
            )
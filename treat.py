import pandas as pd
import pytz
import boto3
from datetime import datetime
from io import StringIO
from airflow.contrib.hooks.aws_hook import AwsHook

current_date = datetime.now().strftime("%Y-%m-%d")
month = datetime.now().strftime("%b")
bucket_name = "openweather-project"
file_key = f"staging/{month}/{current_date}.csv"
def data_cleaning():
    aws_hook = AwsHook("aws_credentials_id")
    credentials = aws_hook.get_credentials()

    client = boto3.client("s3", aws_access_key_id= credentials.access_key, aws_secret_access_key= credentials.secret_key)

    s3_object = client.get_object(Bucket=bucket_name, Key=file_key)

    df = pd.read_csv(s3_object["Body"])

    df['date'] = pd.to_datetime(df['date'], unit='s', utc=True)
    df['date'] = df['date'].dt.tz_convert(pytz.timezone('America/Sao_Paulo'))
    df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M')

    df['sun_rise'] = pd.to_datetime(df['sun_rise'], unit='s', utc=True)
    df['sun_rise'] = df['sun_rise'].dt.tz_convert(pytz.timezone('America/Sao_Paulo'))
    df['sun_rise'] = df['sun_rise'].dt.strftime('%H:%M')

    df['sunset'] = pd.to_datetime(df['sunset'], unit='s', utc=True)
    df['sunset'] = df['sunset'].dt.tz_convert(pytz.timezone('America/Sao_Paulo'))
    df['sunset'] = df['sunset'].dt.strftime('%H:%M')

    def kelvin_to_celsius(kelvin):
        celsius = kelvin - 273.15
        return round(celsius, 2)

    df['temp'] = df['temp'].apply(kelvin_to_celsius)
    df['feels_like'] = df['feels_like'].apply(kelvin_to_celsius)
    df['temp_min'] = df['temp_min'].apply(kelvin_to_celsius)
    df['temp_max'] = df['temp_max'].apply(kelvin_to_celsius)

    csv_buffer = StringIO()

    df.to_csv(csv_buffer, index=False)

    client.put_object(
        Body= csv_buffer.getvalue(),
        Bucket=bucket_name,
        Key= f"trusted/{month}/{current_date}.csv"
        )
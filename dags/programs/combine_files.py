import pandas as pd
from datetime import datetime
from io import StringIO
import boto3
from airflow.contrib.hooks.aws_hook import AwsHook

bucket_name = "openweather-project"
current_date = datetime.now().strftime("%Y-%m-%d")
month = datetime.now().strftime("%b")

def combine_separate():
    aws_hook = AwsHook("aws_credentials_id")
    credentials = aws_hook.get_credentials()

    client = boto3.client("s3", aws_access_key_id= credentials.access_key, aws_secret_access_key= credentials.secret_key)

    s3_files = client.list_objects_v2(Bucket=bucket_name, Prefix=f"raw/{current_date}/")

    combined_data = pd.DataFrame()

    for file in s3_files.get("Contents"):
        file_name = file.get("Key")
        
        obj = client.get_object(Bucket=bucket_name, Key=file_name)
        csv_data = obj["Body"].read().decode("utf-8")
        
        df = pd.read_csv(StringIO(csv_data))
        
        combined_data = pd.concat([combined_data, df], ignore_index=True)

    csv_buffer = StringIO()

    combined_data.to_csv(csv_buffer, index=False)

    client.put_object(
        Body= csv_buffer.getvalue(),
        Bucket=bucket_name,
        Key= f"staging/{month}/{current_date}.csv"
        )
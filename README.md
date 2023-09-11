# Extract Weather Data with Apache Airflow 

In this project, we will construct an ETL batch pipeline to extract weather data for the top 10 biggest cities in Brazil using [Openweather API](https://openweathermap.org/api) and automate it with Apache Airflow.

foto

We selected AWS as our cloud provider for this project to establish the necessary infrastructure for data storage. The following tools were used to build this project:

- **S3**: Used to store weather data csv files at different stages (Raw, Staging, Trusted).
- **RDS**: MySQL 8.0.33, db.t3.micro, 20GB General Purpose SSD (AWS Free Tier) as our Database for cleaned data.
- **Docker**: Used to containerize our application.
- **Pandas**: Used for data wrangling of the csv files.
- **Boto3**: Python SDK to interact with AWS services.
- **Apache Airflow**: Used to automate, schedule, monitor data workflows.
- **Openweather API**: Our data source for this project

The pipeline consists of 5 steps:

1. Make API call to return weather data in JSON format and transform and upload it to S3 Bucket in `raw/year-month-day/` folder. (extract_cidades.py)

Example of collected data for Brasília:

```
id: 3469058
nome: Brasília
temp: 300.66 (Temperature in Kelvin)
feels_like: 300.35
temp_min: 300.16
temp_max: 300.66
sun_set: 1693991658 (Time in Unix Timestamp)
sunset: 1694034389 (Time in Unix Timestamp)
weather_condition: scattered clouds
date: 1694028619 (Time in Unix Timestamp)
```

2. Combine each CSV file `created in step 1` into one CSV file and upload it to S3 Bucket in `staging/month/` folder. (combine_files.py)

Example of combined CSV file:

foto

3. Convert temperature values from Kelvin to Celsius and time from Unix timestamp to UTC-3 datetime then upload it to S3 Bucket in `trusted/month/`. (treat.py)

Example of data transformation:

```
temp: 300.66 -> 27.51
feels_like: 300.35 -> 27.20
temp_min: 300.16 -> 27.01
temp_max: 300.66 -> 27.51
sun_set: 1693991658 -> 06:14 (Only hour and minutes)
sunset:  1694034389 -> 18:06 (Only hour and minutes)
date: 1694028619 -> 2023-09-06 16:30
```

4. Load transformed data `create in step 3` to RDS MySQL Database. (load_to_rds.py)

Printscreen of database
# Extract Weather Data with Apache Airflow 

In this project, we will construct an ETL batch pipeline to extract weather data for the top 10 biggest cities in Brazil using [Openweather API](https://openweathermap.org/api) and automate it with Apache Airflow.

![DIAGRAM_OPENWEATHER](https://github.com/RodrigoEiki/CityWeatherAirflowETL/assets/125326098/f0c47a1a-155a-4a73-92d2-27f228cbbfe9)

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

```
id,nome,temp,feels_like,temp_min,temp_max,sun_rise,sunset,weather_condition,date
3469058,Brasília,300.66,300.35,300.16,300.66,1693991658,1694034389,scattered clouds,1694028619
6322752,Curitiba,287.22,286.38,286.85,287.64,1693992276,1694034424,light intensity drizzle,1694028382
6320062,Fortaleza,302.22,304.46,301.05,302.22,1693989068,1694032466,clear sky,1694028350
3462377,Goiânia,301.98,302.71,301.98,301.98,1693992002,1694034681,scattered clouds,1694028566
3663517,Manaus,307.42,309.89,307.42,309.43,1693994210,1694037642,scattered clouds,1694028346
3452925,Porto Alegre,292.81,292.55,292.58,294.41,1693992890,1694034740,clear sky,1694028343
3390760,Recife,301.17,303.22,301.17,301.17,1693988312,1694031473,broken clouds,1694028279
3451190,Rio de Janeiro,294.37,294.71,294.13,297.12,1693990736,1694033045,broken clouds,1694028566
3450554,Salvador,298.13,298.62,298.13,298.13,1693989320,1694032207,clear sky,1694028415
3448439,São Paulo,290.9,290.95,290.07,292.29,1693991578,1694033848,broken clouds,1694028329
```

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

![RDS_Data](https://github.com/RodrigoEiki/CityWeatherAirflowETL/assets/125326098/ed99a254-a608-427f-9601-2af75ac40b54)

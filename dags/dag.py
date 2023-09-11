from airflow.decorators import dag
from datetime import timedelta
from airflow.operators.python_operator import PythonOperator
import sys
sys.path.append('/opt/airflow/dags/programs/')
import combine_files
import pendulum
import extract_cidades
import load_to_rds
import treat

default_args = {
    'owner': 'rodrigo',
    'start_date': pendulum.now(),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_retry': False,
    "catchup": False
    }

@dag(
     default_args = default_args,
     description= 'Extract Data from Openweather API, transform and load it to RDS MySQL DB',
     schedule_interval = '0 4 * * *'
     )

def openweather_project_v2():
    
    extract_data = PythonOperator(
            task_id = 'extract_data_from_api',
            python_callable = extract_cidades.extract_api,
        )
    
    combine_csv = PythonOperator(
            task_id = 'combine_separate_files_from_api',
            python_callable = combine_files.combine_separate,
        )
    
    data_cleaning = PythonOperator(
            task_id = 'modify_data',
            python_callable = treat.data_cleaning,
        )
    
    load_data = PythonOperator(
            task_id = 'load_data_to_rds_mysql_db',
            python_callable = load_to_rds.load_rds,
        )
    
    extract_data >> combine_csv >> data_cleaning >> load_data
    
openweather_project_v2 = openweather_project_v2()
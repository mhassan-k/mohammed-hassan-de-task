from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime
from de_utils.operators.nyt_books_api_client_operator import NYTBooksAPIClientOperator

# Variables
api_key = 'fA9Y74l4GCgpj6sZpiXlLPf8IDUT6jRy'

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 7),
    'retries': 1,
}

# Define the DAG
dag = DAG(
    'nyt_books_api_pipeline',
    default_args=default_args,
    description='DAG to fetch NYT books data and save to PostgreSQL',
    schedule_interval='@daily',
)

start = DummyOperator(task_id='start', dag=dag)
end = DummyOperator(task_id='end', dag=dag)

fetch_and_save_data_task = NYTBooksAPIClientOperator(
    task_id='fetch_nyt_books',
    api_key=api_key,
    db_params={
        'dbname': 'postgres',
        'user': 'airflow',
        'password': 'airflow',
        'host': 'host.docker.internal',
        'port': '8585',
        'options': '-c search_path=public'
    },
    url='https://api.nytimes.com/svc/books/v3/lists/full-overview.json',
    start_date_dt='2021-01-01',
    end_date_dt='2021-03-31',
    dag=dag,
)
start >> fetch_and_save_data_task >> end
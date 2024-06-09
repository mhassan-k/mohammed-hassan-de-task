from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

# Define the default_args dictionary
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 1),
    'retries': 1,
}

# Define the DAG
dag = DAG(
    'hello_world_dag',
    default_args=default_args,
    description='A simple Hello World DAG',
    schedule_interval='@daily',
)

# Define the Python function
def print_hello():
    print("Hello, World!")

# Define the tasks
start = DummyOperator(
    task_id='start',
    dag=dag,
)

hello_task = PythonOperator(
    task_id='hello_task',
    python_callable=print_hello,
    dag=dag,
)

end = DummyOperator(
    task_id='end',
    dag=dag,
)
# Set up the task dependencies
start >> hello_task >> end


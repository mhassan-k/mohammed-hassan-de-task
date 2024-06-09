from datetime import datetime
from cosmos import DbtDag, ExecutionConfig, ProfileConfig, ProjectConfig
from cosmos import ProfileConfig
from cosmos.profiles import PostgresUserPasswordProfileMapping

airflow_db = ProfileConfig(
    profile_name="airflow_db",
    target_name="dev",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id="airflow_metadata_db",
        profile_args={"schema": "public"},
    ),
)

my_cosmos_dag = DbtDag(
    project_config=ProjectConfig(
        "/opt/airflow/dbt/nyt_books",
    ),
    profile_config=airflow_db,
    execution_config=ExecutionConfig(
        dbt_executable_path="/opt/airflow/dbt/dbt_venv/bin/dbt",
    ),
    schedule_interval=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
    dag_id="nyt_books_dbt_run",
)
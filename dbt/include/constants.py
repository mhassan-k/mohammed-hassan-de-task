"Contains constants used in the DAGs"
from pathlib import Path
from cosmos import ExecutionConfig

nyt_books_path = Path("/opt/airflow/dbt/nyt_books")
dbt_executable = Path("/opt/airflow/dbt_venv/bin/dbt")

venv_execution_config = ExecutionConfig(
    dbt_executable_path=str(dbt_executable),
)
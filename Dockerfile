# Use the official Apache Airflow image
FROM apache/airflow:2.7.0

# Copy the requirements file to the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install -r requirements.txt
USER root

# Install required packages and dbt
RUN apt-get update && \
    apt-get install -y python3-pip && \
    python -m venv /opt/airflow/dbt/dbt_venv && source /opt/airflow/dbt/dbt_venv/bin/activate && \
    #pip3 install --no-cache-dir dbt-postgres==1.5.4 && \
    deactivate


ENV PATH="/opt/airflow/dbt/dbt_venv/bin:$PATH"

# Switch back to airflow user
USER airflow

# Copy the rest of your Airflow setup if necessary
 COPY ./dags /opt/airflow/dags
 COPY ./dbt /opt/airflow/dbt

# Set the Airflow home directory and other environment variables if needed
ENV AIRFLOW_HOME=/opt/airflow

# Set environment variable for Airflow metadata database connection
ENV AIRFLOW_CONN_AIRFLOW_METADATA_DB=postgresql+psycopg2://postgres:airflow@airflow:8585/postgres

# Use the official Apache Airflow image
FROM apache/airflow:2.7.0

# Set environment variables
ENV AIRFLOW_CONN_AIRFLOW_METADATA_DB=postgresql+psycopg2://airflow:airflow@host.docker.internal:8585/postgres

# Install dbt-core and dbt-postgres globally
RUN pip install --no-cache-dir dbt-core dbt-postgres==1.5.4

# Copy the requirements file to the container (if needed)
COPY requirements.txt /requirements.txt

# Install other dependencies from requirements.txt (if any)
RUN pip install --no-cache-dir -r /requirements.txt

# Ensure dbt is in the PATH
ENV PATH="/root/.local/bin:${PATH}"
# New York Times Books API

## Description
A data pipeline with Python, dbt, Docker, Airflow, and Postgres

### Objective

### Dataset

[NY books API](https://developer.nytimes.com/docs/books-product/1/routes/lists/overview.json/get) is an API that fetches data about to books

## Architecture
![image](https://github.com/mhassan-k/mohammed-hassan-de-task/assets/12893951/0a1bc487-c170-43e6-95fc-fc08b9f240a7)


## Data Modeling
Here are the dimensional models created from the provided data:

  - fct_bookRankings: This table contains the fact data about the book rankings.
  - dim_Books: This table contains detailed information about each book.
  - dim_lists: This table contains information about the lists.
  - dim_publishers: This table contains information about the publishers.

### Tools 
- Containerization - [**Docker**](https://www.docker.com), [**Docker Compose**](https://docs.docker.com/compose/)
- Orchestration - [**Airflow**](https://airflow.apache.org)
- Transformation - [**dbt**](https://www.getdbt.com)
- Data Warehouse - [**Postgres**](https://www.postgresql.org/)
- Language - [**Python**](https://www.python.org)

## Setup
### Pre-requisites
  - [docker](https://www.docker.com/products/docker-desktop/)
  - [docker-compose](https://docs.docker.com/compose/install/)
### Files Usage

- `requirements.txt`: a text file lsiting the projet's dependancies.
- `README.md`: Markdown text with a brief explanation of the project and the repository structure.
- `Dockerfile`: build users can create an automated build that executes several command-line instructions in a container.
- `docker-compose.yaml`: Integrates the various docker containers and run them in a single environment.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/mhassan-k/mohammed-hassan-de-tas
   ```

2. Run
   ```sh
    docker-compose build
    docker-compose up
   ```
3. Open Airflow web browser
   ```JS
   Navigate to `http://localhost:8000/` on the browser
   login --> username : airflow password : airflow
   trigger airflow pipeline  `x`
    ```
## How can I make this better?!
- 
- 

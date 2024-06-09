import requests
import pandas as pd
import logging
from sqlalchemy import create_engine, text
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from datetime import datetime, timedelta
import time


class NYTBooksAPIClientOperator(BaseOperator):
    @apply_defaults
    def __init__(
        self, api_key, db_params, url, start_date_dt, end_date_dt, *args, **kwargs
    ):
        super(NYTBooksAPIClientOperator, self).__init__(*args, **kwargs)
        self.api_key = api_key
        self.db_params = db_params
        self.url = url
        self.start_date_dt = datetime.strptime(start_date_dt, "%Y-%m-%d")
        self.end_date_dt = datetime.strptime(end_date_dt, "%Y-%m-%d")
        self.logger = logging.getLogger("NYTBooksAPIClient")
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        self.engine = create_engine(
            f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['dbname']}"
        )

    def fetch_and_transform_data(self, date):
        request_url = f"{self.url}?api-key={self.api_key}&published_date={date}"
        request_headers = {"Accept": "application/json"}
        response = requests.get(request_url, headers=request_headers)
        response.raise_for_status()
        self.logger.info(f"Data fetched successfully from the API for date {date}.")
        data = response.json()
        lists = data["results"]["lists"]

        # Flatten the nested JSON
        records = []
        for item in lists:
            for book in item["books"]:
                record = {
                    "bestsellers_date": data["results"]["bestsellers_date"],
                    "published_date": data["results"]["published_date"],
                    "published_date_description": data["results"][
                        "published_date_description"
                    ],
                    "previous_published_date": data["results"][
                        "previous_published_date"
                    ],
                    "next_published_date": data["results"]["next_published_date"],
                    "list_id": item["list_id"],
                    "list_name": item["list_name"],
                    "display_name": item["display_name"],
                    "updated": item["updated"],
                    "list_image": item["list_image"],
                    "list_image_width": item["list_image_width"],
                    "list_image_height": item["list_image_height"],
                    "book_rank": book["rank"],
                    "book_title": book["title"],
                    "book_author": book["author"],
                    "book_description": book["description"],
                    "book_isbn": book["primary_isbn13"],
                    "book_publisher": book["publisher"],
                    "book_image": book["book_image"],
                }
                records.append(record)

        df = pd.DataFrame(records)
        self.logger.info(
            f"Data transformed into DataFrame with {len(df)} records for date {date}."
        )
        return df

    def create_table_if_not_exists(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS public.best_seller_book_lists (
            bestsellers_date DATE,
            published_date DATE,
            published_date_description TEXT,
            previous_published_date DATE,
            next_published_date DATE,
            list_id INTEGER,
            list_name TEXT,
            display_name TEXT,
            updated TEXT,
            list_image TEXT,
            list_image_width INTEGER,
            list_image_height INTEGER,
            book_rank INTEGER,
            book_title TEXT,
            book_author TEXT,
            book_description TEXT,
            book_isbn VARCHAR(13),
            book_publisher TEXT,
            book_image TEXT
        );
        """
        with self.engine.connect() as connection:
            connection.execute(text(create_table_query))
            self.logger.info("Table 'best_seller_book_lists' ensured to exist.")

    def truncate_table(self):
        truncate_table_query = "TRUNCATE TABLE best_seller_book_lists;"
        with self.engine.connect() as connection:
            connection.execute(text(truncate_table_query))
            self.logger.info("Table 'best_seller_book_lists' truncated.")

    def save_data_to_postgres(self, df):
        try:
            df.to_sql(
                "best_seller_book_lists",
                self.engine,
                if_exists="append",
                index=False,
                method="multi",
            )
            self.logger.info("DataFrame uploaded to PostgreSQL successfully.")
        except Exception as e:
            self.logger.error(f"Error uploading DataFrame to PostgreSQL: {e}")

    def execute(self, context):
        self.create_table_if_not_exists()
        self.truncate_table()

        current_date = self.start_date_dt
        while current_date <= self.end_date_dt:
            retries = 5
            delay = 15
            for attempt in range(retries):
                try:
                    df = self.fetch_and_transform_data(
                        current_date.strftime("%Y-%m-%d")
                    )
                    self.save_data_to_postgres(df)
                    time.sleep(5)  # Sleep for 5 seconds after saving the data
                    break
                except requests.exceptions.RequestException as e:
                    self.logger.error(
                        f"Error fetching data for date {current_date.strftime('%Y-%m-%d')}: {e}"
                    )
                    if attempt < retries - 1:
                        time.sleep(delay * (2**attempt))  # Exponential backoff
                    else:
                        self.logger.error(
                            f"Max retries reached for date {current_date.strftime('%Y-%m-%d')}. Skipping."
                        )
                except Exception as e:
                    self.logger.error(
                        f"An error occurred for date {current_date.strftime('%Y-%m-%d')}: {e}"
                    )
                    break
            current_date += timedelta(days=1)

        self.logger.info("Process completed successfully.")

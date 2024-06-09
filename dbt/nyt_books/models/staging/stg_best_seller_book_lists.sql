{{
  config(
    materialized='table'

  )
}}

SELECT  *  from {{ source('airflow_db', 'best_seller_book_lists') }}

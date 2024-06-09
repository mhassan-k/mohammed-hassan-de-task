{{ config(
    materialized='incremental',
    unique_key='list_id'
) }}

with new_lists as (
    select distinct
        list_id,
        list_name,
        display_name,
        updated,
        published_date
    from {{ ref('stg_best_seller_book_lists') }}
    {% if is_incremental() %}
    where published_date > (select max(published_date) from {{ this }})
    {% endif %}
)

select
    list_id,
    list_name,
    display_name,
    updated
from new_lists

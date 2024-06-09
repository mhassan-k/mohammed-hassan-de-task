
{{ config(
    materialized='incremental',
    unique_key='publisher_id'
) }}

with new_publishers as (
    select distinct
        book_publisher,
        published_date
    from {{ ref('stg_best_seller_book_lists') }}
    {% if is_incremental() %}
    where published_date > (select max(published_date) from {{ this }})
    {% endif %}
),
publisher_ids as (
    select
        row_number() over(order by published_date) as publisher_id,
        book_publisher
    from new_publishers
)

select
    p.publisher_id,
    np.book_publisher
from new_publishers np
join publisher_ids p on np.book_publisher = p.book_publisher

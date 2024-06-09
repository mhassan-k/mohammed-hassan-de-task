{{ config(
    materialized='incremental',
    unique_key=['bestsellers_date', 'list_id', 'book_rank']
) }}

with rankings as (
    select
        bestsellers_date,
        list_id,
        book_rank,
        book_title,
        book_publisher,
        published_date
    from {{ ref('stg_best_seller_book_lists') }}
    {% if is_incremental() %}
    where published_date > (select max(published_date) from {{ this }})
    {% endif %}
)

select
    r.bestsellers_date,
    r.list_id,
    r.book_rank,
    b.book_id,
    p.publisher_id
from rankings r
left join {{ ref('dim_books') }} b on r.book_title = b.book_title
left join {{ ref('dim_publishers') }} p on r.book_publisher = p.book_publisher

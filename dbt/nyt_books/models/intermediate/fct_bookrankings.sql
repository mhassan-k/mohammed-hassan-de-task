{{ config(
    materialized='incremental',
    unique_key=['bestsellers_date', 'list_id', 'book_rank']
) }}

with base as (
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
),

book_ids as (
    select
        book_title,
        min(book_id) as book_id
    from {{ ref('dim_books') }}
    group by book_title
),

publisher_ids as (
    select
        book_publisher,
        min(publisher_id) as publisher_id
    from {{ ref('dim_publishers') }}
    group by book_publisher
)

select
    b.bestsellers_date,
    b.list_id,
    b.book_rank,
    bi.book_id,
    pi.publisher_id
from base b
left join book_ids bi on b.book_title = bi.book_title
left join publisher_ids pi on b.book_publisher = pi.book_publisher

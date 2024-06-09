{{ config(
    materialized='incremental',
    unique_key='book_id'
) }}

with new_books as (
    select distinct
        book_title,
        book_author,
        book_isbn,
        book_description,
        book_image,
        published_date
    from {{ ref('stg_best_seller_book_lists') }}
    {% if is_incremental() %}
    where published_date > (select max(published_date) from {{ this }})
    {% endif %}
),
book_ids as (
    select
        row_number() over(order by published_date) as book_id,
        book_title
    from new_books
)

select
    b.book_id,
    nb.book_title,
    nb.book_author,
    nb.book_isbn,
    nb.book_description,
    nb.book_image
from new_books nb
join book_ids b on nb.book_title = b.book_title

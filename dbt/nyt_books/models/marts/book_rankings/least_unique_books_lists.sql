{{ config(
    materialized='view'
) }}

select dl.list_name, count(distinct fb.book_id) as unique_books
from {{ ref('fct_bookrankings') }} fb
join {{ ref('dim_lists') }} dl on fb.list_id = dl.list_id
group by dl.list_name
order by unique_books asc
limit 3
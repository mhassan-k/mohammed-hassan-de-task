{{ config(
    materialized='view'
) }}

select book_title, count(*) as weeks_in_top_3
from {{ ref('fct_bookrankings') }} fb
join {{ ref('dim_books') }} db on fb.book_id = db.book_id
where book_rank <= 3 and extract(year from bestsellers_date) = 2022
group by book_title
order by weeks_in_top_3 desc
limit 1

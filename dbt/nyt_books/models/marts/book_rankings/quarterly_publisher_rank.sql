{{ config(
    materialized='view'
) }}

with PublisherScores as (
    select
        fb.publisher_id,
        date_part('quarter', fb.bestsellers_date) as quarter,
        extract(year from fb.bestsellers_date) as year,
        case
            when fb.book_rank = 1 then 5
            when fb.book_rank = 2 then 4
            when fb.book_rank = 3 then 3
            when fb.book_rank = 4 then 2
            when fb.book_rank = 5 then 1
            else 0
        end as score
    from {{ ref('fct_bookrankings') }} fb
)
select
    dp.book_publisher,
    ps.year,
    ps.quarter,
    sum(ps.score) as total_score,
    rank() over (partition by ps.year, ps.quarter order by sum(ps.score) desc) as rank
from PublisherScores ps
join {{ ref('dim_publishers') }} dp on ps.publisher_id = dp.publisher_id
group by dp.book_publisher, ps.year, ps.quarter
having rank <= 5

{{ config(
    materialized='view'
) }}

with JakeBooks as (
    select distinct fb.book_id, db.book_title, 'Jake' as team
    from {{ ref('fct_bookrankings') }} fb
    join {{ ref('dim_books') }} db on fb.book_id = db.book_id
    where fb.book_rank = 1 and year(fb.bestsellers_date) = 2023
),
PeteBooks as (
    select distinct fb.book_id, db.book_title, 'Pete' as team
    from {{ ref('fct_bookrankings') }} fb
    join {{ ref('dim_books') }} db on fb.book_id = db.book_id
    where fb.book_rank = 3 and year(fb.bestsellers_date) = 2023
),
SharedBooks as (
    select jb.book_id, jb.book_title, 'Jake' as team
    from JakeBooks jb

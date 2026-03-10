with base as (
    select * from {{ ref('stg_macro_indicators') }}
),

weekly as (
    select
        date_trunc('week', price_date) as week_start,
        market,
        round(avg(index_value)::numeric, 2) as avg_index,
        round(min(index_value)::numeric, 2) as min_index,
        round(max(index_value)::numeric, 2) as max_index,
        count(*) as trading_days
    from base
    group by 1, 2
)

select * from weekly
order by week_start, market

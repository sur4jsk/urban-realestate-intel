with base as (
    select * from {{ ref('stg_macro_indicators') }}
),

latest as (
    select
        market,
        round(avg(index_value)::numeric, 2) as avg_index_1y,
        round(min(index_value)::numeric, 2) as min_1y,
        round(max(index_value)::numeric, 2) as max_1y,
        round((max(index_value) - min(index_value))::numeric, 2) as range_1y,
        round(
            ((max(index_value) - min(index_value)) / min(index_value) * 100)::numeric,
        2) as pct_growth_1y,
        count(*) as total_days
    from base
    group by market
)

select * from latest

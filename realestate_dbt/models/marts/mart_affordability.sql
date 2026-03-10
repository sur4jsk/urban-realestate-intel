with base as (
    select * from {{ ref('stg_macro_indicators') }}
),

monthly as (
    select
        date_trunc('month', price_date) as month,
        market,
        round(avg(index_value)::numeric, 2) as avg_monthly_index,
        round(
            (avg(index_value)::numeric / lag(avg(index_value)::numeric)
            over (partition by market order by date_trunc('month', price_date)) * 100 - 100)
        , 2) as mom_growth_pct
    from base
    group by 1, 2
)

select * from monthly
order by month, market

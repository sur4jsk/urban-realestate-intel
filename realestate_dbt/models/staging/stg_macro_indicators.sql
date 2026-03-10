with source as (
    select * from macro_indicators
),

cleaned as (
    select
        date::date as price_date,
        index_value,
        market,
        fetched_at
    from source
    where index_value is not null
)

select * from cleaned

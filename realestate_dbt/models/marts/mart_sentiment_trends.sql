with base as (
    select * from news_sentiment
),

weekly as (
    select
        date_trunc('week', published_at::timestamp) as week_start,
        market,
        round(avg(sentiment_compound)::numeric, 4) as avg_sentiment,
        round(avg(sentiment_positive)::numeric, 4) as avg_positive,
        round(avg(sentiment_negative)::numeric, 4) as avg_negative,
        count(*) as article_count,
        round(avg(sentiment_neutral)::numeric, 4) as avg_neutral
    from base
    group by 1, 2
)

select * from weekly
order by week_start, market

{{ config(materialized='table') }}

select
    story_id,
    (array_agg(title order by snapshot_time desc))[1] as title,
    min(author)        as author,
    min(domain)        as domain,
    min(posted_time)   as posted_time,
    min(snapshot_time) as first_seen,
    max(snapshot_time) as last_seen,
    count(*)           as snapshots_seen,
    min(rank)          as best_rank,
    (array_agg(score order by snapshot_time))[1]      as first_score,
    (array_agg(score order by snapshot_time desc))[1] as last_score,
    max(score)         as peak_score
from {{ ref('stg_snapshots') }}
group by story_id

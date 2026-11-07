select snapshot_time, story_id, count(*) as copies from {{ source('hn', 'hn_snapshots') }} group by snapshot_time, story_id having count(*) > 1

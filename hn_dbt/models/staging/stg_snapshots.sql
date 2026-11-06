select id as row_id, snapshot_time, rank, story_id, title, author, score, comments_count, url, posted_time,
    regexp_replace(split_part(split_part(url, '://', 2), '/', 1), 'www\.', '') as domain,
    extract(epoch from (snapshot_time - posted_time)) / 3600.0 as age_hours
  from {{source('hn', 'hn_snapshots')}}
  where story_id is not null and title is not null and score >= 0

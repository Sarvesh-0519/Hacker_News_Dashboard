select * from {{source('hn', 'hn_snapshots')}} where score < 0 or comments_count < 0 or rank not between 1 and 100 or posted_time > snapshot_time

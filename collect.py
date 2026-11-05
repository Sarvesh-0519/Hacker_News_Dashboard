import sys
import time
import requests
import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

BASE_URL = "https://hacker-news.firebaseio.com/v0"
load_dotenv()


def fetch_json(url, tries=3):
    for attempt in range(1, tries + 1):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # turns errors like 500 into exceptions
            return response.json()
        except requests.RequestException as error:
            print(f"Attempt {attempt} failed for {url}: {error}")
            time.sleep(2)
    return None


def main():
    ids = fetch_json(f"{BASE_URL}/topstories.json")
    if ids is None:
        print("Could not get the story list. Giving up.")
        sys.exit(1)
    top_100 = ids[:100]

    conn = psycopg2.connect(
        host="localhost",
        port=6283,
        dbname="postgres",
        user="postgres",
        password=os.environ["DB_Password"],
    )

    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS hn_snapshots (
                id            SERIAL PRIMARY KEY,
                snapshot_time TIMESTAMPTZ NOT NULL,
                rank          INTEGER,
                story_id      BIGINT,
                title         TEXT,
                author        TEXT,
                score         INTEGER,
                comments_count      INTEGER,
                url           TEXT,
                posted_time   TIMESTAMPTZ
            );
        """)

        snapshot_time = datetime.now(timezone.utc)
        saved = 0

        for rank, story_id in enumerate(top_100, start=1):
            story = fetch_json(f"{BASE_URL}/item/{story_id}.json")
            if story is None:
                continue

            posted_time = None
            if "time" in story:
                posted_time = datetime.fromtimestamp(story["time"], tz=timezone.utc)

            cur.execute(
                """
                INSERT INTO hn_snapshots
                    (snapshot_time, rank, story_id, title, author, score, comments_count, url, posted_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    snapshot_time,
                    rank,
                    story.get("id"),
                    story.get("title"),
                    story.get("by"),
                    story.get("score"),
                    story.get("descendants"),
                    story.get("url"),
                    posted_time,
                ),
            )
            saved += 1

        if saved < 50:
            conn.rollback()
            print(f"Only {saved} stories collected. Nothing saved.")
            sys.exit(1)

        conn.commit()
        print(f"Done. Saved {saved} stories at {snapshot_time}")
    finally:
        conn.close()


main()

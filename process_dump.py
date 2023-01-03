import ujson
import duckdb
import glob

from datetime import datetime
from collections import deque

db = duckdb.connect("fadbuys-data.db")

sorts = ["new", "hot", "top"]
for sort in sorts:
    for path in glob.glob(f"archive/{sort}/*/*.json"):
        with open(path) as f:
            _, sort, subreddit, filename = path.split("/")
            print(f"Processing {sort}/{subreddit}/{filename}")
            data = ujson.load(f)
            created = datetime.fromtimestamp(data["created_utc"])

            # This is going to be VERY slow but I don't know a better
            # way to do the upserts yet.
            db.execute("delete from reddit_submissions where id = ?", [data["id"]])
            db.execute(
                """
            insert into reddit_submissions (
                id,
                title,
                name,
                url,
                selftext,
                score,
                upvote_ratio,
                permalink,
                author,
                num_comments,
                created_utc,
                sort,
                subreddit
            ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                [
                    data["id"],
                    data["title"],
                    data["name"],
                    data["url"],
                    data["selftext"],
                    data["score"],
                    data["upvote_ratio"],
                    data["permalink"],
                    data["author"],
                    data["num_comments"],
                    created,
                    sort,
                    subreddit,
                ],
            )

            comment_q = deque(data["comments"])

            while comment_q:
                comment = comment_q.popleft()

                created = datetime.fromtimestamp(comment["created_utc"])
                db.execute("delete from reddit_comments where id = ?", [comment["id"]])
                db.execute(
                    """
                insert into reddit_comments (
                    id,
                    author,
                    score,
                    submission,
                    body,
                    created_utc,
                    parent_id,
                    name
                ) values (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    [
                        comment["id"],
                        comment["author"],
                        comment["score"],
                        comment["submission"],
                        comment["body"],
                        created,
                        comment["parent_id"],
                        f"t1_{comment['id']}",
                    ],
                )

                comment_q.extend(comment["replies"])

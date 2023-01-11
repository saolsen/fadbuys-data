import duckdb
from logsnag import LogSnag

import os

api_key = os.environ["LOGSNAG_API_KEY"]

logsnag = LogSnag(token=api_key, project="steveindusteves")

logsnag.publish(
    channel="fadbuys-data",
    event="Sync Success",
    description="Successfully synced data from Reddit.",
    icon="✅",
    notify=False,
)

(num_submissions,) = (
    duckdb.connect("fadbuys-data.db")
    .execute("SELECT count(*) FROM reddit_submissions")
    .fetchone()
)

logsnag.insight(
    title="Number of Reddit Submissions",
    value=num_submissions,
    icon=" 🧩",
)

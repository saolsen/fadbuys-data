from logsnag import LogSnag

import os

api_key = os.environ["LOGSNAG_API_KEY"]

logsnag = LogSnag(token=api_key, project="steveindusteves")

logsnag.publish(
    channel="fadbuys-data",
    event="Sync Failure",
    description="Error syncing data from Reddit.",
    icon="❌",
    notify=True,
)

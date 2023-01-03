CREATE TABLE reddit_submissions (
    id VARCHAR PRIMARY KEY,
    title VARCHAR,
    name VARCHAR,
    url VARCHAR,
    selftext VARCHAR,
    score INTEGER,
    upvote_ratio REAL,
    permalink VARCHAR,
    author VARCHAR,
    num_comments INTEGER,
    created_utc TIMESTAMP,
    sort VARCHAR,
    subreddit VARCHAR,
);

CREATE TABLE reddit_comments (
    id VARCHAR PRIMARY KEY,
    author VARCHAR,
    score INTEGER,
    submission VARCHAR,
    body VARCHAR,
    created_utc TIMESTAMP,
    parent_id VARCHAR,
    name VARCHAR,
);

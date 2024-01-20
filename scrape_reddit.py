import praw
import json
import os
from dotenv import load_dotenv

load_dotenv()
reddit_password = os.getenv("REDDIT_PASS")

reddit = praw.Reddit(
    client_id="W9tvH4aQUgjjfg3vG5SRiQ",
    client_secret="47gt5VFEictQUWbeCXr9i0h6Qb3EGQ",
    password=reddit_password,
    user_agent="script by u/Longjumping_Tea_3516",
    username="Longjumping_Tea_3516",
)
rpurdue = reddit.subreddit("Purdue")


course_docs = []
with open("data/course_docs.json", "r") as json_file:
   course_docs = json.load(json_file)


queries = []
for course in course_docs:
    code = course["code"]
    title = course["title"]
    instructors = course["instructors"]
    instructor_query = "".join([f' OR "{name}"' for name in instructors])
    query = f'{code} or "{code}"{instructor_query}'
    # print(query)
    queries.append(query)

last_completed_query = queries[3260 + 507]
print("last completed: ", last_completed_query)
start_scraping = False
with open("data/reddit_docs.jsonl", "a") as file:
    all_docs = []
    for query in queries:
        if query == last_completed_query:
            start_scraping = True
            continue
        if not start_scraping: continue
        # print(query)
        code = query[:query.index('or')].strip()
        print(code)
        for submission in rpurdue.search(query, sort='new'):
            # add post to docs
            submission_title = submission.title
            submission_body = submission.selftext
            doc = f"POST_TITLE: {submission_title} | BODY: {submission_body}"
            all_docs.append(doc)
            # print(doc)
            # get comments of the post
            submission.comment_sort = "top"
            submission.comments.replace_more(limit=0)
            comments = submission.comments.list()
            for comment in comments:
                doc = f"POST_TITLE: {submission_title} | COMMENT_BODY: {comment.body}"
                entry = {
                    "code": code,
                    "chunk": doc
                }
                all_docs.append(entry)
                file.write(json.dumps(entry))
                file.write("\n")
                # print(doc)
        file.flush()

# with open("data/reddit_docs.json", 'w') as file:
#     json.dump(all_docs, file, indent=2)
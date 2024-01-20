import praw
import json

reddit = praw.Reddit(
    client_id="W9tvH4aQUgjjfg3vG5SRiQ",
    client_secret="47gt5VFEictQUWbeCXr9i0h6Qb3EGQ",
    password="moocow22pig",
    user_agent="script by u/Longjumping_Tea_3516",
    username="Longjumping_Tea_3516",
)
rpurdue = reddit.subreddit("Purdue")


course_docs = []
with open("data/course_docs.json") as json_file:
   course_docs = json.load(json_file)


queries = []
for course in course_docs:
    code = course["code"]
    title = course["title"]
    instructors = course["instructors"]
    instructor_query = [f' OR "{name}"' for name in instructors]
    query = f'{code} or "{code}"{instructor_query}'
    print(query)
    queries.append(queries)

# all_docs = []
# for query in queries:
#     print(query)
#     code = query[:query.index_of('or')].strip()
#     for submission in rpurdue.search(query, sort='new'):
#         # add post to docs
#         submission_title = submission.title
#         submission_body = submission.selftext
#         doc = f"POST_TITLE: {submission_title} | BODY: {submission_body}"
#         all_docs.append(doc)
#         # get comments of the post
#         submission.comment_sort = "top"
#         submission.comments.replace_more(limit=0)
#         comments = submission.comments.list()
#         for comment in comments:
#             doc = f"POST_TITLE: {submission_title} | COMMENT_BODY: {comment.body}"
#             all_docs.append({
#                 "code": code,
#                 "chunk": doc
#             })


# with open("data/reddit_docs.json", 'w') as file:
#     json.dump(all_docs, file, indent=2)
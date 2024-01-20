# from convokit import Corpus, download

# subreddit = 'subreddit-Purdue'
# corpus_size = 20_000
# corpus = Corpus(filename=download(subreddit))
# five_years_ago = 1547987415
# comments = [utterance.timestamp for utterance in corpus.iter_utterances() if (len(utterance.text.split(' ')) > 10)]
# documents = comments
# print(documents[-1])
import requests
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
submissions = []
course_docs = []
with open("data/course_docs.json") as json_file:
   course_docs = json.load(json_file)

base = "https://www.boilerclasses.com/api/get?detailId="

new_course_docs = []
for course in course_docs:
    instructors = []
    combined = (course["code"] + course["title"]).replace(" ", "")
    print(combined)
    endpoint = base + combined
    response = requests.get(endpoint)
    data = response.json()
    if ("total" not in data['course']) or data['course']['total'] == 0: continue
    data = response.json()['course']['documents'][0]['value']
    print(data)
    if "instructor" in data:
        print(data)
        instructors = list(data["instructor"].values())
        instructors = list(set([item[0] for item in instructors]))
        print(instructors)
    course["instructors"] = instructors
    new_course_docs.append(course)
    print("---")

with open("data/course_docs.json", 'w') as file:
    json.dump(new_course_docs, file, indent=2)


# for submission in rpurdue.search('CS182 OR "CS 182"  OR "Elisha Sacks" OR "Sarah Sellke"', sort='new'):
#     submissions.append(submission)
#     print(submission.title)
# print(len(submissions))

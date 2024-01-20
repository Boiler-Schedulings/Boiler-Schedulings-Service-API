from convokit import Corpus, download

subreddit = 'subreddit-Purdue'
corpus_size = 20_000
corpus = Corpus(filename=download(subreddit))
five_years_ago = 1547987415
comments = [utterance.timestamp for utterance in corpus.iter_utterances() if (len(utterance.text.split(' ')) > 10)]
documents = comments
print(documents[-1])
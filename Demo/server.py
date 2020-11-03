from flask import Flask, request
import os
from naturalSort import natural_keys 
from papers import papers 
import nltk
import math
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Read and prepare the files
filesList = os.listdir("./data")
filesList.sort(key=natural_keys)
filesList = filesList[1:]

def read_files_into_string(filenames):
    strings = []
    for filename in filenames:
        with open(f'data/federalist_{filename}.txt') as f:
            strings.append(f.read())
    return '\n'.join(strings)

federalist_by_author = {}
for author, files in papers.items():
    federalist_by_author[author] = read_files_into_string(files)

authors = ("Hamilton", "Madison", "Disputed", "Jay", "Shared")

# Transform the authors' corpora into lists of word tokens
federalist_by_author_tokens = {}
federalist_by_author_length_distributions = {}
for author in authors:
    tokens = nltk.word_tokenize(federalist_by_author[author])

    federalist_by_author_tokens[author] = ([token for token in tokens
                                            if any(c.isalpha() for c in token)])

@app.route('/kilgariff')
def kilgariff():
    authors = ("Hamilton", "Madison", "Jay")

    output = {}
    for author in authors:
        federalist_by_author_tokens[author] = (
            [token.lower() for token in federalist_by_author_tokens[author]])
    federalist_by_author_tokens["Disputed"] = (
        [token.lower() for token in federalist_by_author_tokens["Disputed"]])

    for author in authors:
        joint_corpus = (federalist_by_author_tokens[author] +
                        federalist_by_author_tokens["Disputed"])
        joint_freq_dist = nltk.FreqDist(joint_corpus)
        most_common = list(joint_freq_dist.most_common(500))

        author_share = (len(federalist_by_author_tokens[author])
                        / len(joint_corpus))
        

        chisquared = 0
        for word,joint_count in most_common:
            author_count = federalist_by_author_tokens[author].count(word)
            disputed_count = federalist_by_author_tokens["Disputed"].count(word)

            expected_author_count = joint_count * author_share
            expected_disputed_count = joint_count * (1-author_share)

            chisquared += ((author_count-expected_author_count) *
                        (author_count-expected_author_count) /
                        expected_author_count)

            chisquared += ((disputed_count-expected_disputed_count) *
                        (disputed_count-expected_disputed_count)
                        / expected_disputed_count)

        output[author] = chisquared

    return output

@app.route('/burrows')
def burrows():
    authors = ("Hamilton", "Madison", "Jay")

    for author in authors:
        federalist_by_author_tokens[author] = (
            [tok.lower() for tok in federalist_by_author_tokens[author]])

    whole_corpus = []
    for author in authors:
        whole_corpus += federalist_by_author_tokens[author]

    whole_corpus_freq_dist = list(nltk.FreqDist(whole_corpus).most_common(30))

    features = [word for word,freq in whole_corpus_freq_dist]
    feature_freqs = {}

    for author in authors:
        feature_freqs[author] = {}

        overall = len(federalist_by_author_tokens[author])

        for feature in features:
            presence = federalist_by_author_tokens[author].count(feature)
            feature_freqs[author][feature] = presence / overall
    corpus_features = {}

    for feature in features:
        corpus_features[feature] = {}

        feature_average = 0
        for author in authors:
            feature_average += feature_freqs[author][feature]
        feature_average /= len(authors)
        corpus_features[feature]["Mean"] = feature_average

        feature_stdev = 0
        for author in authors:
            diff = feature_freqs[author][feature] - corpus_features[feature]["Mean"]
            feature_stdev += diff*diff
        feature_stdev /= (len(authors) - 1)
        feature_stdev = math.sqrt(feature_stdev)
        corpus_features[feature]["StdDev"] = feature_stdev

    feature_zscores = {}
    for author in authors:
        feature_zscores[author] = {}
        for feature in features:

            feature_val = feature_freqs[author][feature]
            feature_mean = corpus_features[feature]["Mean"]
            feature_stdev = corpus_features[feature]["StdDev"]
            feature_zscores[author][feature] = ((feature_val-feature_mean) /
                                                feature_stdev)

    testcase_tokens = nltk.word_tokenize(federalist_by_author["TestCase"])

    testcase_tokens = [token.lower() for token in testcase_tokens
                    if any(c.isalpha() for c in token)]

    overall = len(testcase_tokens)
    testcase_freqs = {}
    for feature in features:
        presence = testcase_tokens.count(feature)
        testcase_freqs[feature] = presence / overall

    testcase_zscores = {}
    for feature in features:
        feature_val = testcase_freqs[feature]
        feature_mean = corpus_features[feature]["Mean"]
        feature_stdev = corpus_features[feature]["StdDev"]
        testcase_zscores[feature] = (feature_val - feature_mean) / feature_stdev

    deltas = {}
    for author in authors:
        delta = 0
        for feature in features:
            delta += math.fabs((testcase_zscores[feature] -
                                feature_zscores[author][feature]))
        delta /= len(features)
        deltas[author] = delta
    return deltas

app.run("127.0.0.1", 3000)
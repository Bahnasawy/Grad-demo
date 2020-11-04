from papers import papers 
import nltk
import math
import copy

def read_files_into_string(filenames):
        strings = []
        for filename in filenames:
            with open(f'data/federalist_{filename}.txt') as f:
                strings.append(f.read())
        return '\n'.join(strings)

def burrows(disputedPaper, disputedAuthor):
    papersList = copy.deepcopy(papers)
    papersList[disputedAuthor].remove(disputedPaper)
    output = {}
    output["results"] = {}

    federalist_by_author = {}
    for author, files in papersList.items():
        federalist_by_author[author] = read_files_into_string(files)
    federalist_disputed = ""
    with open(f'data/federalist_{disputedPaper}.txt') as f:
            federalist_disputed = f.read()

    authors = ("Hamilton", "Madison", "Jay")

    # Transform the authors' corpora into lists of word tokens
    federalist_by_author_tokens = {}
    for author in authors:
        tokens = nltk.word_tokenize(federalist_by_author[author])

        federalist_by_author_tokens[author] = ([token for token in tokens
                                                if any(c.isalpha() for c in token)])

    tokens = nltk.word_tokenize(federalist_disputed)
    federalist_disputed_tokens = ([token for token in tokens
                                if any(c.isalpha() for c in token)])

    for author in authors:
        federalist_by_author_tokens[author] = (
            [tok.lower() for tok in federalist_by_author_tokens[author]])
    federalist_disputed_tokens = (
        [token.lower() for token in federalist_disputed_tokens])


    # Prep Data Processing
    whole_corpus = []
    for author in authors:
        whole_corpus += federalist_by_author_tokens[author]

    whole_corpus_freq_dist = list(nltk.FreqDist(whole_corpus).most_common(30))
    output["mostCommon"] = whole_corpus_freq_dist

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

    # Test Data Processing

    overall = len(federalist_disputed_tokens)
    testcase_freqs = {}
    for feature in features:
        presence = federalist_disputed_tokens.count(feature)
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
    output["results"] = deltas
    return output

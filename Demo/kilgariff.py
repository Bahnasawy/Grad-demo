from papers import papers 
import nltk

def kilgariff(disputedPaper, disputedAuthor):
    papersList = list(papers)
    papersList[disputedAuthor].remove(disputedPaper)
    output = {}
    output["results"] = {}

    def read_files_into_string(filenames):
        strings = []
        for filename in filenames:
            with open(f'data/federalist_{filename}.txt') as f:
                strings.append(f.read())
        return '\n'.join(strings)

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
            [token.lower() for token in federalist_by_author_tokens[author]])
    federalist_disputed_tokens = (
        [token.lower() for token in federalist_disputed_tokens])

    for author in authors:
        joint_corpus = (federalist_by_author_tokens[author] +
                        federalist_disputed_tokens)
        joint_freq_dist = nltk.FreqDist(joint_corpus)
        most_common = list(joint_freq_dist.most_common(500))
        output["mostCommon"] = most_common

        author_share = (len(federalist_by_author_tokens[author])
                        / len(joint_corpus))

        chisquared = 0
        for word,joint_count in most_common:
            author_count = federalist_by_author_tokens[author].count(word)
            disputed_count = federalist_disputed_tokens.count(word)

            expected_author_count = joint_count * author_share
            expected_disputed_count = joint_count * (1-author_share)

            chisquared += ((author_count-expected_author_count) *
                        (author_count-expected_author_count) /
                        expected_author_count)

            chisquared += ((disputed_count-expected_disputed_count) *
                        (disputed_count-expected_disputed_count)
                        / expected_disputed_count)

        output["results"][author] = chisquared

    return output


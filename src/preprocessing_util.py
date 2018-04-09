from collections import Counter
import re
import string

import spacy
from tqdm import tqdm


nlp = spacy.load('en')
punctuations = string.punctuation
stopwords = nlp.Defaults.stop_words


# function that removes the headers from the document
def clean_headers(article, keep_history=True):
    lines = article.splitlines()
    new_article = []
    index = 0
    for i in range(len(lines)):
        if not lines[i]:
            index = i
            break
        if lines[i].startswith('Subject'):
            new_article.append(lines[i])

    if not keep_history:
        new_lines = remove_history(lines[index:])
        new_article..extend(new_lines)
    else:
        new_article.extend(lines[index:])

    new_article = [t for t in new_article if t]

    return '\n'.join(new_article)


# function to remove chat history from document
def remove_history(lines):
    clean_lines = []
    for line in lines:
        if not line.startswith('>'):
            clean_lines.append(line)

    return clean_lines

# function to cleanup text by removing personal pronouns, stopwords, and puncuation and count occurances of words
def cleanup_text(doc):
    doc = nlp(doc, disable=['parser', 'ner'])
    tokens = [tok.lemma_.lower().strip() for tok in doc if tok.lemma_ != '-PRON-']
    tokens = [tok for tok in tokens if tok not in stopwords and tok not in punctuations]

    # 's appears a lot in the text, so it should be removed since it's not a word
    tokens = [tok for tok in tokens if tok != '\'s']

    words_count = Counter(tokens)
    text = ' '.join(tokens)
    return (text, words_count)


def preprocess(article, keep_history=True):
    article = clean_headers(article, keep_history)
    clean_text, words_count = cleanup_text(article)

    return (clean_text, words_count)

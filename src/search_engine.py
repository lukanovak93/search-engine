import string

import spacy

from preprocessing_util import cleanup_text, clean_headers, preprocess

class SearchEngine:
    """class that models search engine"""

    def __init__(self, vocab, documents):
        self.vocab = vocab
        self.documents = documents

    def initialize_database(src_path):
        for doc in _get_files(src_path):
            # TODO: Think about not returning clean text at all, just words counter
            text, words_count = preprocess(doc)
            # TODO: maybe function for adding a doc to both tables
            db_entry = _create_db_entry()

    def _get_files(base_dir):
        for entry in os.scandir(base_dir):
            if entry.is_file():
                yield entry.path
            elif entry.is_dir():
                yield from _get_files(entry.path)


    def _create_vocab_entry(words_count, doc_id):
        for word in words_count.keys():
            try:
                docs = vocab.find({'Word':word})
            except KeyError:
                docs = set()
            docs.add(doc_id)

    def _create_documents_entry(words_count, doc_id):
        for word, count in words_count.items():












# nlp = spacy.load('en')
#
# punctuations = string.punctuation
#
# stopwords = nlp.Defaults.stop_words

text = '''Distribution1: na
Lines1: 18
From: decay@cbnewsj.cb.att.com (dean.kaflowitz)
Subject: Re: about the bible quiz answers
Organization: AT&T
Distribution2: na
Lines2: 18

bla bla bla
bla

blabla'''

print(text)
print('****')
result_text, result_count = preprocess(text)
print(result_text)
print(result_count)

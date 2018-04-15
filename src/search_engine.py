from collections import Counter, OrderedDict
from operator import itemgetter
import os
import sys
import string

import pymongo
import spacy
from tqdm import tqdm

from preprocessing_util import cleanup_text, clean_headers, preprocess
from search_engine_util import _get_files

class SearchEngine:
    """class that models search engine"""

    def __init__(self, vocab, documents):
        self.vocab = vocab
        self.documents = documents

    def add_to_database(self, src_path):
        if os.path.exists(src_path):
            if os.path.isdir(src_path):
                elems = []
                for e in _get_files(src_path):
                    elems.append(e)
                for doc in tqdm(elems[:20]):
                    with open(doc, 'r') as f:
                        article = f.read()
                    text, words_count = preprocess(article)
                    self._insert(words_count, doc)
            elif os.path.isfile(src_path):
                with open(doc, 'r') as f:
                    article = f.read()
                text, words_count = preprocess(article)
                self._insert(words_count, doc)
        else:
            print('File or directory does not exist!')

    def _insert(self, words_count, doc_id):
        for word in words_count.keys():
            entry = self.vocab.find_one({'word':word})
            if not entry or doc_id not in entry['docs']:
                self.vocab.update_one({'word':word}, {'$push': {'docs':doc_id}}, upsert=True)

        self.documents.update_one({'doc': doc_id}, {'$push':{'words': dict(words_count)}}, upsert=True)

    def _query_word(self, w):
        entry = self.vocab.find_one({'word': w})
        if entry:
            docs = entry['docs']
            if docs:
                idf = 1/len(docs)
            else:
                return {}

            res = {}
            for doc_id in docs:
                document = self.documents.find_one({'doc': doc_id})
                words = dict(document['words'][0])
                s_words = sum(words.values())
                tf = words[w]/s_words
                res[doc_id] = tf*idf

            return OrderedDict(sorted(res.items(), reverse=True, key=itemgetter(1)))

        else:
            return {}

    def query(self, q):
        _, words_count = preprocess(q)
        words = list(words_count.keys())

        res = []
        for word in words:
            res.append(self._query_word(word))

        result = Counter()
        for r in res:
            result += Counter(r)

        return OrderedDict(sorted(result.items(), reverse=True, key=itemgetter(1)))

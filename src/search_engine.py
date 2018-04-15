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
                for doc in tqdm(elems):
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


    def _check_all_words(self, q_words, docs):
        res_list = []
        for doc_id in docs:
            document = self.documents.find_one({'doc': doc_id})
            if all(elem in document['words'][0] for elem in q_words):
                res_list.append(doc_id)

        return res_list


    def _query_word(self, q_words):
        word = q_words[0]
        entry = self.vocab.find_one({'word': word})
        if entry:
            docs = entry['docs']
            if docs:
                idf = 1/len(docs)
            else:
                return {}

            term_docs = self._check_all_words(q_words, docs)

            idfs = {}
            for i in q_words:
                w = self.vocab.find_one({'word':i})
                idfs[i] = 1/len(w['docs'])

            doc_tfidf = {}
            for doc_id in term_docs:
                document = self.documents.find_one({'doc': doc_id})
                words = dict(document['words'][0])
                s_words = sum(words.values())
                tf_idf_doc = 0
                for w in q_words:
                    tf = words[w]/s_words
                    tf_idf_doc += tf*idfs[w]

                doc_tfidf[doc_id] = tf_idf_doc

            return doc_tfidf

        else:
            return {}

    def query(self, q):
        _, words_count = preprocess(q)
        q_words = list(words_count.keys())

        result = self._query_word(q_words)

        # res = []
        # for word in q_words:
        #     res.append(self._query_word(q_words))
        #
        # result = Counter()
        # for r in res:
        #     result += Counter(r)

        return OrderedDict(sorted(result.items(), reverse=True, key=itemgetter(1)))

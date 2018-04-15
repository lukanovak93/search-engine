from subprocess import call
import sys
import pymongo

from search_engine import SearchEngine

if __name__ == '__main__':

    client = pymongo.MongoClient(maxPoolSize=None)
    db = client.NewDB2
    vocab = db.Vocab
    documents = db.Documents

    cursor_v = vocab.find({})
    cursor_d = documents.find({})

    search_engine = SearchEngine(vocab, documents)

    if not cursor_v.count() and not cursor_d.count():
        search_engine = SearchEngine(vocab, documents)
        print('Initializing database...')
        search_engine.add_to_database('data/20news-bydate-train')
        search_engine.add_to_database('data/20news-bydate-test')
        print('Initialized successfully!')

    print('''
Now You can type the query. If You wish to add an document or list of documents to the database, type `add path/to/file/or/folder`. If you whish to exit the search engine just type `exit` or `quit`.
    ''')

    while True:
        query = input('Search: ').lower()
        if query in ['bye', 'goodbye', 'exit', 'quit']:
            print('\nGoodbye!')
            # call('mongodump --archive=database/db_dump.archive --db db')
            sys.exit(1)
        elif query.startswith('add'):
            search_engine.add_to_database(query.split()[-1])
        else:
            ranked_results = search_engine.query(query)
            print('\nNumber of results: ' + str(len(ranked_results)) + '\n')

            cnt = 0
            for doc, score in ranked_results.items():
                cnt += 1
                print('{0}. Document: {1}\tScore: {2:.4f}'.format(cnt, '/'.join(doc.split('/')[-2:]), score))
                print()

# search-engine
Search engine made to query terms in documents and rank the result documents based on their TF-IDF value.

## Setup
Clone this repository. Then type:

`cd search-engine`

Give the setup script executable permission by typing:

`chmod +x setup.sh`

Then run setup script to install everything needed for search-engine to work:

`sudo ./setup.sh`

This script downloads [20 newsgroups dataset](http://qwone.com/~jason/20Newsgroups/) and puts it in the `data` folder. Then it  installs [pipenv](https://robots.thoughtbot.com/how-to-manage-your-python-projects-with-pipenv) and everything else inside it.

Run search-engine by typing:

`pipenv run python src/main.py`

# System information
The search-engine is developed on 64-bit Ubuntu 16.04
Processor: Intel® Core™ i5-2450M CPU @ 2.50GHz × 4
RAM: 4GB

# Implementation details
This is very simple system that has 3 components:

- Database
    - [MongoDB](https://www.mongodb.com/) is used for storing the data. The interface for the database is [PyMongo](https://api.mongodb.com/python/current/). The database has 2 collections:
        - Vocab - used for storing words as a key and list of documents that contain that word as a value
        - Documents - used for storing relative document path as a key and a dictionary of a words counter in that document as a value.


- Search Engine class
    - Class that models search engine. It takes two collections as parameters and initializes them in `add_to_database` function. The same function can also be used for adding new documents to the database. It takes a path as an argument and if path is to a file then adds it to the database, and if path points to a directory, then adds all the documents from that directory to the database (like bulk insert).
    - Furthermore, it has query function that takes a query and returns a dictionary ordered by values. The keys in the dictionary are the document paths and the values are the tf-idf measures calculated by the query words.

- Utils
    - `preprocessing_util.py` is a script that preprocesses the text. It uses [Spacy](https://spacy.io/) library for text preprocessing. This script takes the text, tokenizes it, lemmatizes it, removes stopwords,
    removes unuseful headers, removes personal pronouns and punctuations and counts occurances of words in that text.
    - `search_engine_uitl.py` has only one function inside it and that is a generator that yields the paths to a files in a root folder.


- `main.py` is a script where a main program is. It runs the MongoDB, makes a connection to a database and checks if database already exists. If it exists, uses it, and if not, it initializes it with 20 newsgroups dataset from `data` folder. Then it hangs in a loop where user can query terms or add new documents to the database by typing `add path/to/folder/or/document`. If user searches the term(s), it returns the list of documents, ordered by TF-IDF measure values of query term(s). To exit the program, just type `exit` or `quit`.

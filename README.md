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

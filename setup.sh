sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2930ADAE8CAF5059EE73BB4B58712A2291FA4AD5
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.6 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.6.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo pip3 install pipenv
sudo pipenv install
sudo pipenv run python -m spacy download en
wget http://qwone.com/~jason/20Newsgroups/20news-bydate.tar.gz
tar -xzf 20news-bydate.tar.gz
rm 20news-bydate.tar.gz
mkdir data
mv 20news-bydate-test 20news-bydate-train data

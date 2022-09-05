# bwl-wordle-web-scraper
Repository for the web scraper part of our main repository. See https://github.com/3k-dome/bwl-wordle.

Utility scripts to collect the words for our wordle game.

```scraper.py``` simply runs the webscraper and collects all words, needs parameters ```--min``` and ```--max``` to specify the allowed word length, i.e. run ```python scraper.py --min 4 --max 6``` to download all words with length of [4:6]. Words are stored under ```/cache```.

```prepper.py``` simply converts the words into a format which can than be red by our main application.

A curated list of bussines words ```bussines_.json``` is provided and used by ```prepper.py```.

# install

Python 3.10+ is required. To install simply run the following commands in the project root open.

```
python -m venv venv
./venv/Scripts/Activate.ps1
python -m pip install -r requirements.txt
```

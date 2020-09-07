# Personalized Music Recommendations

This is a personal project to expand my skills in data wrangling, machine learning and general Python. It's a music project where I combined labeled data from Pandora with the Spotify audio features to create a classifier model that predicts if I or any user of Pandora would like a new song. I used data from Pandora because it was my main music player for years which means it has lots of liked and unliked songs. Currently they do not have a personal developer API which is why I had to use Spotify's API. Spotify does have their own recommendation endpoint but would require the user to have Spotify music data which I do not.

## Installation

Use the [Anaconda](https://anaconda.org/anaconda/python) distribution of Python. This project is in Python 3.7.7 with Conda 4.8.4
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install these dependencies.

```bash
pip install selenium
pip install beautifulsoup4
pip install spotipy
```

## Usage

```python
The [main notebook](https://github.com/vphan404/Personalized-Music-Recommendations/blob/master/main.ipynb) should lay out how you can use this program.
```

## License

[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)

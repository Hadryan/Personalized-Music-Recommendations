# Personalized Music Recommendations

A music program where I combined labeled data from Pandora with Spotify audio features to create a classifier model that predicts if I or any Pandora user would like a new song.

## Motivation

This is a personal project to expand my data wrangling, machine learning, and general Python skills. I merged two of my most significant interests to do a project that excited me and kept me wanting to learn. I think AI is the future, and creating a specialized tool for music was very fulfilling.

I used Pandora's data because it was my primary music player for years, which means it has many of my liked and unliked songs. They do not have a personal developer API, so I had to use Spotify's API for song features. Spotify does have a recommendation endpoint but would require the user to have Spotify music data in the form of liked songs or playlists.

<!-- I web scraped the data off of Pandora using Selenium because many elements on the webpage used JavaScript to load in. -->

## Requirements

Use the [Anaconda](https://anaconda.org/anaconda/python) distribution of Python. This project is in Python 3.7.7 with Conda 4.8.4.\
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install these dependencies. You may use the -U flag e.g. _pip -U install package_ to also update to the newest version.

```bash
# Parsing HTML documents and easily extracting data from HTML.
pip install beautifulsoup4
# Automating interaction with the browser.
pip install selenium
# Simplifies Spotify API usage.
pip install spotipy
# Creating deep learning models.
pip install tensorflow
pip install tensorflow-addons
```

These should come with Anaconda.

```bash
# interactive Python shell. Allows easy prototyping.
pip install ipython
# Used for saving models.
pip install joblib
# Creating data visualization.
pip install matplotlib
# Working with arrays.
pip install numpy
# USeful data structure for manipulation and analysis.
pip install pandas
# Creating classical models.
pip install scikit-learn
# High level interface to matplotlib.
pip install seaborn
```

## How-to

The [main notebook](https://github.com/vphan404/Personalized-Music-Recommendations/blob/master/main.ipynb) demonstrates how to use the program.

## License

[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)

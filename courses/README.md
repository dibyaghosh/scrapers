## Berkeley Guide Scraper

This python script scrapes all the courses offered by Berkeley in recent years.
The program is simple to run, and saves to a SQL database when run.

# Installation

Create a conda environment using

	conda create --name ENV_NAME python=3.4

Install from the list of requirements.


	pip install -r requirements.txt

# How to Run

To run the visualization, do the following. We assume that you have already started your conda environment using

	source activate ENV_NAME

1) If the database hasn't already been created (e.g. this is the first time you are running the scraper), run the following

  python models.py

2) To run the scraper, run the following (and let it finish)

	python scraper.py

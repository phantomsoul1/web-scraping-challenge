# web-scraping-challenge
Web Scraping assignment for Rutgers Data Science Bootcamp.

Details on the assigment are available in the readme file within the Instructions folder here.

## Prerequisites
* MongoDB - installed and running.
    * Modify the URI in *config.py* as necessary if not the community version on localhost
* Python libraries
    * Beautiful Soup 4 (https://www.crummy.com/software/BeautifulSoup/bs4/doc/#)
    * Splinter (https://splinter.readthedocs.io/en/latest/index.html)
        * Requires Google Chrome
        * Set path to 'chromedriver' in the *config.py* file
    * pprint (for diagnostic printouts)
    * SQLAlchemy (https://www.sqlalchemy.org)

## Execution
Once prequisites are met, the scraper can be run by executing the *app.py* file in the *Missions_to_Mars* folder and opening the link produced by SQLAlchemy Flask. This will load a dummy webpage (for performance reasons); Mars data can be loaded by clicking the link to scrape new data.

This app was written and tested with Python 3.7.6

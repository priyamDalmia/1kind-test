## 1kind-test
1kind Job Interview test solutions.

A general web-scrapper and PostgrSQL database manager!

### Tasks. 

1. Create, host and launch a postgresql database on AWS.
2. Build a small python app to populate the database with articles scrapped from the web.
3. Query the results and present an analysis.

## Getting Started.

1. Clone the poject. 
2. Create a virtual environment and install the requirments.

## Running the code.

1. Populate the *config.yaml* file with the credentials provided. Once that is completed, run the command: `python3 tests/test_remote_connection.py`. The output should confirm that a sucessfull connection has been established. 

## Scraping and storing BBC new articles.

1. class `Scraper`: (/scraper.py) contains the scrapper. The scraper class uses its config `ScraperConfig` to crawl and scrape a site for news articles. Any article with topics given in the keywords list will be extracted and stored. 

2. class `DB_Writer`: (/access_database.py) contains the database writer. The writer will request items (articles + data) from the scrapper, calculate the sentiments and make an entry in appropriate table. The schema for table creation is persent as a global variable and can be changed easily to incorporate more fields.

## Recreating the results.

Don't beielve strangers on the internet. Use `run.py` to recreate the results yourself.

* `python3 run.py --checkhealth`: Shows if the cofiguration is correct and the DB can be accessed.   

* `python3 run.py --show_tables`: Prints the table names, schemas and other details. 

* `python3 run.py --clean_run`: Will delete the existing tables and re-scrape the sites. Use this command to scrape websites for different keywords. 


NOTE: `config.yaml` can be used to overwrite the default infile configuration. This allows for a central control of all configurable parameters. Arguments in this file take precedence over all default config files. 


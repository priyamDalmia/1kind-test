# 1kind-test
1kingd Job Interview test solutions.

# Tasks. 

1. Create, host and launch a postgresql database on AWS.
2. Build a small python app to populate the database with articles scrapped from the web.
3. Query the results and present an analysis.

# Getting Started.

1. Clone the poject. 
2. Create a virtual environment and install the requirments.

# Running the code.

1. Populate the *config.yaml* file with the credentails provided. Once that is completed, run the commands `python3 tests/test_remote_connection.py`. The output should confirm that a succesfull connection has been established. 

## Scraping and storing BBC new articles.

1. class `Scraper`: () contains the scrapper. The scraper class uses its config `ScraperConfig` to navigate and scrape a site for news articles. Any article with topics given in the keywords list will be extracted and stored. 

2. class `DB_Writer`: () contains the database writer. The writer will request items (articles + data) from the scrapper, calculate the sentiment and store in item in appropriate table. The schema for table creation is persent as a global variable and can be changed easily to incorporate more fields.


`python3 run.py --re`: Use this command to delete exsisting tables and re-populate the database with news articles. Scraping 500 articles should take approx <2mins.  


NOTE: `config.yaml` can be used to overwrite in file default configuration to allow a central control to all configurable parameters. This means that the arguments in this file take precednce over all default cofig files. 

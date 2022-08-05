import os
import yaml 

from access_database import DB_Reader, DB_Writer
from scraper import Scraper

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--checkhealth", action="store_true", description="")
parser.add_argument("--show_tables", action="store_true", description="")
parser.add_argument("--clean_run", action="store_true", description="")

## Run Checks and See if the setup is complete 
def checkhealth():
    pass

## Run and show the number of tables and items in each
def show_tables():
    pass

## delete exsisitng tables 
def delete_tables():
    pass

## Run, Delete and Re-scrape the data
def write_to_database():
    pass

if __name__ == "__main__":
    # parse arguments
    with open('config.yaml') as f:
        config = yaml.load(f, Loader = yaml.FullLoader)

    # get scraper
    scraper = Scraper()    
        
    # get reader 
    reader = DB_Reader(config)
    
    # get writer 
    writer = DB_Writer(config, scraper)
    
    breakpoint()


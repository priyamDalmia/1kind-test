import sys
import yaml 

from tests import test_remote_connection as trc
from access_database import DB_Reader, DB_Writer
from scraper import Scraper

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--checkhealth", action="store_true")
parser.add_argument("--show_tables", action="store_true")
parser.add_argument("--clean_run", action="store_true")

## Run Checks and See if the setup is complete 
def checkhealth(config):
    trc.test_remote_connection(config["postgres"])

## Run and show the number of tables and items in each
def show_tables(config, db_reader):
    db_reader.show_tables()

## delete exsisitng tables 
def delete_tables(config, db_writer):
    db_writer.delete_tables()

## Run, Delete and Re-scrape the data
def write_to_database():
    db_writer.record_to_database()

if __name__ == "__main__":
    # parse arguments
    args = parser.parse_args()
    with open('config.yaml') as f:
        config = yaml.load(f, Loader = yaml.FullLoader)
    
    if args.checkhealth:
        checkhealth(config)
        sys.exit()
 
    # get scraper
    scraper = Scraper()    
        
    # get reader 
    reader = DB_Reader(config)
    
    # get writer 
    writer = DB_Writer(config, scraper)
    
   
    if args.show_tables:
        show_tables(config, reader)


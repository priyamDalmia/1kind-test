import yaml
import traceback
from scraper import Scraper, ScraperConfig
from helpers import connect_to_db, get_sentiment 


# BASIC TABLE SCHEMA 
TABLE_SCHEMA = '''CREATE TABLE %s 
            (id         INT       PRIMARY KEY   NOT NULL,
            sentiment   REAL      NOT NULL,
            topic       TEXT      NOT NULL,
            title       TEXT      NOT NULL,
            subtitle    TEXT      NOT NULL,
            article     TEXT      NOT NULL,
            metadata    TEXT      NOT NULL);''' # % (table_name)

# Get all tables from the database
GET_TABLES = '''SELECT table_schema, table_name 
            FROM information_schema.tables
            WHERE (table_schema = 'public')'''

# Delete any table from the database
DELETE_TABLE = '''DROP TABLE %s'''

# Primary tables in the database
TABLE_POSITIVE = "positive"
TABLE_NEGATIVE = "negative" 

class DB_Reader:
    def __init__(self, config):
        self.config = config
        self.open_connection()
    
    def open_connection(self):
        self.connector, self.cursor = connect_to_db(self.config["postgres"])
    
    def read_from_table(self):
        breakpoint()
        table_name = "positive"
        GET_ITEMS = f'''SELECT * FROM {table_name}'''
        self.cursor.execute(GET_ITEMS)
        return self.cursor.fetchall()
    
    def show_tables(self):
        TABLE_INFO = '''SELECT * FROM %s'''
        
        self.cursor.execute(TABLE_INFO % TABLE_POSITIVE)
        table_info = self.cursor.description
        COL_NAMES = [col.name for col in table_info]
        print("\nTable Name: ", {TABLE_POSITIVE})
        print("With columns: ", COL_NAMES)
        print(table_info)

        self.cursor.execute(TABLE_INFO % TABLE_NEGATIVE)
        table_info = self.cursor.description
        COL_NAMES = [col.name for col in table_info]
        print("\nTable Name: ", {TABLE_NEGATIVE})
        print("With columns: ", COL_NAMES)
        print(table_info)

class DB_Writer:
    def __init__(self, config, scraper):
        self.config = config
        self.scraper = scraper
        self.delete_table = config["delete_tables"]

        # setup connections and get cursor
        self.open_connection()

    def open_connection(self):
        self.connector, self.cursor = connect_to_db(self.config["postgres"])

    def close_connection(self):
        pass

    def setup_tables(self):
        # checks if the tables are present 
        # if not creates the tables using the schema
        if self.delete_table:
            # first delete all tables
            self.delete_tables()

        self.cursor.execute(GET_TABLES)
        list_tables = self.cursor.fetchall()
        for table_name in [TABLE_POSITIVE, TABLE_NEGATIVE]:
            if sum(map(int, [table_name == i[1] for i in list_tables])):
                print(f"database contains table -> {table_name}")
            else:
                print(f"table -> {table_name} not found. new table created!")
                self.cursor.execute(TABLE_SCHEMA % (table_name))
                self.connector.commit()
    
    def delete_tables(self):
        self.cursor.execute(DELETE_TABLE % TABLE_POSITIVE)
        self.cursor.execute(DELETE_TABLE % TABLE_NEGATIVE)
        print("Deleted exsiting tables!")


    def record_to_database(self):
        # setup tables and start scraping and storing resutls.
        self.setup_tables()
        items_stored = {
                TABLE_POSITIVE: 0, 
                TABLE_NEGATIVE: 0}
        data_config = self.config["database"]
        total_items_stored = 0
        while total_items_stored < data_config["num_records"]:
            record_item = scraper.get_item()
            if (not record_item["id"]) and\
                    (not record_item["article"]):
                continue

            ## get sentiment for subtitles 
            sentiment = get_sentiment(record_item["subtitle"])
            if sentiment['pos'] > sentiment['neg']:
                item_sentiment = sentiment['pos']
                table = TABLE_POSITIVE
            else:
                item_sentiment = sentiment['neg']
                table = TABLE_NEGATIVE

            item_data = (
                    record_item["id"],
                    item_sentiment,
                    record_item["topic"],
                    record_item["title"],
                    record_item["subtitle"],
                    record_item["article"],
                    record_item["metadata"])
            
            store_sucess = self.store_item(table, item_data)
            items_stored[table] += int(store_sucess)
            total_items_stored = sum(list(items_stored.values()))
            if total_items_stored%10 == 0:
                print(f"Total items stored into the database: {total_items_stored}")
        
        # print total items stored in each data table.
        print(f"Total items stored: {items_stored}")

    def store_item(self, table_name, item_data):
        # insert item into table.
        INSERT_ITEM = f'''INSERT INTO {table_name} VALUES (%s, %s, %s, %s, %s, %s, %s) '''
        try:
            self.cursor.execute(INSERT_ITEM, item_data)
            self.connector.commit()
            return True
        except: 
            # ROLLBACK TRANSACTION if insert error
            # traceback.print_exc()
            self.connector.rollback()
            return False

if __name__ == "__main__":
    # FOR DEBUGGING ONLY
    scraper_config = ScraperConfig() 
    scraper = Scraper()    

    with open('config.yaml') as f:
        config = yaml.load(f, Loader = yaml.FullLoader)

    #writer = DB_Writer(config, scraper)
    #writer.record_to_database()

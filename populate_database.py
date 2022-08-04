import yaml
import traceback
from scraper import Scraper, ScraperConfig
from helpers import connect_to_db, get_sentiment 
# BASIC TABLE SCHEMA 
# TODO create entry for tags
TABLE_SCHEMA = '''CREATE TABLE %s 
            (id         INT       PRIMARY KEY   NOT NULL,
            topic       TEXT      NOT NULL,
            title       TEXT      NOT NULL,
            subtitle    TEXT      NOT NULL,
            article     TEXT      NOT NULL,
            sentiment   REAL      NOT NULL);''' # % (table_name)

GET_TABLES = '''SELECT table_schema, table_name 
            FROM information_schema.tables
            WHERE (table_schema = 'public')'''

DELETE_TABLE = '''DROP TABLE %s'''

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

class DB_Writer:
    def __init__(self, config, scraper):
        self.config = config
        self.scraper = scraper
        self.delete_table = True 

        # TODO setup connections here
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
            self.cursor.execute(DELETE_TABLE % TABLE_POSITIVE)
            self.cursor.execute(DELETE_TABLE % TABLE_NEGATIVE)
            print("Deleted exsiting tables!")

        self.cursor.execute(GET_TABLES)
        list_tables = self.cursor.fetchall()
        for table_name in [TABLE_POSITIVE, TABLE_NEGATIVE]:
            if sum(map(int, [table_name == i[1] for i in list_tables])):
                # TODO get databse name
                print(f"database contains table -> {table_name}")
            else:
                print(f"table -> {table_name} not found. new table created!")
                self.cursor.execute(TABLE_SCHEMA % (table_name))
                self.connector.commit()

    def record_to_database(self):
        # check if connection is available; then make records here 
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
                    record_item["topic"],
                    record_item["title"],
                    record_item["subtitle"],
                    record_item["article"],
                    item_sentiment)
                    # possibly record metadata also
            
            store_sucess = self.store_item(table, item_data)
            items_stored[table] += int(store_sucess)
            total_items_stored = sum(list(items_stored.values()))
            if total_items_stored%5 == 0:
                print(f"Total items stored into the database: {total_items_stored}")

        print(f"Total items stored: {items_stored}")

    def store_item(self, table_name, item_data):
        # TODO Create decorater for debugging easily
        INSERT_ITEM = f'''INSERT INTO {table_name} VALUES (%s, %s, %s, %s, %s, %s) '''
        try:
            self.cursor.execute(INSERT_ITEM, item_data)
            self.connector.commit()
            return True
        except Exception as e: 
            # TODO add more detail 
            traceback.print_exc()
            self.connector.rollback()
            return False

if __name__ == "__main__":
    scraper_config = ScraperConfig() 
    scraper = Scraper()    

    with open('config.yaml') as f:
        config = yaml.load(f, Loader = yaml.FullLoader)

    #reader = DB_Reader(config)
    #data = reader.read_from_table()
    writer = DB_Writer(config, scraper)
    writer.record_to_database()
    breakpoint()

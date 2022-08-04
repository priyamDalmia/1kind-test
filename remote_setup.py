import yaml
import psycopg2

def connect_to_db(config):
    try:
        connect = psycopg2.connect(
                user=config["user"], 
                password=config["password"], 
                host=config["hostname"], 
                database=config["database"])
        print("Successful connection!")
    except Exception as e:
        print("Connection could not be established")
        print(e)
    cursor = connect.cursor()
    return connect, cursor 

if __name__ == "__main__":
    # FOR DEBUGGING ONLY
    with open('config.yaml') as f:
        config_data = yaml.load(f, Loader = yaml.FullLoader)
    connect, cursor = connect_to_db(config_data["postgres"])


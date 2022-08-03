import yaml
import psycopg2

def connect_to_db(config):
    try:
        connection = psycopg2.connect(
                user=config["user"], 
                password=config["password"], 
                host=config["hostname"], 
                database=config["database"])
        print("Successfull connection!")
    except Exception as e:
        print("Connection could not be established")
        print(e)

    breakpoint()



if __name__ == "__main__":
    
    with open('config.yaml') as f:
        data = yaml.load(f, Loader = yaml.FullLoader)
        config = data["postgres"]

    test_remote_connection(config)


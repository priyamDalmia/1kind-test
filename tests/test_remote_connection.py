import psycopg2
import yaml

def test_remote_connection(config):
    try:
        connection = psycopg2.connect(
                user=config["user"], 
                password=config["password"], 
                host=config["hostname"], 
                database=config["database"])
        print("CONNECTED!")
    except Exception as e:
        print(f"Connection could not be established: {e}")

if __name__ == "__main__":
    
    with open('config.yaml') as f:
        data = yaml.load(f, Loader = yaml.FullLoader)
    
    test_remote_connection(data["postgres"])


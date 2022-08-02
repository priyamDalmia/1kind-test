import psycopg2
import os
import json


def test_local_connection():
    try:
        connection = psycopg2.connect(user="postgres", password="mypassword", host="localhost", database="postgres")
        print("Successfull connection")
    except Exception as e:
        print("Connection could not be established")
        print(e)



if __name__ == "__main__":
    test_local_connection()


import psycopg2
from config import load_config


def connect():
    config = load_config()
    try:
        with psycopg2.connect(
            dbname=config["dbname"],
            user=config["user"],
            password=config["password"],
            host=config["host"],
            port=config["port"],
        ) as conn:
            print("Connected to the PostgreSQL server.")
            # You can use conn here, e.g., to execute queries
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


if __name__ == "__main__":
    connect()

import os
from dotenv import load_dotenv

load_dotenv()


def load_config():
    config = {
        "dbname": os.getenv("POSTGRES_DB", "fitapp"),
        "user": os.getenv("POSTGRES_USER", "postgres"),
        "password": os.getenv("POSTGRES_PASSWORD", "<PASSWORD>"),
        "host": os.getenv("POSTGRES_HOST", "db"),
        "port": os.getenv("POSTGRES_PORT", "5432"),
    }
    return config


if __name__ == "__main__":
    config = load_config()
    print(config)

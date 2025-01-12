import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Exercise
from config import load_config

config = load_config()
DATABASE_URL = f"postgresql+psycopg2://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['dbname']}"
engine = create_engine(DATABASE_URL, echo=True)
Exercise.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

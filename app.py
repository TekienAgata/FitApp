from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import Exercise
from os import environ


app = Flask(__name__)
DATABASE_URL = f"postgresql+psycopg2://{environ.get('POSTGRES_USER')}:{environ.get('POSTGRES_PASSWORD')}@{environ.get('POSTGRES_HOST')}:{environ.get('POSTGRES_PORT')}/{environ.get('POSTGRES_DB')}"
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
dbapp = SQLAlchemy(app)
with app.app_context():
    dbapp.create_all()


@app.route("/")
def hello_world():
    return "Hello World!"


"""@app.route("/exercises")
def get_exercises():
    session.close()
    exercises = session.query(Exercise).all()
    return jsonify(exercises)"""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

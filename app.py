from flask import Flask, jsonify
from db_setup import session
from models import Exercise
import psycopg2
import os


app = Flask(__name__)


@app.route("/")
def hello_world():  # put application's code here
    return "Hello World!"


@app.route("/exercises")
def get_exercises():
    session.close()
    exercises = session.query(Exercise).all()
    return jsonify(exercises)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

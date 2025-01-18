from flask import Flask, jsonify, make_response, request
from models import db, Exercise
from os import environ


app = Flask(__name__)
DATABASE_URL = (
    f"postgresql+psycopg2://{environ.get('POSTGRES_USER')}:"
    f"{environ.get('POSTGRES_PASSWORD')}@{environ.get('POSTGRES_HOST')}:"
    f"{environ.get('POSTGRES_PORT')}/{environ.get('POSTGRES_DB')}"
)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/")
def hello_world():
    return "Hello World!"


@app.route("/exercises", methods=["GET"])
def get_exercises():
    try:
        exercises = Exercise.query.all()
        return make_response(jsonify([exercise.json() for exercise in exercises]), 200)
    except Exception as e:
        return make_response(
            jsonify({"message": "error getting exercises", "error": str(e)}), 500
        )


@app.route("/exercises", methods=["POST"])
def create_exercise():
    try:
        data = request.get_json()
        if not all(field in data for field in ["name", "description", "category"]):
            return make_response(jsonify({"message": "required fields missing"}), 400)
        exercise = Exercise(
            name=data["name"], description=data["description"], category=data["category"]
        )
        db.session.add(exercise)
        db.session.commit()
        return make_response(jsonify({"message": "exercise created successfully"}), 201)
    except Exception as e:
        return make_response(
            jsonify({"message": "error creating exercise", "error": str(e)}), 500
        )


@app.route("/exercises/<int:id>", methods=["PUT", "DELETE"])
def modify_exercise(id):
    try:
        exercise = Exercise.query.get(id)
        if exercise:
            if request.method == "DELETE":
                db.session.delete(exercise)
                db.session.commit()
                return make_response(
                    jsonify({"message": f"exercise {id} deleted"}), 200
                )
            if request.method == "PUT":
                data = request.get_json()
                if "name" in data:
                    exercise.name = data["name"]
                if "description" in data:
                    exercise.description = data["description"]
                if "category" in data:
                    exercise.category = data["category"]
                db.session.commit()
                return make_response(
                    jsonify({"message": f"exercise {id} updated"}), 200
                )
        return make_response(jsonify({"message": "exercise not found"}), 404)
    except Exception as e:
        make_response(jsonify({"message": f"error modifying exercise {id}","error":str(e)}), 500)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

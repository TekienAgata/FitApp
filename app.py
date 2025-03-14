from os import environ
from flask import Flask, jsonify, make_response, request
from models import Exercise, User, Workout, WorkoutExercise, db

app = Flask(__name__)
DATABASE_URL = (
    f"postgresql+psycopg2://{environ.get('POSTGRES_USER')}:"
    f"{environ.get('POSTGRES_PASSWORD')}@{environ.get('POSTGRES_HOST')}:"
    f"{environ.get('POSTGRES_PORT')}/{environ.get('POSTGRES_DB')}"
)
print(DATABASE_URL)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def hello_world():
    return "Im here!"


# Exercises' endpoints
@app.route("/exercises", methods=["GET"])
def get_exercises():
    try:
        exercises = Exercise.query.all()
        return make_response(
            jsonify([exercise.make_json() for exercise in exercises]), 200
        )
    except Exception as e:
        return make_response(
            jsonify({"message": "error getting exercises", "error": str(e)}), 500
        )


@app.route("/exercises", methods=["POST"])
def create_exercise():
    try:
        data = request.get_json()
        if not all(field in data for field in ["name", "category"]):
            return make_response(jsonify({"message": "required fields missing"}), 400)
        if data.get("custom_made"):
            if "created_by" not in data:
                return make_response(
                    jsonify({"message": "created_by required for custom exercises"}),
                    400,
                )
            user = User.query.get(data["created_by"])
            if not user:
                return make_response(
                    jsonify({"message": "specified user not found"}), 404
                )
        exercise = Exercise(
            name=data["name"],
            description=data.get("description", ""),
            category=data["category"],
            custom_made=data.get("custom_made", False),
            created_by=data.get("created_by") if data.get("custom_made") else None,
        )
        db.session.add(exercise)
        db.session.commit()
        return make_response(jsonify({"message": "exercise created successfully"}), 201)
    except Exception as e:
        return make_response(
            jsonify({"message": "error creating exercise", "error": str(e)}), 500
        )


@app.route("/exercises/<uuid:id>", methods=["PUT", "DELETE"])
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
                if "custom_made" in data:
                    exercise.custom_made = data["custom_made"]
                db.session.commit()
                return make_response(
                    jsonify({"message": f"exercise {id} updated"}), 200
                )
        return make_response(jsonify({"message": "exercise not found"}), 404)
    except Exception as e:
        return make_response(
            jsonify({"message": f"error modifying exercise {id}", "error": str(e)}), 500
        )


# Users' endpoints
@app.route("/users", methods=["GET"])
def get_users():
    try:
        users = User.query.all()
        return make_response(jsonify([user.make_json() for user in users]), 200)
    except Exception as e:
        return make_response(
            jsonify({"message": "error getting users", "error": str(e)}), 500
        )


@app.route("/users", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        if not all(field in data for field in ["username", "name", "email"]):
            return make_response(jsonify({"message": "required fields missing"}), 400)
        user = User(
            username=data["username"],
            name=data["name"],
            email=data["email"],
        )
        db.session.add(user)
        db.session.commit()
        return make_response(jsonify({"message": "user created successfully"}), 201)
    except Exception as e:
        return make_response(
            jsonify({"message": "error creating user", "error": str(e)}), 500
        )


@app.route("/users/<uuid:id>", methods=["PUT", "DELETE"])
def modify_user(id):
    try:
        user = User.query.get(id)
        if user:
            if request.method == "DELETE":
                db.session.delete(user)
                db.session.commit()
                return make_response(jsonify({"message": f"user {id} deleted"}), 200)
            if request.method == "PUT":
                data = request.get_json()
                if "username" in data:
                    user.username = data["username"]
                if "name" in data:
                    user.name = data["name"]
                if "email" in data:
                    user.email = data["email"]
                db.session.commit()
                return make_response(jsonify({"message": f"user {id} updated"}), 200)
        return make_response(jsonify({"message": "user not found"}), 404)
    except Exception as e:
        return make_response(
            jsonify({"message": f"error modifying user {id}", "error": str(e)}), 500
        )


# Workouts' endpoints
@app.route("/workouts", methods=["GET"])
def get_workouts():
    try:
        workouts = Workout.query.all()
        return make_response(
            jsonify([workout.make_json() for workout in workouts]), 200
        )
    except Exception as e:
        return make_response(
            jsonify({"message": "error getting workouts", "error": str(e)}), 500
        )


@app.route("/workouts", methods=["POST"])
def create_workout():
    try:
        data = request.get_json()
        if "user_workout_id" not in data:
            return make_response(jsonify({"message": "user_workout_id required"}), 400)
        user = User.query.get(data["user_workout_id"])
        if not user:
            return make_response(jsonify({"message": "specified user not found"}), 404)
        workout = Workout(user_workout_id=data["user_workout_id"])
        db.session.add(workout)
        db.session.commit()
        return make_response(
            jsonify(
                {
                    "message": "workout created successfully",
                    "workout": workout.make_json(),
                }
            ),
            201,
        )
    except Exception as e:
        return make_response(
            jsonify({"message": "error creating workout", "error": str(e)}), 500
        )


@app.route("/workouts/<uuid:id>", methods=["GET", "PUT", "DELETE"])
def modify_workout(id):
    try:
        workout = Workout.query.get(id)
        if workout:
            if request.method == "GET":
                return make_response(jsonify(workout.make_json()), 200)
            if request.method == "DELETE":
                db.session.delete(workout)
                db.session.commit()
                return make_response(jsonify({"message": f"workout {id} deleted"}), 200)
            if request.method == "PUT":
                data = request.get_json()
                db.session.commit()
                return make_response(jsonify({"message": f"workout {id} updated"}), 200)
        return make_response(jsonify({"message": "workout not found"}), 404)
    except Exception as e:
        return make_response(
            jsonify({"message": f"error modifying workout {id}", "error": str(e)}), 500
        )


@app.route("/workouts_exercises", methods=["POST"])
def add_exercise_to_workout():
    try:
        data = request.get_json()
        if not all(field in data for field in ["workout_id", "exercise_id", "sets"]):
            return make_response(jsonify({"message": "required fields missing"}), 400)
        workout = Workout.query.get(data["workout_id"])
        if not workout:
            return make_response(
                jsonify({"message": "specified workout not found"}), 404
            )

        exercise = Exercise.query.get(data["exercise_id"])
        if not exercise:
            return make_response(
                jsonify({"message": "specified exercise not found"}), 404
            )
        workout_exercise = WorkoutExercise(
            workout_id=data["workout_id"],
            exercise_id=data["exercise_id"],
            sets=data["sets"],
            repetitions=data.get("repetitions"),
            weights=data.get("weights"),
            duration=data.get("duration"),
        )
        db.session.add(workout_exercise)
        db.session.commit()
        return make_response(
            jsonify(
                {
                    "message": "exercise added to workout",
                    "workout_exercise": workout_exercise.make_json(),
                }
            ),
            201,
        )
    except Exception as e:
        return make_response(
            jsonify({"message": "error adding exercise to workout", "error": str(e)}),
            500,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

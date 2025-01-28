from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

workout_exercise = db.Table(
    "workout_exercise",
    db.Column("workout_id", db.Integer, db.ForeignKey("workouts.id"), primary_key=True),
    db.Column("exercise.id", db.Integer, db.ForeignKey("exercises.id"), primary_key=True),
)


class Exercise(db.Model):
    __tablename__ = "exercises"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100), nullable=False)
    # workouts = db.relationship("Workout", backref="exercise")

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description or "No description available",
            "category": self.category,
        }


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    workouts = db.relationship("Workout", backref="user")

    def json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "name": self.name,
        }


class Workout(db.Model):
    __tablename__ = "workouts"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    user_workout_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    comments = db.Column(db.Text)

    exercises = db.relationship(
        "Exercise", secondary=workout_exercise, backref="workouts"
    )

    def json(self):
        return {
            "id": self.id,
            "date": self.date.isformat(),
            "user": self.user.username,
            "exercises": [exercise.json() for exercise in self.exercises],
            "comments": self.comments or "",
        }


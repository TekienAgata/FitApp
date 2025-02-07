from datetime import datetime
from uuid import uuid4

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID

# Initializing the database's ORM
db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = "exercises"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100), nullable=False)
    custom_made = db.Column(db.Boolean, default=False, nullable=False)
    created_by = db.Column(UUID(as_uuid=True),db.ForeignKey("users.id"), default=None)

    def make_json(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description or "No description available",
            "category": self.category,
        }


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = db.Column(db.String(100), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    workouts = db.relationship("Workout", back_populates="user")

    def make_json(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "email": self.email,
            "name": self.name,
        }


class Workout(db.Model):
    __tablename__ = "workouts"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    user_workout_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False
    )
    user = db.relationship("User", back_populates="workouts")


    def make_json(self):
        return {
            "id": str(self.id),
            "date": self.date.isoformat(),
            "user": self.user.username,
            "exercises": [exercise.json() for exercise in self.exercises],
            "comments": self.comments or "",
        }

class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"
    id = db.Column(UUID(as_uuid=True), primary_key = True, default=uuid4)
    workout_id = db.Column(UUID(as_uuid=True), db.ForeignKey("workouts.id"),nullable=False)
    exercise_id =db.Column(UUID(as_uuid=True),db.ForeignKey("exercises.id"),nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    repetitions = db.Column(db.Integer)
    weights = db.Column(db.Float)
    duration = db.Column(db.Float)

    def make_json(self):
        return
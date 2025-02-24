from datetime import datetime
from uuid import uuid4

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

# Initializing the database's ORM
db = SQLAlchemy()


class Exercise(db.Model):
    """
    Represents an exercise that can be included in a workout.

    Attributes:
        id (UUID): Unique identifier for the exercise.
        name (str): Name of the exercise.
        description (str, optional): Detailed description of the exercise.
        category (str): Category of the exercise (e.g., "Strength", "Cardio").
        custom_made (bool): Indicates if the exercise is custom-created by a user.
        created_by (UUID, optional): References the user who created the custom exercise.

    Relationships:
        creator (User): Links the exercise to the user who created it.
        workouts (WorkoutExercise): Many-to-many relationship with workouts through WorkoutExercise.
    """

    __tablename__ = "exercises"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100), nullable=False)
    custom_made = db.Column(db.Boolean, default=False, nullable=False)
    created_by = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=True)

    # Relationships
    creator = db.relationship("User", back_populates="exercises")
    workouts = db.relationship("WorkoutExercise", back_populates="exercise")

    def make_json(self):
        """Returns a dictionary representation of the exercise."""
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description or "No description available",
            "category": self.category,
            "custom_made": self.custom_made,
            "created_by": self.creator.username if self.creator else None,
        }


class User(db.Model):
    """
    Represents a user in the system.

    Attributes:
        id (UUID): Unique identifier for the user.
        username (str): Unique username of the user.
        name (str): Full name of the user.
        email (str): Unique email address.
        created_at (datetime): Timestamp when the user was created.

    Relationships:
        workouts (Workout): One-to-many relationship with workouts.
        exercises (Exercise): One-to-many relationship with exercises created by the user.
    """

    __tablename__ = "users"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = db.Column(db.String(100), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    workouts = db.relationship("Workout", back_populates="user")
    exercises = db.relationship("Exercise", back_populates="creator")

    def make_json(self):
        """Returns a dictionary representation of the user."""
        return {
            "id": str(self.id),
            "username": self.username,
            "email": self.email,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
        }


class Workout(db.Model):
    """
    Represents a workout session performed by a user.

    Attributes:
        id (UUID): Unique identifier for the workout.
        created_at (datetime): Timestamp when the workout was created.
        user_workout_id (UUID): Foreign key referencing the user who performed the workout.

    Relationships:
        user (User): Links the workout to the user who performed it.
        workout_exercises (WorkoutExercise): Many-to-many relationship with exercises through WorkoutExercise.
    """

    __tablename__ = "workouts"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_workout_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False
    )

    # Relationships
    user = db.relationship("User", back_populates="workouts")
    workout_exercises = db.relationship("WorkoutExercise", back_populates="workout")

    def make_json(self):
        """Returns a dictionary representation of the workout."""
        return {
            "id": str(self.id),
            "created_at": self.created_at.isoformat(),
            "user": self.user.username,
            "exercises": [we.make_json() for we in self.workout_exercises],
        }


class WorkoutExercise(db.Model):
    """
    Represents the association between workouts and exercises.

    This is a junction table implementing a many-to-many relationship between
    Workout and Exercise, allowing additional attributes such as sets, repetitions, weights, and duration.

    Attributes:
        id (UUID): Unique identifier for the relationship.
        workout_id (UUID): Foreign key referencing the workout.
        exercise_id (UUID): Foreign key referencing the exercise.
        sets (int): Number of sets for this exercise in the workout.
        repetitions (int, optional): Number of repetitions per set.
        weights (float, optional): Weight used in the exercise (if applicable).
        duration (float, optional): Duration of the exercise in minutes.

    Relationships:
        workout (Workout): Links the record to the associated workout.
        exercise (Exercise): Links the record to the associated exercise.
    """

    __tablename__ = "workout_exercises"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    workout_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("workouts.id"), nullable=False
    )
    exercise_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("exercises.id"), nullable=False
    )
    sets = db.Column(db.Integer, nullable=False)
    repetitions = db.Column(db.Integer)
    weights = db.Column(db.Float)
    duration = db.Column(db.Float)

    # Relationships
    workout = db.relationship("Workout", back_populates="workout_exercises")  # FIXED
    exercise = db.relationship("Exercise", back_populates="workouts")

    def make_json(self):
        """Returns a dictionary representation of the workout-exercise association."""
        return {
            "id": str(self.id),
            "workout_id": str(self.workout_id),
            "exercise_id": str(self.exercise_id),
            "sets": self.sets,
            "repetitions": self.repetitions,
            "weights": self.weights,
            "duration": self.duration,
        }

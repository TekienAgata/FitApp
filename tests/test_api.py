def test_hello_world(client):
    """Test the hello world endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.data.decode("utf-8") == "Hello World!"


def test_create_user(client):
    """Test user creation"""
    test_user = {
        "username": "testuser",
        "name": "Test User",
        "email": "test@example.com",
    }
    response = client.post("/users", json=test_user)
    assert response.status_code == 201
    assert response.json["message"] == "user created successfully"

    # Verify user was created
    response = client.get("/users")
    assert response.status_code == 200
    users = response.json
    assert len(users) == 1
    assert users[0]["username"] == test_user["username"]
    assert users[0]["email"] == test_user["email"]


def test_create_exercise(client):
    """Test exercise creation"""
    test_exercise = {
        "name": "Push-ups",
        "category": "Strength",
        "description": "Basic push-ups",
    }
    response = client.post("/exercises", json=test_exercise)
    assert response.status_code == 201
    assert response.json["message"] == "exercise created successfully"

    # Verify exercise was created
    response = client.get("/exercises")
    assert response.status_code == 200
    exercises = response.json
    assert len(exercises) == 1
    assert exercises[0]["name"] == test_exercise["name"]
    assert exercises[0]["category"] == test_exercise["category"]


def test_create_workout_with_exercise(client):
    """Test creating a workout and adding an exercise to it"""
    # First create a user
    test_user = {
        "username": "testuser",
        "name": "Test User",
        "email": "test@example.com",
    }
    response = client.post("/users", json=test_user)
    assert response.status_code == 201

    # Get the user to get their ID
    response = client.get("/users")
    user_id = response.json[0]["id"]

    # Create a workout
    response = client.post("/workouts", json={"user_workout_id": user_id})
    assert response.status_code == 201
    workout_id = response.json["workout"]["id"]

    # Create an exercise
    test_exercise = {"name": "Push-ups", "category": "Strength"}
    response = client.post("/exercises", json=test_exercise)
    assert response.status_code == 201

    # Get the exercise ID
    response = client.get("/exercises")
    exercise_id = response.json[0]["id"]

    # Add exercise to workout
    workout_exercise = {
        "workout_id": workout_id,
        "exercise_id": exercise_id,
        "sets": 3,
        "repetitions": 10,
    }
    response = client.post("/workouts_exercises", json=workout_exercise)
    assert response.status_code == 201
    assert response.json["message"] == "exercise added to workout"

    # Verify workout has the exercise
    response = client.get(f"/workouts/{workout_id}")
    assert response.status_code == 200
    assert len(response.json["exercises"]) == 1
    assert response.json["exercises"][0]["sets"] == 3
    assert response.json["exercises"][0]["repetitions"] == 10


def test_invalid_user_creation(client):
    """Test user creation with missing required fields"""
    invalid_user = {"username": "testuser"}  # Missing required fields
    response = client.post("/users", json=invalid_user)
    assert response.status_code == 400
    assert response.json["message"] == "required fields missing"


def test_custom_exercise_creation(client):
    """Test creating a custom exercise with user association"""
    # First create a user
    test_user = {
        "username": "testuser",
        "name": "Test User",
        "email": "test@example.com",
    }
    response = client.post("/users", json=test_user)
    assert response.status_code == 201

    # Get the user ID
    response = client.get("/users")
    user_id = response.json[0]["id"]

    # Create custom exercise
    test_exercise = {
        "name": "Custom Exercise",
        "category": "Custom",
        "custom_made": True,
        "created_by": user_id,
    }
    response = client.post("/exercises", json=test_exercise)
    assert response.status_code == 201

    # Verify exercise was created with correct association
    response = client.get("/exercises")
    assert response.status_code == 200
    exercises = response.json
    assert len(exercises) == 1
    assert exercises[0]["custom_made"] == True
    assert exercises[0]["created_by"] == "testuser"

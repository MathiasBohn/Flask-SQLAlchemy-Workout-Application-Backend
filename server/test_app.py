import pytest
from app import app
from models import db, Exercise, Workout, WorkoutExercise
from datetime import date
from sqlalchemy.exc import IntegrityError

@pytest.fixture
def client():
    """Create a test client"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

@pytest.fixture
def sample_data():
    """Create sample data for tests"""
    exercise = Exercise(
        name="Push-ups",
        category="strength",
        equipment_needed=False
    )
    workout = Workout(
        date=date(2025, 10, 20),
        duration_minutes=45,
        notes="Test workout"
    )
    
    db.session.add_all([exercise, workout])
    db.session.commit()
    
    return {'exercise': exercise, 'workout': workout}

# MODEL VALIDATION TESTS

def test_exercise_name_validation(client):
    """Test that exercise name must be at least 3 characters (database constraint)"""
    with app.app_context():
        with pytest.raises(IntegrityError):  # Changed from ValueError to IntegrityError
            exercise = Exercise(name="ab", category="strength", equipment_needed=False)
            db.session.add(exercise)
            db.session.commit()

def test_workout_duration_validation(client):
    """Test that workout duration must be positive"""
    with app.app_context():
        with pytest.raises((ValueError, IntegrityError)):  # Accept either error
            workout = Workout(date=date.today(), duration_minutes=0, notes="test")
            db.session.add(workout)
            db.session.commit()

def test_exercise_category_validation(client):
    """Test that exercise category cannot be empty"""
    with app.app_context():
        with pytest.raises(ValueError):
            exercise = Exercise(name="Test", category="", equipment_needed=False)
            db.session.add(exercise)
            db.session.commit()

# ENDPOINT STATUS CODE TESTS

def test_get_workouts_success(client, sample_data):
    """Test GET /workouts returns 200"""
    response = client.get('/workouts')
    assert response.status_code == 200

def test_get_exercises_success(client, sample_data):
    """Test GET /exercises returns 200"""
    response = client.get('/exercises')
    assert response.status_code == 200

def test_get_workout_by_id_success(client, sample_data):
    """Test GET /workouts/<id> returns 200 for existing workout"""
    response = client.get('/workouts/1')
    assert response.status_code == 200

def test_get_workout_by_id_not_found(client):
    """Test GET /workouts/<id> returns 404 for non-existent workout"""
    response = client.get('/workouts/999')
    assert response.status_code == 404

def test_post_workout_success(client):
    """Test POST /workouts returns 201 with valid data"""
    response = client.post('/workouts', json={
        'date': '2025-10-26',
        'duration_minutes': 60,
        'notes': 'New workout'
    })
    assert response.status_code == 201

def test_post_workout_invalid_data(client):
    """Test POST /workouts returns 400 with invalid data"""
    response = client.post('/workouts', json={
        'date': '2025-10-26',
        'duration_minutes': -5  # Invalid: negative duration
    })
    assert response.status_code == 400

def test_post_exercise_success(client):
    """Test POST /exercises returns 201 with valid data"""
    response = client.post('/exercises', json={
        'name': 'Squats',
        'category': 'strength',
        'equipment_needed': False
    })
    assert response.status_code == 201

def test_post_exercise_invalid_data(client):
    """Test POST /exercises returns 400 with invalid data"""
    response = client.post('/exercises', json={
        'name': 'ab',
        'category': 'strength',
        'equipment_needed': False
    })
    assert response.status_code == 400

def test_delete_workout_success(client, sample_data):
    """Test DELETE /workouts/<id> returns 200"""
    response = client.delete('/workouts/1')
    assert response.status_code == 200


def test_delete_workout_not_found(client):
    """Test DELETE /workouts/<id> returns 404 for non-existent workout"""
    response = client.delete('/workouts/999')
    assert response.status_code == 404

def test_delete_exercise_success(client, sample_data):
    """Test DELETE /exercises/<id> returns 200"""
    response = client.delete('/exercises/1')
    assert response.status_code == 200

def test_post_workout_exercise_success(client, sample_data):
    """Test POST /workouts/<id>/exercises/<id>/workout_exercises returns 201"""
    response = client.post('/workouts/1/exercises/1/workout_exercises', json={
        'sets': 3,
        'reps': 12
    })
    assert response.status_code == 201

def test_post_workout_exercise_not_found(client):
    """Test POST returns 404 when workout or exercise doesn't exist"""
    response = client.post('/workouts/999/exercises/999/workout_exercises', json={
        'sets': 3,
        'reps': 12
    })
    assert response.status_code == 404
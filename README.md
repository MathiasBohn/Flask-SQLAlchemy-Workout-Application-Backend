# The VERY BEST Flask SQLAlchemy Workout Application Backend

## Project Description

A SUPER DUPER AND VERY FUCKING AWESOME robust REST API backend for a workout tracking application built with Flask, SQLAlchemy, and Marshmallow. This API enables personal trainers to manage workouts and exercises, track workout sessions, and associate exercises with workouts including detailed information like sets, reps, and duration.

The application demonstrates professional backend development practices - mom, look at how far I've come! - including:
- RESTful API design
- Multi-layered data validation (database constraints, model validations, and schema validations)
- Complex many-to-many relationships with additional data
- Comprehensive error handling
- Full test coverage

## THE BEST features

- **Exercise Management**: Create, view, and delete reusable exercises
- **Workout Management**: Create, view, and delete workout sessions
- **Exercise-Workout Association**: Add exercises to workouts with specific sets, reps, and duration
- **Data Validation**: Three layers of validation ensure data integrity
- **Cascade Deletes**: Deleting workouts or exercises automatically removes associated records
- **Comprehensive Testing**: Full test suite for validations and endpoints

## Honestly, the most superior tech stack

- **Flask 2.2.2** - Web framework
- **SQLAlchemy 3.0.3** - ORM for database operations
- **Flask-Migrate 3.1.0** - Database migrations
- **Marshmallow 3.20.1** - Object serialization/deserialization and validation
- **SQLite** - Database (development)
- **pytest 8.4.2** - Testing framework

## Installation Instructions (if you really want to do this)

### Prerequisites
- Python 3.13.7
- pipenv 2025.0.4

### Setup Steps

1. **Clone the repository**
```bash
   git clone <your-repo-url>
   cd Flask-SQLAlchemy-Workout-Application-Backend
```

2. **Install dependencies**
```bash
   pipenv install
```
   
   This will install all dependencies from the Pipfile:
   - Flask 2.2.2
   - Flask-Migrate 3.1.0
   - Flask-SQLAlchemy 3.0.3
   - Werkzeug 2.2.2
   - importlib-metadata 6.0.0
   - importlib-resources 5.10.0
   - ipdb 0.13.9
   - marshmallow 3.20.1
   
   And dev dependencies:
   - pytest (for testing)

3. **Activate the virtual environment**
```bash
   pipenv shell
```

4. **Initialize the database**
```bash
   cd server
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
```

5. **Seed the database with sample data**
```bash
   python seed.py
```

## Dependencies (Pipfile)

### Production Dependencies
```
Flask = "2.2.2"
Flask-Migrate = "3.1.0"
Flask-SQLAlchemy = "3.0.3"
Werkzeug = "2.2.2"
importlib-metadata = "6.0.0"
importlib-resources = "5.10.0"
ipdb = "0.13.9"
marshmallow = "3.20.1"
```

### Development Dependencies
```
pytest = "*"
```

## Run Instructions

### Start the Flask Development Server
```bash
cd server
python app.py
```

The API will be available at `http://localhost:5555`

### Run Tests
```bash
pytest server/test_app.py -v
```

Or from the project root:
```bash
pytest -v
```

### Access Flask Shell
```bash
flask shell
```

## API Endpoints

### Workout Endpoints

#### `GET /workouts`
**Description**: Retrieve a list of all workouts

**Response**: `200 OK`
```json
[
  {
    "id": 1,
    "date": "2025-10-20",
    "duration_minutes": 45,
    "notes": "Morning workout session"
  }
]
```

---

#### `GET /workouts/<id>`
**Description**: Retrieve a single workout with its associated exercises and workout details (sets, reps, duration)

**Response**: `200 OK`
```json
{
  "id": 1,
  "date": "2025-10-20",
  "duration_minutes": 45,
  "notes": "Morning workout session",
  "workout_exercises": [
    {
      "id": 1,
      "exercise": {
        "id": 1,
        "name": "Push-ups",
        "category": "strength",
        "equipment_needed": false
      },
      "sets": 3,
      "reps": 15,
      "duration_seconds": null
    }
  ]
}
```

**Error Response**: `404 Not Found` if workout doesn't exist

---

#### `POST /workouts`
**Description**: Create a new workout

**Request Body**:
```json
{
  "date": "2025-10-26",
  "duration_minutes": 60,
  "notes": "Evening training"
}
```

**Response**: `201 Created`
```json
{
  "id": 4,
  "date": "2025-10-26",
  "duration_minutes": 60,
  "notes": "Evening training"
}
```

**Validations**:
- `date` is required (cannot be in the future)
- `duration_minutes` is required (must be > 0)
- `notes` is optional

**Error Response**: `400 Bad Request` if validation fails

---

#### `DELETE /workouts/<id>`
**Description**: Delete a workout (also deletes associated workout-exercise records)

**Response**: `200 OK`
```json
{
  "message": "Workout deleted successfully"
}
```

**Error Response**: `404 Not Found` if workout doesn't exist

---

### Exercise Endpoints

#### `GET /exercises`
**Description**: Retrieve a list of all exercises

**Response**: `200 OK`
```json
[
  {
    "id": 1,
    "name": "Push-ups",
    "category": "strength",
    "equipment_needed": false
  }
]
```

---

#### `GET /exercises/<id>`
**Description**: Retrieve a single exercise with its associated workouts

**Response**: `200 OK`
```json
{
  "id": 1,
  "name": "Push-ups",
  "category": "strength",
  "equipment_needed": false,
  "workouts": [
    {
      "id": 1,
      "date": "2025-10-20",
      "duration_minutes": 45,
      "notes": "Morning workout session"
    }
  ]
}
```

**Error Response**: `404 Not Found` if exercise doesn't exist

---

#### `POST /exercises`
**Description**: Create a new exercise

**Request Body**:
```json
{
  "name": "Burpees",
  "category": "cardio",
  "equipment_needed": false
}
```

**Response**: `201 Created`
```json
{
  "id": 6,
  "name": "Burpees",
  "category": "cardio",
  "equipment_needed": false
}
```

**Validations**:
- `name` is required (must be at least 3 characters, must be unique)
- `category` is required (cannot be empty)
- `equipment_needed` is required (boolean)

**Error Response**: `400 Bad Request` if validation fails

---

#### `DELETE /exercises/<id>`
**Description**: Delete an exercise (also deletes associated workout-exercise records)

**Response**: `200 OK`
```json
{
  "message": "Exercise deleted successfully"
}
```

**Error Response**: `404 Not Found` if exercise doesn't exist

---

### Workout-Exercise Association Endpoint

#### `POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises`
**Description**: Add an exercise to a workout with specific sets, reps, or duration

**Request Body**:
```json
{
  "sets": 4,
  "reps": 12,
  "duration_seconds": null
}
```

**Response**: `201 Created`
```json
{
  "id": 6,
  "workout_id": 1,
  "exercise_id": 2,
  "sets": 4,
  "reps": 12,
  "duration_seconds": null
}
```

**Validations**:
- `workout_id` must exist
- `exercise_id` must exist
- `sets`, `reps`, and `duration_seconds` are optional but must be positive if provided

**Error Responses**:
- `404 Not Found` if workout or exercise doesn't exist
- `400 Bad Request` if validation fails

---

## Database Schema

### Exercise
- `id` (Primary Key)
- `name` (String, Unique, Min 3 characters)
- `category` (String, Not Null)
- `equipment_needed` (Boolean, Not Null)

### Workout
- `id` (Primary Key)
- `date` (Date, Not Null)
- `duration_minutes` (Integer, Not Null, > 0)
- `notes` (Text, Nullable)

### WorkoutExercise (Join Table)
- `id` (Primary Key)
- `workout_id` (Foreign Key → Workout)
- `exercise_id` (Foreign Key → Exercise)
- `reps` (Integer, Nullable, > 0 if provided)
- `sets` (Integer, Nullable, > 0 if provided)
- `duration_seconds` (Integer, Nullable, > 0 if provided)

## Validation Layers

The application implements three layers of validation:

1. **Database Constraints** (Table-level)
   - NOT NULL constraints
   - UNIQUE constraints
   - CHECK constraints (e.g., `length(name) >= 3`, `duration_minutes > 0`)

2. **Model Validations** (SQLAlchemy-level)
   - Custom `@validates` decorators
   - Business logic validation
   - Examples:
     - Exercise name validation (min 3 characters)
     - Exercise category validation (not empty)
     - Workout duration validation (must be positive)

3. **Schema Validations** (API-level)
   - Marshmallow field validators
   - Request/response validation
   - Examples:
     - `validate.Length(min=3)` on exercise name
     - `@validates` custom methods in schemas
     - Required field enforcement

## Testing

### Test Suite Overview

The test suite (`server/test_app.py`) includes 16 tests covering:

#### Model Validation Tests (3)
1. **test_exercise_name_validation** - Verifies exercise name must be at least 3 characters (database constraint)
2. **test_workout_duration_validation** - Verifies workout duration must be positive
3. **test_exercise_category_validation** - Verifies exercise category cannot be empty

#### Endpoint Status Code Tests (13)
1. **test_get_workouts_success** - GET /workouts returns 200
2. **test_get_exercises_success** - GET /exercises returns 200
3. **test_get_workout_by_id_success** - GET /workouts/<id> returns 200
4. **test_get_workout_by_id_not_found** - GET /workouts/<id> returns 404
5. **test_post_workout_success** - POST /workouts returns 201 with valid data
6. **test_post_workout_invalid_data** - POST /workouts returns 400 with invalid data
7. **test_post_exercise_success** - POST /exercises returns 201 with valid data
8. **test_post_exercise_invalid_data** - POST /exercises returns 400 with invalid data
9. **test_delete_workout_success** - DELETE /workouts/<id> returns 200
10. **test_delete_workout_not_found** - DELETE /workouts/<id> returns 404
11. **test_delete_exercise_success** - DELETE /exercises/<id> returns 200
12. **test_post_workout_exercise_success** - POST workout_exercises returns 201
13. **test_post_workout_exercise_not_found** - POST workout_exercises returns 404

### Running Tests
```bash
# Run all tests with verbose output
pytest server/test_app.py -v

# Run tests from project root
pytest -v

# Run specific test
pytest server/test_app.py::test_get_workouts_success -v

# Run with coverage (if pytest-cov is installed)
pytest --cov=server server/test_app.py
```

### Test Fixtures

- **client** - Creates a test Flask client with a separate test database
- **sample_data** - Seeds test database with sample Exercise and Workout records

## Project Structure
```
Flask-SQLAlchemy-Workout-Application-Backend/
├── server/
│   ├── app.py              # Main application and routes
│   ├── models.py           # Database models with validations
│   ├── schemas.py          # Marshmallow schemas for serialization
│   ├── seed.py             # Database seeding script
│   ├── test_app.py         # Test suite (16 tests)
│   ├── instance/
│   │   └── app.db          # SQLite database (created after setup)
│   └── migrations/         # Database migrations (created after flask db init)
├── Pipfile                 # Project dependencies
├── Pipfile.lock            # Locked dependency versions
├── requirements.txt        # Dependency list for pip
└── README.md               # This file
```

## File Descriptions

### Core Application Files

- **app.py** - Main Flask application with all API endpoints, error handling, and routing
- **models.py** - SQLAlchemy models (Exercise, Workout, WorkoutExercise) with relationships, table constraints, and model validations
- **schemas.py** - Marshmallow schemas for serialization/deserialization and schema-level validation
- **seed.py** - Script to populate database with sample data for development and testing

### Test Files

- **test_app.py** - Comprehensive test suite using pytest
  - Tests model validations
  - Tests all endpoint status codes
  - Tests CRUD operations
  - Tests error handling
  - Uses fixtures for test data and client setup

### Configuration Files

- **Pipfile** - Defines project dependencies managed by pipenv
- **Pipfile.lock** - Locked versions of all dependencies and sub-dependencies
- **requirements.txt** - Traditional pip requirements file (optional, generated from Pipfile)

## Author

Built as a demonstration of professional Flask backend development practices.

## License

This project is available for educational purposes.
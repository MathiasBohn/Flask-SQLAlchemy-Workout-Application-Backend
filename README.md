# Flask SQLAlchemy Workout Application Backend

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
- **pytest** - Testing framework

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
   - CHECK constraints

2. **Model Validations** (SQLAlchemy-level)
   - Custom `@validates` decorators
   - Business logic validation

3. **Schema Validations** (API-level)
   - Marshmallow field validators
   - Request/response validation

## Project Structure
```
Flask-SQLAlchemy-Workout-Application-Backend/
├── server/
│   ├── app.py              # Main application and routes
│   ├── models.py           # Database models
│   ├── schemas.py          # Marshmallow schemas
│   ├── seed.py             # Database seeding script
│   ├── test_app.py         # Test suite
│   ├── instance/
│   │   └── app.db          # SQLite database
│   └── migrations/         # Database migrations
├── Pipfile                 # Dependencies
├── Pipfile.lock
└── README.md
```

## Testing

Run the test suite to verify all functionality:
```bash
pytest server/test_app.py -v
```

Tests cover:
- Model validations
- Endpoint status codes
- CRUD operations
- Error handling

## Author

Built as a demonstration of professional Flask backend development practices.

## License

This project is available for educational purposes.
from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from marshmallow import ValidationError

from models import db, Exercise, Workout, WorkoutExercise
from schemas import (
    exercise_schema, exercises_schema,
    workout_schema, workouts_schema,
    workout_exercise_schema
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# WORKOUT ENDPOINTS

@app.route('/workouts', methods=['GET'])
def get_workouts():
    """GET /workouts - List all workouts"""
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout_by_id(id):
    """GET /workouts/<id> - Show a single workout with its associated exercises"""
    workout = Workout.query.get(id)
    
    if not workout:
        return jsonify({"error": "Workout not found"}), 404
    
    # Serialize workout with nested exercises and workout_exercises
    result = workout_schema.dump(workout)
    
    # Include workout_exercises details
    result['workout_exercises'] = [
        {
            'id': we.id,
            'exercise': exercise_schema.dump(we.exercise),
            'reps': we.reps,
            'sets': we.sets,
            'duration_seconds': we.duration_seconds
        }
        for we in workout.workout_exercises
    ]
    
    return jsonify(result), 200


@app.route('/workouts', methods=['POST'])
def create_workout():
    """POST /workouts - Create a workout"""
    try:
        # Deserialize and validate request data
        data = workout_schema.load(request.get_json())
        
        # Create new workout
        new_workout = Workout(
            date=data['date'],
            duration_minutes=data['duration_minutes'],
            notes=data.get('notes')
        )
        
        db.session.add(new_workout)
        db.session.commit()
        
        return jsonify(workout_schema.dump(new_workout)), 201
    
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    """DELETE /workouts/<id> - Delete a workout"""
    workout = Workout.query.get(id)
    
    if not workout:
        return jsonify({"error": "Workout not found"}), 404
    
    # Cascade delete will automatically delete associated WorkoutExercises
    db.session.delete(workout)
    db.session.commit()
    
    return jsonify({"message": "Workout deleted successfully"}), 200


# EXERCISE ENDPOINTS

@app.route('/exercises', methods=['GET'])
def get_exercises():
    """GET /exercises - List all exercises"""
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise_by_id(id):
    """GET /exercises/<id> - Show an exercise and associated workouts"""
    exercise = Exercise.query.get(id)
    
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404
    
    # Serialize exercise with nested workouts
    result = exercise_schema.dump(exercise)
    
    # Include associated workouts
    result['workouts'] = [workout_schema.dump(workout) for workout in exercise.workouts]
    
    return jsonify(result), 200


@app.route('/exercises', methods=['POST'])
def create_exercise():
    """POST /exercises - Create an exercise"""
    try:
        # Deserialize and validate request data
        data = exercise_schema.load(request.get_json())
        
        # Create new exercise
        new_exercise = Exercise(
            name=data['name'],
            category=data['category'],
            equipment_needed=data['equipment_needed']
        )
        
        db.session.add(new_exercise)
        db.session.commit()
        
        return jsonify(exercise_schema.dump(new_exercise)), 201
    
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    """DELETE /exercises/<id> - Delete an exercise"""
    exercise = Exercise.query.get(id)
    
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404
    
    # Cascade delete will automatically delete associated WorkoutExercises
    db.session.delete(exercise)
    db.session.commit()
    
    return jsonify({"message": "Exercise deleted successfully"}), 200


# WORKOUT-EXERCISE ENDPOINT

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    """POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises
    Add an exercise to a workout, including reps/sets/duration"""
    try:
        # Check if workout exists
        workout = Workout.query.get(workout_id)
        if not workout:
            return jsonify({"error": "Workout not found"}), 404
        
        # Check if exercise exists
        exercise = Exercise.query.get(exercise_id)
        if not exercise:
            return jsonify({"error": "Exercise not found"}), 404
        
        # Get request data
        data = request.get_json()
        
        # Create workout-exercise association
        new_workout_exercise = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            reps=data.get('reps'),
            sets=data.get('sets'),
            duration_seconds=data.get('duration_seconds')
        )
        
        db.session.add(new_workout_exercise)
        db.session.commit()
        
        return jsonify(workout_exercise_schema.dump(new_workout_exercise)), 201
    
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(port=5555, debug=True)
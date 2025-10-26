from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate

from models import db, Exercise, Workout, WorkoutExercise

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# WORKOUT ENDPOINTS

@app.route('/workouts', methods=['GET'])
def get_workouts():
    """GET /workouts - List all workouts"""
    # TODO: Add serialization with Marshmallow
    return jsonify({"message": "GET all workouts endpoint"}), 200


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout_by_id(id):
    """GET /workouts/<id> - Show a single workout with its associated exercises"""
    # TODO: Add serialization with Marshmallow
    # Stretch goal: include reps/sets/duration data from WorkoutExercises
    return jsonify({"message": f"GET workout {id} endpoint"}), 200


@app.route('/workouts', methods=['POST'])
def create_workout():
    """POST /workouts - Create a workout"""
    # TODO: Add serialization and validation with Marshmallow
    return jsonify({"message": "POST workout endpoint"}), 201


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    """DELETE /workouts/<id> - Delete a workout"""
    # Stretch goal: delete associated WorkoutExercises (handled by cascade)
    # TODO: Add error handling
    return jsonify({"message": f"DELETE workout {id} endpoint"}), 200


# EXERCISE ENDPOINTS

@app.route('/exercises', methods=['GET'])
def get_exercises():
    """GET /exercises - List all exercises"""
    # TODO: Add serialization with Marshmallow
    return jsonify({"message": "GET all exercises endpoint"}), 200


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise_by_id(id):
    """GET /exercises/<id> - Show an exercise and associated workouts"""
    # TODO: Add serialization with Marshmallow
    return jsonify({"message": f"GET exercise {id} endpoint"}), 200


@app.route('/exercises', methods=['POST'])
def create_exercise():
    """POST /exercises - Create an exercise"""
    # TODO: Add serialization and validation with Marshmallow
    return jsonify({"message": "POST exercise endpoint"}), 201


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    """DELETE /exercises/<id> - Delete an exercise"""
    # Stretch goal: delete associated WorkoutExercises (handled by cascade)
    # TODO: Add error handling
    return jsonify({"message": f"DELETE exercise {id} endpoint"}), 200


# WORKOUT-EXERCISE ENDPOINT

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    """POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises
    Add an exercise to a workout, including reps/sets/duration"""
    # TODO: Add serialization and validation with Marshmallow
    return jsonify({"message": f"POST exercise {exercise_id} to workout {workout_id} endpoint"}), 201


if __name__ == '__main__':
    app.run(port=5555, debug=True)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = 'exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False)
    
    # Relationship to WorkoutExercise
    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')
    
    # Relationship to Workout through WorkoutExercise
    workouts = db.relationship('Workout', secondary='workout_exercises', back_populates='exercises')
    
    def __repr__(self):
        return f'<Exercise {self.id}: {self.name}>'


class Workout(db.Model):
    __tablename__ = 'workouts'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    
    # Relationship to WorkoutExercise
    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')
    
    # Relationship to Exercise through WorkoutExercise
    exercises = db.relationship('Exercise', secondary='workout_exercises', back_populates='workouts')
    
    def __repr__(self):
        return f'<Workout {self.id}: {self.date}>'


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)
    
    # Relationships
    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')
    
    def __repr__(self):
        return f'<WorkoutExercise {self.id}: Workout {self.workout_id}, Exercise {self.exercise_id}>'
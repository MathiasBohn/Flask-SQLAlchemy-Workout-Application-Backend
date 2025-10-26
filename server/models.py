from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint

db = SQLAlchemy()

# Define Models here

class Exercise(db.Model):
    __tablename__ = 'exercises'
    
    # Table Constraint 3: Check constraint on name length
    __table_args__ = (
        CheckConstraint('length(name) >= 3', name='check_exercise_name_length'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)  # Table Constraints 1 & 2: nullable=False & unique=True
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False)
    
    # Relationship to WorkoutExercise
    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')
    
    # Relationship to Workout through WorkoutExercise
    workouts = db.relationship('Workout', secondary='workout_exercises', back_populates='exercises')
    
    # Model Validation 1: Validate name is not empty
    @validates('name')
    def validate_name(self, key, name):
        if not name or not name.strip():
            raise ValueError("Exercise name cannot be empty")
        return name.strip()
    
    # Model Validation 3: Validate category is not empty
    @validates('category')
    def validate_category(self, key, category):
        if not category or not category.strip():
            raise ValueError("Exercise category cannot be empty")
        return category.strip()
    
    def __repr__(self):
        return f'<Exercise {self.id}: {self.name}>'


class Workout(db.Model):
    __tablename__ = 'workouts'
    
    # Table Constraint 4: Check constraint on duration_minutes
    __table_args__ = (
        CheckConstraint('duration_minutes > 0', name='check_duration_positive'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    
    # Relationship to WorkoutExercise
    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')
    
    # Relationship to Exercise through WorkoutExercise
    exercises = db.relationship('Exercise', secondary='workout_exercises', back_populates='workouts')
    
    # Model Validation 2: Validate duration is positive
    @validates('duration_minutes')
    def validate_duration(self, key, duration_minutes):
        if duration_minutes <= 0:
            raise ValueError("Duration must be greater than 0")
        return duration_minutes
    
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
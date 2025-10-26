from marshmallow import Schema, fields, validate, validates, ValidationError

# EXERCISE SCHEMA

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=3))
    category = fields.Str(required=True, validate=validate.Length(min=1))
    equipment_needed = fields.Bool(required=True)
    
    # Nested relationships (optional, for when we want to include related data)
    workouts = fields.List(fields.Nested('WorkoutSchema', exclude=('exercises',)), dump_only=True)
    workout_exercises = fields.List(fields.Nested('WorkoutExerciseSchema', exclude=('exercise',)), dump_only=True)
    
    # Schema Validation 1: Validate name is not empty or whitespace
    @validates('name')
    def validate_name(self, value):
        if not value or not value.strip():
            raise ValidationError("Exercise name cannot be empty or whitespace")
    
    # Schema Validation 2: Validate category is not empty or whitespace
    @validates('category')
    def validate_category(self, value):
        if not value or not value.strip():
            raise ValidationError("Exercise category cannot be empty or whitespace")


# WORKOUT SCHEMA

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1))
    notes = fields.Str(allow_none=True)
    
    # Nested relationships (optional, for when we want to include related data)
    exercises = fields.List(fields.Nested('ExerciseSchema', exclude=('workouts',)), dump_only=True)
    workout_exercises = fields.List(fields.Nested('WorkoutExerciseSchema', exclude=('workout',)), dump_only=True)
    
    # Schema Validation 3: Validate duration is positive
    @validates('duration_minutes')
    def validate_duration(self, value):
        if value <= 0:
            raise ValidationError("Duration must be greater than 0")


# WORKOUT EXERCISE SCHEMA

class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    reps = fields.Int(allow_none=True, validate=validate.Range(min=1))
    sets = fields.Int(allow_none=True, validate=validate.Range(min=1))
    duration_seconds = fields.Int(allow_none=True, validate=validate.Range(min=1))
    
    # Nested relationships
    workout = fields.Nested('WorkoutSchema', exclude=('workout_exercises', 'exercises'), dump_only=True)
    exercise = fields.Nested('ExerciseSchema', exclude=('workout_exercises', 'workouts'), dump_only=True)


# SCHEMA INSTANCES

# Single object schemas
exercise_schema = ExerciseSchema()
workout_schema = WorkoutSchema()
workout_exercise_schema = WorkoutExerciseSchema()

# Multiple objects schemas
exercises_schema = ExerciseSchema(many=True)
workouts_schema = WorkoutSchema(many=True)
workout_exercises_schema = WorkoutExerciseSchema(many=True)

# Special schema for detailed workout view (includes workout_exercises with full details)
workout_detail_schema = WorkoutSchema()

# Special schema for detailed exercise view (includes workout_exercises with full details)
exercise_detail_schema = ExerciseSchema()
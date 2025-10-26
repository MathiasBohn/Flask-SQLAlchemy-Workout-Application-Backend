from app import app
from models import db, Exercise, Workout, WorkoutExercise
from datetime import date

with app.app_context():
    
    # reset data and add new example data, committing to db
    print("Clearing existing data...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()
    
    print("Creating exercises...")
    # Create some exercises
    exercise1 = Exercise(
        name="Push-ups",
        category="strength",
        equipment_needed=False
    )
    
    exercise2 = Exercise(
        name="Running",
        category="cardio",
        equipment_needed=False
    )
    
    exercise3 = Exercise(
        name="Bench Press",
        category="strength",
        equipment_needed=True
    )
    
    exercise4 = Exercise(
        name="Squats",
        category="strength",
        equipment_needed=False
    )
    
    exercise5 = Exercise(
        name="Yoga",
        category="flexibility",
        equipment_needed=False
    )
    
    db.session.add_all([exercise1, exercise2, exercise3, exercise4, exercise5])
    db.session.commit()
    print(f"Created {Exercise.query.count()} exercises")
    
    print("Creating workouts...")
    # Create some workouts
    workout1 = Workout(
        date=date(2025, 10, 20),
        duration_minutes=45,
        notes="Morning workout session"
    )
    
    workout2 = Workout(
        date=date(2025, 10, 22),
        duration_minutes=60,
        notes="Evening strength training"
    )
    
    workout3 = Workout(
        date=date(2025, 10, 24),
        duration_minutes=30,
        notes="Quick cardio session"
    )
    
    db.session.add_all([workout1, workout2, workout3])
    db.session.commit()
    print(f"Created {Workout.query.count()} workouts")
    
    print("Creating workout-exercise associations...")
    # Create workout-exercise associations with reps/sets/duration
    we1 = WorkoutExercise(
        workout_id=workout1.id,
        exercise_id=exercise1.id,
        sets=3,
        reps=15,
        duration_seconds=None
    )
    
    we2 = WorkoutExercise(
        workout_id=workout1.id,
        exercise_id=exercise4.id,
        sets=4,
        reps=10,
        duration_seconds=None
    )
    
    we3 = WorkoutExercise(
        workout_id=workout2.id,
        exercise_id=exercise3.id,
        sets=5,
        reps=8,
        duration_seconds=None
    )
    
    we4 = WorkoutExercise(
        workout_id=workout2.id,
        exercise_id=exercise4.id,
        sets=4,
        reps=12,
        duration_seconds=None
    )
    
    we5 = WorkoutExercise(
        workout_id=workout3.id,
        exercise_id=exercise2.id,
        sets=None,
        reps=None,
        duration_seconds=1800  # 30 minutes
    )
    
    db.session.add_all([we1, we2, we3, we4, we5])
    db.session.commit()
    print(f"Created {WorkoutExercise.query.count()} workout-exercise associations")
    
    print("Seeding complete!")
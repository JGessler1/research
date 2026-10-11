
from flask import Flask, request, send_from_directory, jsonify
from pathlib import Path

app = Flask(__name__)
FRONTEND = Path(__file__).parent / "frontend"

WORKOUTS = {
    "Build Muscle": [
        ("Push-ups", 3, "8–12 reps"),
        ("Squats", 3, "10–12 reps"),
        ("Dumbbell Rows", 3, "8–12 reps"),
        ("Lunges", 2, "10 each leg"),
        ("Plank", 3, "30 seconds"),
    ],
    "General Fitness": [
        ("Bodyweight Squats", 3, "10–12 reps"),
        ("Push-ups", 3, "8–10 reps"),
        ("Glute Bridges", 3, "12 reps"),
        ("Bird Dogs", 2, "10 each side"),
        ("Plank", 3, "20–30 seconds"),
    ],
    "Cardio Fitness": [
        ("Brisk Walking", 1, "5 minutes"),
        ("Jumping Jacks", 3, "30 seconds"),
        ("Bodyweight Squats", 3, "12 reps"),
        ("Mountain Climbers", 3, "30 seconds"),
        ("Cool-down Walk", 1, "5 minutes"),
    ],
}


@app.route("/")
def home():
    return send_from_directory(FRONTEND, "index.html")


@app.route("/style.css")
def stylesheet():
    return send_from_directory(FRONTEND, "style.css")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True) or {}

    goal = data.get("goal")
    level = data.get("level")
    duration = data.get("duration")

    if goal not in WORKOUTS or level not in ("Beginner", "Intermediate"):
        return jsonify({"error": "Please select valid workout options."}), 400

    try:
        duration = int(duration)
    except (ValueError, TypeError):
        return jsonify({"error": "Please select a valid duration."}), 400

    if duration not in (15, 30, 45, 60):
        return jsonify({"error": "Please select a valid duration."}), 400

    exercises = []

    for name, sets, reps in WORKOUTS[goal]:
        if level == "Beginner":
            sets = max(1, sets - 1)

        exercises.append({
            "name": name,
            "sets": sets,
            "reps": reps
        })

    return jsonify({
        "goal": goal,
        "level": level,
        "duration": duration,
        "exercises": exercises
    })


if __name__ == "__main__":
    app.run(debug=True)

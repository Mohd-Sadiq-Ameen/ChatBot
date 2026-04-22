from flask import Flask, request, render_template, jsonify, session
from dotenv import load_dotenv
import google.generativeai as genai
import os
import json

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

SYSTEM_PROMPT = """You are CalorieAI — a sharp, knowledgeable nutrition and fitness coach embedded in a calorie tracking app. You have access to the user's current stats when they share them.

Your personality:
- Direct, friendly, and motivating — like a personal trainer who actually cares
- Science-backed advice, no fads or myths
- Give specific, actionable tips — not vague platitudes
- Keep responses concise (2-4 short paragraphs max) unless a detailed breakdown is asked for
- Use emojis sparingly but effectively (1-3 per response max)

You help with:
- Analyzing their calorie balance and whether they're on track
- Food suggestions, meal ideas, macros
- Exercise and burn advice
- Weight loss / muscle gain strategies
- Interpreting their BMR and TDEE
- Motivation and habit building

When the user shares their stats (calories eaten, burned, goal, BMR etc.), reference those numbers specifically in your advice. Be a real coach, not a generic chatbot."""

chat_sessions = {}

def get_chat_session(session_id):
    if session_id not in chat_sessions:
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            system_instruction=SYSTEM_PROMPT
        )
        chat_sessions[session_id] = model.start_chat(history=[])
    return chat_sessions[session_id]

def calculate_bmr(weight, height, age, gender):
    if gender == "male":
        return round(10 * weight + 6.25 * height - 5 * age + 5)
    else:
        return round(10 * weight + 6.25 * height - 5 * age - 161)

def get_tdee(bmr, activity):
    multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9
    }
    return round(bmr * multipliers.get(activity, 1.2))

def get_calorie_goal(tdee, goal):
    if goal == "loss":
        return tdee - 500
    elif goal == "gain":
        return tdee + 500
    return tdee

@app.route("/")
def index():
    if "session_id" not in session:
        session["session_id"] = os.urandom(16).hex()
    return render_template("index.html")

@app.route("/api/profile", methods=["POST"])
def save_profile():
    d = request.json
    profile = {
        "weight": float(d["weight"]),
        "height": float(d["height"]),
        "age": float(d["age"]),
        "gender": d["gender"],
        "activity": d.get("activity", "moderate"),
        "goal": d["goal"]
    }
    bmr = calculate_bmr(profile["weight"], profile["height"], profile["age"], profile["gender"])
    tdee = get_tdee(bmr, profile["activity"])
    calorie_goal = get_calorie_goal(tdee, profile["goal"])
    profile["bmr"] = bmr
    profile["tdee"] = tdee
    profile["calorie_goal"] = calorie_goal
    session["profile"] = profile
    session["food_log"] = []
    session["burn_total"] = 0
    return jsonify({"success": True, "profile": profile})

@app.route("/api/log/food", methods=["POST"])
def log_food():
    d = request.json
    if "food_log" not in session:
        session["food_log"] = []
    entry = {"name": d["name"], "calories": float(d["calories"])}
    log = session["food_log"]
    log.append(entry)
    session["food_log"] = log
    total = sum(e["calories"] for e in log)
    return jsonify({"success": True, "log": log, "total": total})

@app.route("/api/log/burn", methods=["POST"])
def log_burn():
    d = request.json
    current = session.get("burn_total", 0)
    new_total = current + float(d["calories"])
    session["burn_total"] = new_total
    return jsonify({"success": True, "total": new_total})

@app.route("/api/log/clear", methods=["POST"])
def clear_log():
    session["food_log"] = []
    session["burn_total"] = 0
    return jsonify({"success": True})

@app.route("/api/stats", methods=["GET"])
def get_stats():
    profile = session.get("profile", {})
    food_log = session.get("food_log", [])
    burn_total = session.get("burn_total", 0)
    food_total = sum(e["calories"] for e in food_log)
    net = food_total - burn_total
    goal = profile.get("calorie_goal", 2000)
    remaining = goal - net
    return jsonify({
        "profile": profile,
        "food_log": food_log,
        "food_total": food_total,
        "burn_total": burn_total,
        "net": net,
        "goal": goal,
        "remaining": remaining
    })

@app.route("/api/chat", methods=["POST"])
def chat():
    d = request.json
    user_message = d.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    session_id = session.get("session_id", "default")
    chat_obj = get_chat_session(session_id)

    profile = session.get("profile", {})
    food_log = session.get("food_log", [])
    burn_total = session.get("burn_total", 0)
    food_total = sum(e["calories"] for e in food_log)
    net = food_total - burn_total

    context = ""
    if profile:
        goal_map = {"loss": "weight loss", "gain": "muscle gain", "maintain": "maintenance"}
        context = f"""[User's current stats: Weight={profile.get('weight')}kg, Height={profile.get('height')}cm, Age={profile.get('age')}, Gender={profile.get('gender')}, Goal={goal_map.get(profile.get('goal','maintain'))}, BMR={profile.get('bmr')} kcal, TDEE={profile.get('tdee')} kcal, Calorie target={profile.get('calorie_goal')} kcal, Eaten today={food_total} kcal, Burned={burn_total} kcal, Net intake={net} kcal, Remaining={profile.get('calorie_goal',2000)-net} kcal]

User message: {user_message}"""
    else:
        context = user_message

    try:
        response = chat_obj.send_message(context)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
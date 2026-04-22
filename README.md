CalorieAI 🥗
A smart calorie tracking web app powered by Flask + Gemini AI.
Setup

Install dependencies

bash   pip install -r requirements.txt

Add your Gemini API key

bash   cp .env.example .env
   # Edit .env and add your GOOGLE_API_KEY

Run the app

bash   python app.py

Open http://localhost:5000 in your browser.

Features

BMR & TDEE Calculator — Mifflin-St Jeor formula with activity multipliers
Daily Food Log — Track meals and calories consumed
Exercise Log — Log burned calories
Progress Bar — Visual progress toward daily goal
AI Coach — Gemini 2.0 Flash chatbot with full awareness of your stats
Quick Prompts — One-click coaching questions

Structure
CalorieAI/
├── app.py              # Flask backend + Gemini AI
├── requirements.txt
├── .env                # Your API key (don't commit!)
└── templates/
    └── index.html      # Full UI
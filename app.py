from flask import Flask, request, render_template
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()
app = Flask(__name__)

# Conversation list to store chat history
conversation = []

@app.route('/', methods=['GET', 'POST'])
def index():
    global conversation
    
    if request.method == 'POST':
        user_prompt = request.form.get('show_data')
        
        # Add user message to conversation
        conversation.append({"role": "user", "content": user_prompt})

        # Get AI response
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction="You are a BCA Student. Your name is Tekken. Answer in very short always",
                thinking_config=types.ThinkingConfig(thinking_budget=0)
            ),
        )
        answer = response.text

        # Add AI message to conversation
        conversation.append({"role": "ai", "content": answer})

    return render_template('index.html', conversation=conversation)

if __name__ == '__main__':
    app.run(debug=True)

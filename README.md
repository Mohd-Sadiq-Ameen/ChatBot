# ChatBot

A simple **Flask-based ChatBot application** using Google's Gemini API.

## 🚀 Features
- Built with Flask
- Simple web interface for chatting
- Easy to customize

## 📝 Customizing the ChatBot

In the `app.py` file, there is a variable called `system_prompt = ""`.  
You can write instructions in English inside this variable to tell the chatbot how it should behave.  
For example:
```python
system_prompt = "You are a friendly assistant that answers questions politely."


## 🛠 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Mohd-Sadiq-Ameen/ChatBot.git
   cd ChatBot
   ```

2. **Create a `.env` file** in the project root and add your Gemini API key:
   ```ini
   GEMINI_API=your_api_key_here
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask app**
   ```bash
   python app.py
   ```

5. **5. Open your browser and go to:**

      http://127.0.0.1:5000

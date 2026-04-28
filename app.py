from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "llama-3.1-8b-instant"

def ask_ai(prompt):
    res = client.chat.completions.create(
        model=MODEL,
        messages=[{"role":"user","content":prompt}],
        temperature=0.7
    )
    return res.choices[0].message.content

@app.route("/")
def home():
    return jsonify({"message":"BrainForgeAI Backend Running"})

@app.route("/notes", methods=["POST"])
def notes():
    text = request.json["text"]
    prompt = f"Convert this into clean study notes with headings and bullet points:\n{text}"
    return jsonify({"result": ask_ai(prompt)})

@app.route("/planner", methods=["POST"])
def planner():
    data = request.json

    prompt = f"""
Create a smart study planner.

Subjects: {data['subjects']}
Exam Date: {data['date']}
Daily Free Hours: {data['hours']}

Give daily plan.
"""
    return jsonify({"result": ask_ai(prompt)})

@app.route("/quiz", methods=["POST"])
def quiz():
    text = request.json["text"]

    prompt = f"""
Create a quiz from these notes.
Give questions, answers and explanations.

{text}
"""
    return jsonify({"result": ask_ai(prompt)})

if __name__ == "__main__":
    app.run(debug=True, port=5000)

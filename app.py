from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


restaurant_info = """
You are a friendly assistant for Glamour Studio — a premium salon and barber shop.
Only answer questions related to the salon.
Keep replies short, warm and use light emojis.
If someone asks something unrelated politely say you can only help with salon related questions.

Business Information:
- Name: Glamour Studio
- Location: 456 Style Street, Miami, FL
- Opening Hours: Monday to Saturday, 9 AM to 8 PM. Closed Sundays.
- Phone: +1 305 123 4567
- Services: Haircuts, Hair Coloring, Beard Trim, Facial, Manicure, Pedicure
- Pricing: Haircut from $25, Color from $60, Beard Trim $15, Facial $45
- Booking: Available by WhatsApp or walk-in
- Staff: 5 experienced stylists
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": restaurant_info},
            {"role": "user", "content": user_message}
        ]
    )
    
    reply = response.choices[0].message.content
    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
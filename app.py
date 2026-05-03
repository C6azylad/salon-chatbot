from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = Flask(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

APPS_SCRIPT_URL = os.getenv("APPS_SCRIPT_URL")

salon_info = """
You are a friendly assistant for Glamour Studio — a premium salon and barber shop.
Only answer questions related to the salon.
Keep replies short, warm and use light emojis.
If someone asks something unrelated, politely say you can only help with salon-related questions.

Business Information:
- Name: Glamour Studio
- Location: 456 Style Street, Miami, FL
- Opening Hours: Monday to Saturday, 9 AM to 8 PM. Closed Sundays.
- Phone: +1 305 123 4567
- Services: Haircuts, Hair Coloring, Beard Trim, Facial, Manicure, Pedicure
- Pricing: Haircut from $25, Color from $60, Beard Trim $15, Facial $45
- Booking: Clients can book directly in this chat
- Staff: 5 experienced stylists
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")
    history = data.get("history", [])

    messages = [{"role": "system", "content": salon_info}]
    messages += history
    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )

    reply = response.choices[0].message.content
    return jsonify({"reply": reply})

@app.route("/book", methods=["POST"])
def book():
    data = request.json
    name    = data.get("name", "").strip()
    phone   = data.get("phone", "").strip()
    email   = data.get("email", "").strip()
    service = data.get("service", "").strip()
    date    = data.get("date", "").strip()
    time    = data.get("time", "").strip()

    if not all([name, phone, email, service, date, time]):
        return jsonify({"success": False, "error": "Missing fields"}), 400

    if not APPS_SCRIPT_URL:
        return jsonify({"success": False, "error": "Apps Script URL not configured"}), 500

    try:
        r = requests.get(APPS_SCRIPT_URL, params={
            "name": name,
            "phone": phone,
            "email": email,
            "service": service,
            "date": date,
            "time": time
        }, timeout=10)
        r.raise_for_status()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

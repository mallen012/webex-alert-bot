
from flask import Flask, request, jsonify, send_from_directory
import os, requests, re
from dotenv import load_dotenv
from datetime import datetime, date

load_dotenv()
app = Flask(__name__)

def send_webex_message(message):
    headers = {
        "Authorization": f"Bearer {os.getenv('WEBEX_TOKEN')}",
        "Content-Type": "application/json"
    }
    payload = {
        "roomId": os.getenv("WEBEX_ROOM_ID"),
        "text": message
    }
    requests.post("https://webexapis.com/v1/messages", headers=headers, json=payload)

@app.route("/alert", methods=["POST"])
def alert():
    data = request.get_json()
    message = data.get("message", "No message provided")
    send_webex_message(message)
    return jsonify({"status": "Message sent"})

@app.route("/update-config", methods=["POST"])
def update_config():
    data = request.get_json()
    token = data.get("WEBEX_TOKEN")
    room = data.get("WEBEX_ROOM_ID")
    if token and room:
        with open(".env", "w") as f:
            f.write(f"WEBEX_TOKEN={token}\nWEBEX_ROOM_ID={room}\n")
        os._exit(1)
    return jsonify({"status": "Invalid input"})

@app.route("/webex", methods=["POST"])
def receive_webex():
    data = request.get_json()
    message = data.get("text", "").strip().lower()

    if message.startswith("/dadjoke"):
        r = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"})
        send_webex_message(r.json().get("joke", "No joke found."))
        return jsonify({"status": "dadjoke sent"})

    if message.startswith("/weather"):
        zip_code = message.replace("/weather", "").strip()
        key = os.getenv("OPENWEATHER_API_KEY")
        if re.match(r"^\d{5}$", zip_code) and key:
            url = f"http://api.openweathermap.org/data/2.5/weather?zip={zip_code},us&units=imperial&appid={key}"
            r = requests.get(url)
            if r.status_code == 200:
                d = r.json()
                msg = f"Weather in {d['name']}: {d['weather'][0]['description'].title()}\nTemp: {d['main']['temp']}°F"
                send_webex_message(msg)
                return jsonify({"status": "weather sent"})
        send_webex_message("Invalid ZIP or missing API key.")
        return jsonify({"status": "weather error"})

    if message.startswith("/movie"):
        zip_code = message.replace("/movie", "").strip()
        key = os.getenv("MOVIE_API_KEY")
        today = date.today().isoformat()
        url = f"http://data.tmsapi.com/v1.1/movies/showings?startDate={today}&zip={zip_code}&api_key={key}"
        r = requests.get(url)
        if r.status_code == 200:
            movies = r.json()
            titles = [m['title'] for m in movies[:5]]
            send_webex_message("Movies tonight:\n" + "\n".join(titles))
            return jsonify({"status": "movies sent"})

    if message.startswith("/tv"):
        key = os.getenv("TV_API_KEY")
        now = datetime.now()
        start = now.replace(hour=18, minute=0).isoformat()
        end = now.replace(hour=22, minute=0).isoformat()
        networks = ["ABC", "NBC", "CBS", "Paramount", "Max"]
        url = f"https://api.tvmedia.ca/tvlistings?start={start}&end={end}&networks={','.join(networks)}&api_key={key}"
        r = requests.get(url)
        if r.status_code == 200:
            listings = r.json()
            entries = [f"{l['network']}: {l['program']}" for l in listings[:5]]
            send_webex_message("TV Tonight:\n" + "\n".join(entries))
            return jsonify({"status": "tv sent"})

    return jsonify({"status": "unknown command"})

@app.route("/")
def ui():
    return send_from_directory("static", "index.html")


from flask_sock import Sock
sock = Sock(app)

@sock.route("/alert")
def websocket_alert(ws):
    while True:
        message = ws.receive()
        if message:
            send_webex_message(message)
            ws.send("Sent: " + message)

from flask import Flask, request, render_template
import json
import datetime

app = Flask(__name__)
messages = []

# Load saved messages from file
try:
    with open("messages.txt", "r") as f:
        for line in f:
            messages.append(json.loads(line.strip()))
except FileNotFoundError:
    pass

@app.route('/')
def index():
    return render_template('index.html', messages=messages)

@app.route('/message', methods=['POST'])
def receive_message():
    data = request.get_json()
    sender = data.get('sender', 'Unknown')
    salinity = data.get('salinity')
    temperature = data.get('temperature')
    pH = data.get('pH')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entry = {
        'sender': sender,
        'salinity': salinity,
        'temperature': temperature,
        'pH': pH,
        'time': timestamp
    }

    messages.append(entry)

    with open("messages.txt", "a") as f:
        f.write(json.dumps(entry) + "\n")

    return {'status': 'success', 'message': entry}


from waitress import serve

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=10000)

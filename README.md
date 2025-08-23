# FieldLink Server (using ESP8266)

Flask-based backend and dashboard for monitoring environmental sensor data from remote ESP8266 devices deployed by farmers.

## Features
- Accepts JSON POST requests from ESP8266
- Displays real-time sensor data
- Modular and ready for deployment

## Setup
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Run the server: `python server.py`

## Deployment
Use Render with `render.yaml` and `gunicorn server:app`

from flask import Flask, render_template, jsonify
import requests
from datetime import datetime, timedelta
import configparser

# Read API keys from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

GOOGLE_MAPS_API_KEY = config['api_keys']['google_maps_api_key']
WEATHER_API_KEY = config['api_keys']['weather_api_key']

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', google_maps_api_key=GOOGLE_MAPS_API_KEY)

@app.route('/current/<float:lat>/<float:lng>')
def current(lat, lng):
    weather_url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={lat},{lng}"
    response = requests.get(weather_url)
    weather_data = response.json()
    temperature = weather_data['current']['temp_c']
    return jsonify(lat=lat, lng=lng, temperature=temperature)

@app.route('/history/<float:lat>/<float:lng>')
def history(lat, lng):
    historical_data = []
    for i in range(7):
        date = (datetime.utcnow() - timedelta(days=i)).strftime('%Y-%m-%d')
        weather_url = f"http://api.weatherapi.com/v1/history.json?key={WEATHER_API_KEY}&q={lat},{lng}&dt={date}"
        response = requests.get(weather_url)
        weather_data = response.json()
        temperature = weather_data['forecast']['forecastday'][0]['day']['avgtemp_c']
        historical_data.append({'date': date, 'temperature': temperature})
    return jsonify(historical_data=historical_data)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect,flash, jsonify
import requests
import sqlite3
import threading
import time
from datetime import datetime
from config import API_URL, OPENWEATHER_API_KEY, CITY_IDS, SECRET_KEY, DB_PATH

app = Flask(__name__)
app.secret_key = SECRET_KEY
stop_thread = threading.Event()

# Alert configuration
alert_config = {'temp_threshold': None, 'weather_condition': None}

# Weather icon mapping
weather_icon_map = {
    "Clear": "wi-day-sunny",
    "Clouds": "wi-cloudy",
    "Rain": "wi-rain",
    "Thunderstorm": "wi-thunderstorm",
    "Snow": "wi-snow",
    "Mist": "wi-fog",
    "Haze": "wi-day-haze"
}

@app.route('/')
def home():
    selected_city = "Delhi"
    temp_unit = "Celsius"
    weather_data, daily_summaries = get_latest_weather(temp_unit, selected_city)

    return render_template(
        'index.html',
        weather_data=weather_data,
        selected_city=selected_city,
        temp_unit=temp_unit,
        weather_icon_map=weather_icon_map,
        daily_summaries=daily_summaries,
        city_ids=CITY_IDS
    )

def create_database():
    """Create necessary tables if they do not exist."""
    conn = sqlite3.connect(DB_PATH, timeout=10)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS daily_summary (
        date TEXT PRIMARY KEY, city TEXT, avg_temp REAL, max_temp REAL, 
        min_temp REAL, dominant_condition TEXT, avg_humidity REAL, avg_wind_speed REAL
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_alerts (
        city TEXT, threshold_temp REAL, condition TEXT
    )''')
    conn.commit()
    conn.close()

def fetch_weather_data(city_id):
    """Fetch weather data with retry logic."""
    url = f"{API_URL}/weather?id={city_id}&appid={OPENWEATHER_API_KEY}&units=metric"
    for _ in range(3):  # Retry up to 3 times
        try:
            response = requests.get(url, timeout=10)
            print(f"API Response: {response.status_code}, {response.text}")  # Debugging log

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                flash(f"City not found: {response.json().get('message', 'Unknown error')}")
            else:
                flash(f"Error: {response.json().get('message', 'Unknown error')}")
        except requests.RequestException as e:
            print(f"Error fetching data for city_id {city_id}: {e}")
            flash(f"Network error: {str(e)}")
            time.sleep(2)
    return {}

def process_weather_data(entry):
    """Extract weather data from API response."""
    timestamp = datetime.fromtimestamp(entry.get('dt', time.time()))
    temp = entry['main'].get('temp', 0)
    humidity = entry['main'].get('humidity', 0)
    wind_speed = entry['wind'].get('speed', 0)
    condition = entry['weather'][0].get('main', 'Unknown')
    feels_like = entry['main'].get('feels_like', 0)  # Added perceived temperature
    return timestamp, temp, humidity, wind_speed, condition, feels_like

def calculate_daily_summary(weather_data, city):
    """Store weather summary in the database."""
    today = datetime.now().date()
    summary = {'avg_temp': 0, 'max_temp': float('-inf'), 'min_temp': float('inf'),
               'total_humidity': 0, 'total_wind_speed': 0, 'condition_count': {}}

    count = 0

    for data in weather_data.values():
        temp = data['temp']
        summary['avg_temp'] += temp
        summary['max_temp'] = max(summary['max_temp'], temp)
        summary['min_temp'] = min(summary['min_temp'], temp)
        summary['total_humidity'] += data['humidity']
        summary['total_wind_speed'] += data['wind_speed']
        condition = data['condition']
        summary['condition_count'][condition] = summary['condition_count'].get(condition, 0) + 1
        count += 1

    if count > 0:
        avg_temp = round(summary['avg_temp'] / count, 2)
        avg_humidity = round(summary['total_humidity'] / count, 2)
        avg_wind_speed = round(summary['total_wind_speed'] / count, 2)
        dominant_condition = max(summary['condition_count'], key=summary['condition_count'].get)
    else:
        avg_temp = avg_humidity = avg_wind_speed = 0
        dominant_condition = "Unknown"

    conn = sqlite3.connect(DB_PATH, timeout=10)
    try:
        cursor = conn.cursor()
        cursor.execute('''INSERT OR REPLACE INTO daily_summary 
                          (date, city, avg_temp, max_temp, min_temp, dominant_condition, avg_humidity, avg_wind_speed)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                       (today, city, avg_temp, summary['max_temp'], summary['min_temp'], 
                        dominant_condition, avg_humidity, avg_wind_speed))
        conn.commit()
    finally:
        conn.close()

def get_daily_summaries(city=None):
    """Retrieve daily summaries from the database."""
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        if city:
            cursor.execute('SELECT * FROM daily_summary WHERE city = ?', (city,))
        else:
            cursor.execute('SELECT * FROM daily_summary')

        summaries = cursor.fetchall()
        return [dict(zip(['date', 'city', 'avg_temp', 'max_temp', 'min_temp', 
                          'dominant_condition', 'avg_humidity', 'avg_wind_speed'], row))
                for row in summaries]
    finally:
        conn.close()

def get_latest_weather(temp_unit='Celsius', selected_city=None):
    """Fetch latest weather data and summaries."""
    weather_data = {}
    if selected_city:
        city_id = CITY_IDS[selected_city]
        data = fetch_weather_data(city_id)
        if data:
            timestamp, temp, humidity, wind_speed, condition, feels_like = process_weather_data(data)
            weather_data[selected_city] = {
                'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'temp': temp,
                'feels_like': feels_like,  # Store perceived temperature
                'humidity': humidity,
                'wind_speed': wind_speed,
                'condition': condition,
            }
            calculate_daily_summary(weather_data, selected_city)
    return weather_data, get_daily_summaries(selected_city)

@app.route('/get_weather', methods=['POST'])
def get_weather():
    selected_city = request.form.get('city', 'Delhi')
    temp_unit = request.form.get('temp_unit', 'Celsius')
    weather_data, daily_summaries = get_latest_weather(temp_unit, selected_city)

    return render_template(
        'index.html',
        weather_data=weather_data,
        selected_city=selected_city,
        temp_unit=temp_unit,
        weather_icon_map=weather_icon_map,
        daily_summaries=daily_summaries,
        city_ids=CITY_IDS
    )

@app.route('/set_alert', methods=['POST'])
def set_alert():
    temp_threshold = request.form.get('temp_threshold')
    weather_condition = request.form.get('weather_condition')

    # Store thresholds and conditions in alert configuration.
    alert_config['temp_threshold'] = temp_threshold
    alert_config['weather_condition'] = weather_condition

    flash("Alert configuration updated successfully!", "success")
    return redirect('/')

@app.before_first_request
def start_background_thread():
    threading.Thread(target=run_background_process, daemon=True).start()

def run_background_process():
    while not stop_thread.is_set():
        get_latest_weather()
        time.sleep(300)
@app.route('/weather/<city>', methods=['GET'])
def weather(city):
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric')
    return jsonify(response.json())
@app.teardown_appcontext
def stop_background_thread(exception=None):
    stop_thread.set()
@app.route('/get-api-key')
def get_api_key():
    return jsonify(api_key=OPENWEATHER_API_KEY)
@app.route('/')
def index():
    return render_template('index.html', api_key=OPENWEATHER_API_KEY )
if __name__ == "__main__":
    app.run(debug=True)

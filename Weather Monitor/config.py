import os
import secrets

OPENWEATHER_API_KEY = 'YOUR_API_KEY'  # Replace with your actual API key
API_URL = "https://api.openweathermap.org/data/2.5"
SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(16))

CITY_IDS = {
    'Delhi': 1273294,
    'Mumbai': 1275339,
    'Chennai': 1264527,
    'Bangalore': 1277333,
    'Kolkata': 1275004,
    'Hyderabad': 1269843
}
DB_PATH = "weather_data.db"

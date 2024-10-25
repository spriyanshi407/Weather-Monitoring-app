# Weather-Monitoring-app


## Overview
The **Weather Monitoring Application** is a dynamic web-based application designed to provide users with real-time weather data, forecasts, and alerts for selected cities. This application combines a user-friendly interface with powerful backend functionality to deliver timely and accurate weather information.

## Features
- **Real-Time Weather Data**: View current weather conditions, including temperature, humidity, wind speed, and weather icons.
- **Daily Summaries**: Access daily weather summaries that aggregate and display weather data for selected cities.
- **Custom Alerts**: Users can set personalized alerts for specific temperature thresholds and weather conditions (e.g., rain, snow).
- **City Selection**: A dropdown menu to easily select from a list of predefined cities or add new cities.
- **Responsive Design**: The application is fully responsive, ensuring a seamless experience across desktop and mobile devices.
- **Dark Mode**: A toggle button to switch between light and dark themes, enhancing usability in various lighting conditions.
- **Weather Forecasts**: Users can view 5- or 7-day weather forecasts for selected cities (if implemented).
- **Geolocation Support**: Automatically fetch and display weather data for the user's current location (if implemented).
- **Historical Data Access**: Access past weather data for selected cities (if implemented).
- **Visualizations**: Charts and graphs for visual representation of weather trends and historical data (if implemented).

## Technologies Used
- **Frontend**: 
  - HTML5
  - CSS3 (with Flexbox and Grid)
  - JavaScript (for interactivity)
  - Bootstrap (for responsive design)
- **Backend**: 
  - Flask (Python web framework)
  - Jinja2 (template engine for rendering HTML)
- **Database**: 
  - SQLite
- **API**: 
  - [OpenWeatherMap API](https://openweathermap.org/api) for fetching weather data

## Installation
To run the application locally, follow these steps:

1. **Clone the repository**:
  - git clone https://github.com/yourusername/weather-monitoring-app.git
  - cd "Weather Monitor"
2. **Set up a virtual environment (optional but recommended):**
  - python -m venv venv
  - venv\Scripts\activate
3. **Install the required dependencies:**
  - pip install Flask==2.3.2
  - pip install flask requests
4. **Set up your API key:**
   Create a file named config.py and add your OpenWeatherMap API key:
  - API_KEY = 'your_openweathermap_api_key'
5. **Run the application:**
  - python app.py
6. **Open your web browser** and navigate to http://127.0.0.1:5000.

## Usage
**City Selection**:  Choose a city from the dropdown menu.
**Temperature Unit**":  Select your preferred temperature unit (Celsius or Fahrenheit).
**Get Weather**:  Click the "Get Weather" button to fetch and display the current weather conditions.
**Set Alerts**:  Use the alert form to set temperature thresholds and select weather conditions for alerts.
**Explore Daily Summaries**: Access daily weather summaries to view aggregated data.
**Toggle Dark Mode**:  Click the dark mode button to switch themes.

## Future Enhancements
The following features are planned for future updates:

**User Authentication**: Allow users to create accounts and save their preferences and alert settings.
**Enhanced Forecasting**: Integration with additional weather APIs for more accurate forecasting.
**Additional Weather Parameters**: Expand the application to display more weather metrics like UV index, visibility, etc.
**Mobile App Version**: Development of a mobile application for better accessibility.
**Interactive Maps**: Integration of interactive maps to visualize weather data geographically.

## Contribution
Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (git checkout -b feature-branch).
3. Make your changes and commit them (git commit -m 'Add new feature').
4. Push to the branch (git push origin feature-branch).
5. Create a new Pull Request.
   
## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- Special thanks to OpenWeatherMap for providing the weather data API.
- Inspired by various weather applications for their user-friendly design.
- Thank you to the community for open-source libraries and resources that made this project possible.

const themeToggle = document.getElementById('dark-mode-button');
const currentTheme = localStorage.getItem('theme');
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();

// Apply saved theme
if (currentTheme === 'dark') {
    document.body.classList.add('dark-mode');
    themeToggle.textContent = '☀️ Light Mode';
}

themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    themeToggle.textContent = document.body.classList.contains('dark-mode') ? '☀️ Light Mode' : '🌙 Dark Mode';
    localStorage.setItem('theme', document.body.classList.contains('dark-mode') ? 'dark' : 'light');
});

document.getElementById('voice-search-button').addEventListener('click', () => {
    recognition.start(); // Start voice recognition
});

recognition.onstart = () => {
    console.log('Voice recognition started. Speak now.');
};

recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript; // Get the recognized text
    console.log('Recognized text:', transcript); // Log the recognized text
    handleVoiceCommand(transcript); // Handle the recognized command
};

recognition.onerror = (event) => {
    console.error('Speech recognition error:', event.error);
    alert('Error recognizing speech. Please try again.'); // Inform user of the error
};

recognition.onend = () => {
    console.log('Voice recognition ended.');
};

function handleVoiceCommand(command) {
    const cityMatch = command.match(/weather in (\w+)/i); // Updated regex to match "weather in city"
    if (cityMatch) {
        const city = cityMatch[1];
        console.log('Fetching weather data for:', city); // Log the city being fetched
        fetchWeatherData(city); 
    } else {
        alert('Sorry, I could not understand that command. Please try "weather in [city name]"');
    }
}

function fetchWeatherData(city) {
    const apiKey = "{{ api_key }}"; // Ensure you provide the correct API key here
    const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`;

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Weather data received:', data); // Log the received data
            // Process the data and update your UI here
        })
        .catch(error => {
            console.error('Error fetching weather data:', error);
            alert('Could not fetch weather data. Please try again.');
        });
}

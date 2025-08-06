

#  WeatherWise – Your Smart Weather Assistant

**WeatherWise** is a friendly and intelligent chatbot that provides real-time weather updates, clothing suggestions, and helpful safety tips based on the user’s location and current conditions. The app allows users to ask questions like “What’s the weather in Mumbai today?” or “What should I wear during the rain?”, and responds in a simple and useful format. Whether it’s sunny, rainy, or cold, WeatherWise helps users stay prepared for the day.

---

## LLM Concepts Used

### System Prompt and User Prompt

The system prompt defines the assistant’s role and tone. It is set to make the assistant behave like a helpful weather expert. The user prompt is the question typed by the user, such as asking about the weather in a specific city or requesting suggestions for what to wear or avoid in current weather conditions.

### Tuning Parameters

The assistant uses specific tuning values like temperature and top-p to control the response style. A lower temperature is used to keep the answers more accurate and focused. This ensures the chatbot stays consistent and helpful without being too random.

### Structured Output

The chatbot responds with neatly organized information like location, temperature, weather condition, outfit suggestion, and a tip. This format helps in easily displaying the results on a user interface or app screen.

### Function Calling

WeatherWise connects to real-time weather APIs through function calling. When a user asks about the weather, the assistant triggers a backend function to fetch live weather data, like temperature or UV index, based on the user’s city.

### Retrieval-Augmented Generation (RAG)

In addition to live data, the assistant also searches a small knowledge base (like documents or local tips) for season-specific advice. For example, during monsoon season, it might suggest carrying an umbrella or avoiding flood-prone areas by retrieving safety tips from a stored document.

---

## Features

* Gives live weather updates
* Suggests clothes and activities based on the weather
* Provides safety tips using internal knowledge
* Calls APIs to fetch real-time data
* Returns clear, structured responses for the user

---

## Future Scope

* Add voice assistant functionality
* Include a multi-day forecast
* Show weather alerts and warnings


import requests
import google.generativeai as genai

# API Keys
GEMINI_API_KEY = "AIzaSyCJfcW0dMSptZ1TBzHxzXyeNkXM6urAW4Y"  
WEATHER_API_KEY = "941616aadcd50e3cdb8f82f318e6ed9e"      

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


def get_weather(city: str):
    """Fetch current weather and temperature for a city"""
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": WEATHER_API_KEY, "units": "metric"}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        weather = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        return weather, temp
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")


def ask_gemini(weather: str, temp: float):
    """Ask Gemini what is needed for given weather conditions (few-shot prompt included)"""
    prompt = f"""
You are a weather assistant. Based on current weather, list essentials in 2-3 bullet points.

### Example 1:
Weather: Sunny, Temperature: 30°C
Advice:
- Wear light cotton clothes
- Carry sunglasses or a hat
- Stay hydrated with water

### Example 2:
Weather: Rainy, Temperature: 22°C
Advice:
- Carry an umbrella or raincoat
- Wear waterproof shoes
- Avoid slippery roads

### Example 3:
Weather: Cold, Temperature: 10°C
Advice:
- Wear a warm jacket and gloves
- Carry a thermos with hot drink
- Use moisturizer for dry skin

### Now for the user:
Weather: {weather}, Temperature: {temp}°C
Advice:
"""
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=0.7,   # Controls randomness
            top_k=5,           # Considers top 5 tokens
            top_p=0.9          # Nucleus sampling: keeps only top tokens whose cumulative prob ≥ 90%
        )
    )
    return response.text


if __name__ == "__main__":
    city = input("Enter city name: ")
    try:
        weather, temp = get_weather(city)
        print(f"\n[Weather API] {city}: {weather}, {temp}°C")

        advice = ask_gemini(weather, temp)
        print(f"\n[Gemini Advice]\n{advice}")

    except Exception as e:
        print("Error:", e)

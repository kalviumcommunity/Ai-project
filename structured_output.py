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


def ask_gemini_structured(weather: str, temp: float):
    """Ask Gemini with structured output"""

    user_prompt = f"The current weather is: {weather}, temperature {temp}°C. Suggest what a person should carry or wear."

    response = model.generate_content(
        user_prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=0.7,
            top_k=5,
            top_p=0.9,
            response_mime_type="application/json",
            response_schema={
                "type": "object",
                "properties": {
                    "advice": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of short, practical advice points"
                    }
                },
                "required": ["advice"]
            }
        )
    )

    return response.text 


if __name__ == "__main__":
    city = input("Enter city name: ")
    try:
        weather, temp = get_weather(city)
        print(f"\n[Weather API] {city}: {weather}, {temp}°C")

        advice_json = ask_gemini_structured(weather, temp)
        print(f"\n[Gemini Advice - Structured JSON]\n{advice_json}")

    except Exception as e:
        print("Error:", e)

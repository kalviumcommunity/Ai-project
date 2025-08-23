import requests
import google.generativeai as genai

GEMINI_API_KEY = "AIzaSyCJfcW0dMSptZ1TBzHxzXyeNkXM6urAW4Y"  
WEATHER_API_KEY = "941616aadcd50e3cdb8f82f318e6ed9e"      

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
    """Ask Gemini what is needed for given weather conditions"""
    prompt = f"""
The current weather is: {weather}, temperature {temp}°C.
List the essential things a person should carry or wear in this weather.
Answer in 2-3 bullet points.
"""
    response = model.generate_content(prompt)
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

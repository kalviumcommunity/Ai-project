import os
import re
import json
import requests
import google.generativeai as genai

GEMINI_API_KEY = "AIzaSyCJfcW0dMSptZ1TBzHxzXyeNkXM6urAW4Y"   
WEATHER_API_KEY = "941616aadcd50e3cdb8f82f318e6ed9e"         

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def get_weather(city: str):
    """Fetch current weather and temperature for a city"""
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": WEATHER_API_KEY, "units": "metric"}
    response = requests.get(url, params=params, timeout=10)

    if response.status_code == 200:
        data = response.json()
        weather = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        return weather, temp
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

def ask_gemini_cot_safe(weather: str, temp: float):
    """
    Ask Gemini to reason internally (chain-of-thought), but only return a concise final answer.
    Output is strict JSON so it's easy to parse.
    """
    prompt = f"""
You are a helpful weather assistant.

Think through the problem step by step INTERNALLY to decide the best essentials for the given weather.
Do NOT reveal your chain-of-thought. Only output the FINAL RESULT in EXACTLY this JSON format:

{{
  "advice": ["bullet 1", "bullet 2", "bullet 3"],
  "why": "one short sentence explaining the key factor (step-by-step)."
}}

Constraints:
- 2 to 3 bullets max in "advice".
- Keep "why" to one short sentence.
- No extra text outside the JSON.

Input:
Weather: {weather}
Temperature: {temp}°C
"""
    resp = model.generate_content(prompt)
    text = (resp.text or "").strip()

    # Strip code fences if the model wraps JSON in ```json ... ```
    text = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", text, flags=re.DOTALL)

    try:
        data = json.loads(text)
        # minimal validation
        if not isinstance(data.get("advice"), list) or "why" not in data:
            raise ValueError("Invalid JSON schema from model.")
        return data
    except Exception:
        # Fallback: extract top 3 dash bullets if JSON parsing fails
        bullets = [re.sub(r"^\s*-\s*", "", line).strip()
                   for line in text.splitlines() if line.strip().startswith("-")]
        bullets = bullets[:3] or ["Carry water", "Dress appropriately", "Check local alerts"]
        return {"advice": bullets, "why": "Quick essentials based on current conditions."}

if __name__ == "__main__":
    city = input("Enter city name: ").strip()
    try:
        weather, temp = get_weather(city)
        print(f"\n[Weather API] {city}: {weather}, {temp}°C")

        result = ask_gemini_cot_safe(weather, temp)
        print("\n[Gemini Advice]")
        for item in result["advice"]:
            print(f"- {item}")
        print(f"\nWhy: {result['why']}")

    except Exception as e:
        print("Error:", e)

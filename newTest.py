import requests

API_KEY = "941616aadcd50e3cdb8f82f318e6ed9e"
CITY = "Chennai"

url = "http://api.openweathermap.org/data/2.5/weather"
params = {"q": CITY, "appid": API_KEY, "units": "metric"}

r = requests.get(url, params=params)
print(r.status_code, r.text)

import requests

def fetch_weather(city):
    url = f"https://api.weatherapi.com/v1/current.json?key=your_key&q={city}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

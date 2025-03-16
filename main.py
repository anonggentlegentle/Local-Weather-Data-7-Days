import os
from dotenv import load_dotenv
from utils import extract, transform, load

load_dotenv()

api_id = os.getenv('WEATHER_API')

params_geo = {"zip": "2400,PH", "appid": api_id}

url_geo = "http://api.openweathermap.org/geo/1.0/zip"

url_weather = "https://api.openweathermap.org/data/3.0/onecall/day_summary"

weather_data = extract(url_geo, url_weather, params_geo, api_id)

weather_df = transform(weather_data)

load(weather_df)

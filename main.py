import requests
import os
from dotenv import load_dotenv
import pandas as pd
import datetime

load_dotenv()

params_geo = {"zip": "2400,PH", "appid": os.getenv('WEATHER_API')}

geo_code = requests.get(f"http://api.openweathermap.org/geo/1.0/zip", params=params_geo, headers={"accepts": "application/json"})

geo_data = geo_code.json()

lat = geo_data.get("lat")
lon = geo_data.get("lon")

df = pd.DataFrame()

days = 7

date_today = datetime.date.today()
week_ago = date_today - datetime.timedelta(days=days)

start = datetime.date(week_ago.year, week_ago.month, week_ago.day)

res = []

for day in range(days):
    date = (start + datetime.timedelta(days=days)).isoformat()
    res.append(date)

for date in res:
    weather_code = requests.get(f"https://api.openweathermap.org/data/3.0/onecall", params={"lat": lat, "lon": lon, "date": date, "appid": os.getenv("WEATHER_API")})
    print(weather_code.json())

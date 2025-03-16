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
    date = (start + datetime.timedelta(days=day + 1)).isoformat()
    res.append(date)

rows = []

for date in res:
    weather_code = requests.get(f"https://api.openweathermap.org/data/3.0/onecall/day_summary", params={"lat": lat, "lon": lon, "date": date, "units": "metric", "exclude": "minutely,hourly,current", "appid": os.getenv("WEATHER_API")})
    weather_data = weather_code.json()

    data = {"date": weather_data.get("date"), "cloud_cover": weather_data.get("cloud_cover").get("afternoon"), "humidity": weather_data.get("humidity").get("afternoon"), "precipitation": weather_data.get("precipitation").get("total"), "min_temp": weather_data.get("temperature").get("min"), "max_temp": weather_data.get("temperature").get("max"), "max_wind_speed": weather_data.get("wind").get("max").get("speed"), "wind_direction": weather_data.get("wind").get("max").get("direction")}

    rows.append(data)

for i, row in enumerate(rows):
    new_row = pd.DataFrame(row, index=[i])
    df = pd.concat([df, new_row], ignore_index=True)

print(df)

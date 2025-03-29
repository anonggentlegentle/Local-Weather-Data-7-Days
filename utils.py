import requests
import pandas as pd
import datetime as dt
import os.path
from datetime import datetime
from sqlalchemy import create_engine
import psycopg2

def extract(url_geo, url_weather, params_geo, api_id):
    geo_code = requests.get(url_geo, params=params_geo,
                            headers={"accepts": "application/json"})

    geo_data = geo_code.json()

    lat = geo_data.get("lat")

    lon = geo_data.get("lon")

    date_today = dt.date.today()

    week_ago = date_today - dt.timedelta(days=7)

    start = dt.date(week_ago.year, week_ago.month, week_ago.day)

    res = []

    for day in range(7):
        date = (start + dt.timedelta(days=day + 1)).isoformat()
        res.append(date)

    rows = []

    for date in res:
        weather_code = requests.get(url_weather,
                                    params={"lat": lat, "lon": lon, "date": date, "units": "metric",
                                                "exclude": "minutely,hourly,current", "appid": api_id})

        weather_data = weather_code.json()

        data = {"date": datetime.strptime(weather_data.get("date"), "%Y-%m-%d").strftime("%m-%d-%Y"), "cloud_cover": weather_data.get("cloud_cover").get("afternoon"),
                    "humidity": weather_data.get("humidity").get("afternoon"),
                    "precipitation": weather_data.get("precipitation").get("total"),
                    "min_temp": weather_data.get("temperature").get("min"),
                    "max_temp": weather_data.get("temperature").get("max"),
                    "max_wind_speed": weather_data.get("wind").get("max").get("speed"),
                    "wind_direction": weather_data.get("wind").get("max").get("direction")}

        rows.append(data)

    return rows

def transform(weather_data):
    df = pd.DataFrame(weather_data, index=None)

    return df

def load(dataframe, db_user, db_pass):
    con = create_engine(f"postgresql+psycopg2://{db_user}:{db_pass}@localhost:5432/weather_local")

    sql_df = pd.read_sql('SELECT * FROM dagupan_daily_weather', con=con)

    new_df = pd.concat([sql_df, dataframe], ignore_index=True)

    new_df['date'] = pd.to_datetime(new_df['date'], errors='coerce').dt.date

    new_df.drop_duplicates(subset=["date"], inplace=True, keep="first")

    new_df.sort_values(by="date", ascending=True, inplace=True)

    new_df.to_sql("dagupan_daily_weather", con=con, if_exists='replace', index=False)

    # Old way using CSV file

    # if os.path.exists("seven_day_local_weather_data.csv"):
    #     df = pd.read_csv("seven_day_local_weather_data.csv")
    #
    #     new_df = pd.concat([df, dataframe], ignore_index=True)
    #
    #     new_df.drop_duplicates(subset=["date"], inplace=True, keep="first")
    #
    #     new_df.sort_values(by="date", ascending=True, inplace=True)
    #
    #     new_df.to_csv("seven_day_local_weather_data.csv", index=False, mode="w")
    # else:
    #     dataframe.to_csv("seven_day_local_weather_data.csv", index=False, mode="w")

if __name__ == "__main__":
    print("Don't Run")
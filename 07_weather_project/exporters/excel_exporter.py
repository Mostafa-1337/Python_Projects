import pandas as pd
from scrapers.weather_scrapers import weather_datas

def save_to_excel(my_data):
    df = pd.DataFrame([my_data])
    df.to_excel(r"09_weather\result.xlsx",index=False)


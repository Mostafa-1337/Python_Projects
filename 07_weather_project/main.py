from scrapers.weather_scrapers import weather_datas
from exporters.json_exporter import save_to_json
from exporters.excel_exporter import save_to_excel

def main():
    weather_data = weather_datas()
    save_to_json(weather_data)
    save_to_excel(weather_data)

if __name__ == "__main__":
    main()





import asyncio
from exporters.excel_exporter import save_to_excel
from exporters.json_exporter import save_to_json
from scraper.scraper_file import main

def main_file():
    scrape_data = asyncio.run(main())
    save_to_json(scrape_data)
    save_to_excel(scrape_data)

if __name__ == "__main__":
    main_file()
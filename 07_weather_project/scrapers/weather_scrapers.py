from playwright.sync_api import sync_playwright

def weather_datas():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        #go to page
        page.goto("https://www.accuweather.com/en/eg/giza/127047/current-weather/127047")
        page.wait_for_load_state()
        page.click("button:has-text('accept')")
        dates = page.locator("div.content-module.subnav-pagination div").inner_text()
        temps = page.locator("div.display-temp").inner_text()
        wind_g = page.locator("div.detail-item.spaced-content", has_text="Wind Gusts").locator("div").nth(1).inner_text()
        times = page.locator("div.card-header.spaced-content p").inner_text()
        browser.close()

    data = {
        "date":dates,
        "time":times,
        "temp":temps,
        "wind speed":wind_g,
    }
        
    return data


    

from playwright.sync_api import sync_playwright
import pandas as pd

titles = []
prices = []
dollar_price = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    for i in range(1):
        page.goto(f"https://www.jumia.com.eg/catalog/?q=samsung&page={i}#catalog-listing")
        page.wait_for_timeout(1000)
        page.wait_for_selector("#fi-q", state="visible")
        
        page.fill("#fi-q", "samsung")
        page.press("#fi-q", "Enter")
        page.wait_for_timeout(3000)
        names = page.locator("h3.name").all_inner_texts()[:10]
        titles.extend(names)
        price = page.locator("div.prc").all_inner_texts()[:10]
        prices.extend(price)
    def to_dollar(x):
        for dollar in x:
            clean_price = dollar.replace("EGP", "")
            clean_price = clean_price.replace(",", "")
            usd_price = float(clean_price) / 50
            dollar_price.append(f"{usd_price:.2f}$")
            

    


    browser.close()



#pandas
data = {
    "Product":titles,
    "Price":prices
}
df = pd.DataFrame(data)
df.to_excel(r"07_jumia\samsung_phones.xlsx", index=False)
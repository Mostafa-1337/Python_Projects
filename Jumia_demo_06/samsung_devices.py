from playwright.sync_api import sync_playwright
import pandas as pd
from openpyxl import Workbook,load_workbook
from openpyxl.styles import Font,Border,PatternFill,Alignment,Side


def style_sheet(ws):
    back_fill = PatternFill(fill_type="solid",fgColor="1A1C1E")
    header_fill = PatternFill(fill_type="solid",fgColor="111315")
    white_font_header = Font(name="SF Pro",size=14, bold=True, color="F0F4F8")
    white_font = Font(name="SF Pro",size=12, bold=True, color="C4C7C5")
    white_border = Border(
        right=Side(color="2D3135",style="thin"),
        bottom=Side(color="2D3135",style="thin")
    )
    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = white_font_header
        cell.border = white_border
    for i in range(2,ws.max_row + 1):
        for col in ["A","B","C","D"]:
            cell = ws[f"{col}{i}"]
            cell.fill = back_fill
            cell.font = white_font
            cell.border = white_border
    for column in ws.columns:
        max_length = 0
        for cell in column:
            if len(str(cell.value)) > max_length:
                max_length = len(str(cell.value))
        ws.column_dimensions[column[0].column_letter].width = min(max_length + 2,50)



titles = []
prices_after = []
prices_before = []
dollar_price = []
discount = []

search = input("Enter What do you need: ")
start_price = input("Start Price: ")
end_price = input("End Price: ")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    page.goto(f"https://www.jumia.com.eg/catalog/?q={search}&price={start_price}-{end_price}#catalog-listing")


    #get title
    names = page.locator("h3.name").all_inner_texts()[:10]
    titles.extend(names)

    #get price before
    price_b = page.locator("div.prc").all_inner_texts()[:10]
    prices_after.extend(price_b)


    #get price after
    price_a = page.locator("div.old").all_inner_texts()[:10]
    prices_before.extend(price_a)

    #get Offer
    get_offer = page.locator("div.s-prc-w").all()
    for off in get_offer[:10]:
        discounts = off.locator(".bdg._dsct._sm").text_content()
        discount.append(discounts)

        
    
    #dollar price
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
    "Price before Discount":prices_before,
    "Discount":discount,
    "Price after Discount":prices_after,
}

df = pd.DataFrame(data)
df.to_excel(r"07_jumia\samsung_phones.xlsx", index=False)
wb = load_workbook(r"07_jumia\samsung_phones.xlsx")
ws = wb.active
style_sheet(ws)
wb.save(r"07_jumia\samsung_phones.xlsx")
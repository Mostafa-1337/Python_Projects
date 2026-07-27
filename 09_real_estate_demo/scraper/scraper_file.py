from playwright.async_api import async_playwright
import asyncio
import re

semaphore = asyncio.Semaphore(2)

urls = []
locations_and_titles = []
total_prices = []
areas = []
num_of_rooms = []
num_of_bathrooms = []
payments_type = []
finish_type = []
meter_prices = []
property_urls = []



async def scrape_book(browser, url):
    async with semaphore:
        page = await browser.new_page()

        try:
            await page.goto(url)
            location_and_title = await page.locator("p.break-words").first.inner_text()
            #pay type
            page_content = await page.locator("main").inner_text()
            if "تقسيط" in page_content:
                payment_type = "متاح تقسيط"
            else:
                payment_type = "كاش"
            payments_type.append(payment_type)

            total_price_el = await page.locator("div.items-center data").all()
            #price
            for total in total_price_el:
                total_price =  int(await total.get_attribute("value"))
                total_prices.append(total_price)



            area = await page.locator("div[class*='flex gap-0.5x md:gap-x-3x flex-wrap']").all()
            for cards in area:
                try:
                    #area
                    card_a = await cards.locator("div[class*='text-gray__dark_2 flex items-center flex-[49%] md:flex-none gap-x-x flex-row']").nth(0).locator("p").inner_text()
                    clean_area = int(re.sub(r"[^\d]", "", card_a))
                    areas.append(clean_area)
                except:
                    areas.append("N/A")


                try:
                    #num of rooms
                    card_b = await cards.locator("div[class*='text-gray__dark_2 flex items-center flex-[49%] md:flex-none gap-x-x flex-row']").nth(1).locator("p").inner_text()
                    clean_rooms = re.sub(r"[^\d]", "", card_b)
                    num_of_rooms.append(int(clean_rooms))
                except:
                    num_of_rooms.append("N/A")


                try:
                    #num of bathrooms
                    card_c = await cards.locator("div[class*='text-gray__dark_2 flex items-center flex-[49%] md:flex-none gap-x-x flex-row']").nth(2).locator("p").inner_text()
                    clean_bathrooms = re.sub(r"[^\d]", "", card_c)
                    num_of_bathrooms.append(int(clean_bathrooms))
                except:
                    num_of_bathrooms.append("N/A")

                try:
                    #finish type
                    card_d = await cards.locator("div[class*='text-gray__dark_2 flex items-center flex-[49%] md:flex-none gap-x-x flex-row']").nth(3).locator("p").inner_text()
                    finish_type.append(card_d)
                except:
                    finish_type.append("N/A")

            



            #to-list
            locations_and_titles.append(location_and_title)
            property_urls.append(url)

            #meter price
            meter_price = round(total_price / clean_area, 2)
            meter_prices.append(meter_price)




        except Exception as e:
            print(f"Error:{url}, reason:{e}")


        finally:
            await page.close()



async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://aqarmap.com.eg/ar/for-sale/apartment")
        links_el = (await page.locator("a.flex-shrink-0").all())[:10]
        for link in links_el:
            links = await link.get_attribute("href")
            urls.append(f"https://aqarmap.com.eg{links}")


        await page.close()

        tasks = []
        for url in urls:
            task = scrape_book(browser, url)
            tasks.append(task)
        await asyncio.gather(*tasks)



        
        await browser.close()



        data = {
            "الاسم الرئيسي" : locations_and_titles,
            "السعر الاجمالي" : total_prices,
            "سعر المتر" : meter_prices,
            "المساحة" : areas,
            "عدد الغرف" : num_of_rooms,
            "عدد الحمامات" : num_of_bathrooms,
            "نوع التشطيب" : finish_type,
            "نظام الدفع" : payments_type,
            "رابط العقار" : property_urls
        }
    

        return data
    
    print("Done!")




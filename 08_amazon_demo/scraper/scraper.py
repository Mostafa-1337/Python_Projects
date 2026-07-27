from playwright.async_api import async_playwright
import asyncio

semaphore = asyncio.Semaphore(3)

#lists
urls = []
titles = []
prices_b = []
discounts = []
prices_a = []
availability = []
ratings = []
review_counts = []
img_url = []




async def scrape_book(browser, url):
    async with semaphore:
        page = await browser.new_page()

        try:
            await page.goto(url)
            title = await page.locator("span.a-size-large.product-title-word-break").first.inner_text()
            price_a = await page.locator("span.a-price-whole").first.inner_text()
            price_b = await page.locator("span.a-offscreen").first.inner_text()
            av = await page.locator("#availability span").inner_text()
            rating = await page.locator("span.a-size-small.a-color-base").first.inner_text()
            review_count = await page.locator("#acrCustomerReviewText").first.inner_text()
            img_el = await page.locator("#landingImage").all()
            for img in img_el:
                imgs = await img.get_attribute("src")
                img_url.append(imgs)



            try:
                discount = await page.locator("span.apex-savings-container span").first.inner_text(timeout=500)
                clean_discount = discount.replace("-", "").strip()
                discounts.append(clean_discount)
            except:
                discounts.append("Non")

            #clean prices
            clean_price_a = price_a.replace("\n", "").replace(".", "").strip()
            clean_price_b = price_b.replace("EGP", "")
            clean_count = review_count.replace("(", "").replace(")", "").strip()

            #to-list
            titles.append(title)
            prices_a.append(f"EGP {clean_price_a}")
            prices_b.append(f"EGP {clean_price_b}")
            availability.append(av)
            ratings.append(f"{rating} out of 5")
            review_counts.append(clean_count)


        except Exception as e:
            print(f"Error:{url}, reason:{e}")


        finally:
            await page.close()



async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.amazon.eg/s?k=iphone&language=en_AE&crid=26SVEFHUGPNEJ&sprefix=sams%2Caps%2C141&ref=nb_sb_ss_mvt-t11-ranker_2_4")
        links_el = (await page.locator("a.a-link-normal.s-no-outline").all())[:10]
        for link in links_el:
            links = await link.get_attribute("href")
            urls.append(f"https://www.amazon.eg{links}")

        await page.close()

        tasks = []
        for url in urls:
            task = scrape_book(browser, url)
            tasks.append(task)
        await asyncio.gather(*tasks)



        
        await browser.close()


        data = {
            "Product" : titles,
            "Price" : prices_b,
            "Discount" : discounts,
            "Price after discount" : prices_a,
            "Availability" : availability,
            "Rating" : ratings,
            "Review Counts" : review_counts,
            "Product url" : urls,
            "Image url" : img_url
        }

        return data


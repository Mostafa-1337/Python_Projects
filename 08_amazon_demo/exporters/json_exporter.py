import json
def save_to_json(data, filename='10_amazon/data/Products.json'):
    formatted_data = []

    for titles, prices_b, discounts, prices_a, availability, ratings, review_counts, urls, img_url in zip(data["Product"], data["Price"], data["Discount"], data["Price after discount"], data["Availability"], data["Rating"], data["Review Counts"], data["Product url"], data["Image url"]):
        formatted_data.append({
            "Product" : titles,
            "Price" : prices_b,
            "Discount" : discounts,
            "Price after discount" : prices_a,
            "Availability" : availability,
            "Rating" : ratings,
            "Review Counts" : review_counts,
            "Product url" : urls,
            "Image url" : img_url
        })

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(formatted_data, f, ensure_ascii=False, indent=4)
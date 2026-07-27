import json
def save_to_json(data, filename='11_real_estate/data/Real_Estate_data.json'):
    formatted_data = []

    for locations_and_titles, total_prices, meter_prices, areas, num_of_rooms, num_of_bathrooms, finish_type, payments_type, property_urls in zip(data["الاسم الرئيسي"], data["السعر الاجمالي"], data["سعر المتر"], data["المساحة"], data["عدد الغرف"], data["عدد الحمامات"], data["نوع التشطيب"], data["نظام الدفع"], data["رابط العقار"]):
        formatted_data.append({
            "الاسم الرئيسي" : locations_and_titles,
            "السعر الاجمالي" : total_prices,
            "سعر المتر" : meter_prices,
            "المساحة" : areas,
            "عدد الغرف" : num_of_rooms,
            "عدد الحمامات" : num_of_bathrooms,
            "نوع التشطيب" : finish_type,
            "نظام الدفع" : payments_type,
            "رابط العقار" : property_urls
        })

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(formatted_data, f, ensure_ascii=False, indent=4)
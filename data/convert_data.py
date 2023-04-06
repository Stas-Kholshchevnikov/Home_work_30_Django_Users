import csv
import json


def convert(csv_file, json_file, model):
    result = []
    with open(csv_file, encoding="utf-8") as file_csv:
        for row in csv.DictReader(file_csv):
            del row["id"]
            if "price" in row:
                row["price"] = int(row["price"])
            if "is_published" in row:
                row["is_published"] = bool(row["is_published"].title())

            if "location_id" in row:
                row["location"] = [row["location_id"]]
                del row["location_id"]

            result.append({"model": model, "fields": row})

    with open(json_file, "w", encoding="utf-8") as file_json:
        file_json.write(json.dumps(result, ensure_ascii=False))


convert("data_hw_28/category.csv", "data_hw_28/category.json", "ads.Category")
convert("data_hw_28/ad.csv", "data_hw_28/ad.json", "ads.Ad")

convert("data_hw_28/location.csv", "data_hw_28/location.json", "users.Location")
convert("data_hw_28/user.csv", "data_hw_28/user.json", "users.User")

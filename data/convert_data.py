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

            result.append({"model": model, "fields": row})

    with open(json_file, "w", encoding="utf-8") as file_json:
        file_json.write(json.dumps(result, ensure_ascii=False))


convert("categories.csv", "categories.json", "ads.Category")
convert("ads.csv", "ads.json", "ads.Ad")

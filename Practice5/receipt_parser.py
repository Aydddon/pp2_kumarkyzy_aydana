import re
import json

# Read data from raw.txt
with open("raw.txt", "r", encoding="utf-8") as file:
    text = file.read()


# 1. Find product names
product_pattern = r"\d+\.\n(.+)"
products = re.findall(product_pattern, text)


# 2. Find quantities
quantity_pattern = r"\n(\d+,\d{3}) x"
quantities = re.findall(quantity_pattern, text)


# 3. Find unit prices
price_pattern = r"x\s*([\d ]+,\d{2})"
unit_prices = re.findall(price_pattern, text)


# 4. Find total price of each product
item_total_pattern = r"\n([\d ]+,\d{2})\nСтоимость"
item_totals = re.findall(item_total_pattern, text)


# 5. Find total amount
total_pattern = r"ИТОГО:\s*\n([\d ]+,\d{2})"
total_match = re.search(total_pattern, text)

if total_match:
    total = total_match.group(1)
else:
    total = "Not found"


# 6. Find date and time
datetime_pattern = r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})"
datetime_match = re.search(datetime_pattern, text)

if datetime_match:
    date = datetime_match.group(1)
    time = datetime_match.group(2)
else:
    date = "Not found"
    time = "Not found"


# 7. Find payment method
payment_pattern = r"(Банковская карта):\s*\n([\d ]+,\d{2})"
payment_match = re.search(payment_pattern, text)

if payment_match:
    payment_method = payment_match.group(1)
    payment_amount = payment_match.group(2)
else:
    payment_method = "Not found"
    payment_amount = "Not found"


# 8. Create structured output
receipt = {
    "products": products,
    "quantities": quantities,
    "unit_prices": unit_prices,
    "item_totals": item_totals,
    "total": total,
    "date": date,
    "time": time,
    "payment_method": payment_method,
    "payment_amount": payment_amount
}


# 9. Print the result
print(json.dumps(receipt, ensure_ascii=False, indent=4))
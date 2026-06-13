import os
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")


def clean_text(text):
    return str(text).lower().strip()


def extract_store_price(query):

    params = {
        "engine": "google_shopping",
        "q": query,
        "api_key": SERPAPI_API_KEY,
        "gl": "in",
        "hl": "en"
    }

    try:

        search = GoogleSearch(params)
        results = search.get_dict()

        shopping_results = results.get(
            "shopping_results",
            []
        )

        if not shopping_results:
            return "Not Found"

        for item in shopping_results:

            title = clean_text(
                item.get("title", "")
            )

            price = item.get(
                "price",
                "Not Found"
            )

            if price != "Not Found":
                return price

        return "Not Found"

    except Exception as e:

        print("STORE SEARCH ERROR:", e)

        return "Not Found"


def get_official_query(phone_name):

    phone = phone_name.lower()

    if "iphone" in phone:
        return f"{phone_name} Apple India"

    elif "samsung" in phone or "galaxy" in phone:
        return f"{phone_name} Samsung India"

    elif "pixel" in phone:
        return f"{phone_name} Google Store India"

    elif "oneplus" in phone:
        return f"{phone_name} OnePlus India"

    elif "nothing" in phone:
        return f"{phone_name} Nothing India"

    elif "vivo" in phone:
        return f"{phone_name} Vivo India"

    elif "oppo" in phone:
        return f"{phone_name} Oppo India"

    elif "realme" in phone:
        return f"{phone_name} Realme India"

    elif "xiaomi" in phone:
        return f"{phone_name} Xiaomi India"

    elif "motorola" in phone:
        return f"{phone_name} Motorola India"

    return f"{phone_name} Official Store"


def convert_price(price):

    try:

        return int(
            str(price)
            .replace("₹", "")
            .replace(",", "")
            .strip()
        )

    except:
        return 999999999


def search_product(phone_name):

    print("\nSearching Amazon...")
    amazon_price = extract_store_price(
        f"{phone_name} Amazon India"
    )

    print("Searching Flipkart...")
    flipkart_price = extract_store_price(
        f"{phone_name} Flipkart"
    )

    print("Searching Official Store...")
    official_price = extract_store_price(
        get_official_query(phone_name)
    )

    prices = {
        "Amazon": amazon_price,
        "Flipkart": flipkart_price,
        "Official Store": official_price
    }

    valid_prices = {}

    for store, price in prices.items():

        if price != "Not Found":

            valid_prices[store] = convert_price(
                price
            )

    if valid_prices:

        cheapest_store = min(
            valid_prices,
            key=valid_prices.get
        )

    else:

        cheapest_store = "Unknown"

    return {

        "Amazon": amazon_price,

        "Flipkart": flipkart_price,

        "Official Store": official_price,

        "cheapest_store": cheapest_store,

        "best_store": "Amazon",

        "delivery": "Amazon usually delivers faster"
    }
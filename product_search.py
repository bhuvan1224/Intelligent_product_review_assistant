import os
from serpapi import GoogleSearch
from dotenv import load_dotenv
import re

load_dotenv()

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")


def convert_price(price):

    try:

        # Normalize to string and extract numeric portion (handles different formats)
        price_str = str(price)

        # Try to find the first run of digits and commas (e.g. '79,000')
        m = re.search(r"(\d[\d,]*)", price_str.replace('₹',''))
        if not m:
            # fallback: remove non-digits and try
            digits = re.sub(r"[^0-9]", "", price_str)
            if not digits:
                raise ValueError("no digits in price")
            return int(digits)

        numeric = m.group(1).replace(",", "")
        return int(numeric)

    except Exception:
        # Return a very large sentinel so that invalid/unknown prices are ignored
        return 999999999


def extract_store_data(query):

    if not SERPAPI_API_KEY:
        print("SERPAPI_API_KEY not set; shopping results will be unavailable.")
        return {
            "price": "Not Found",
            "link": ""
        }

    params = {
        "engine": "google_shopping",
        "q": query,
        "api_key": SERPAPI_API_KEY,
        "gl": "in",
        "hl": "en"
    }

    blocked_words = [
        "case",
        "cover",
        "protector",
        "screen guard",
        "tempered",
        "charger",
        "adapter",
        "cable",
        "skin",
        "back cover",
        "earbuds",
        "watch",
        "strap"
    ]

    try:

        print(f"STORE QUERY: {query}")
        search = GoogleSearch(params)

        results = search.get_dict()

        shopping_results = results.get(
            "shopping_results",
            []
        )
        print("\nQUERY:", query)

        for item in shopping_results[:5]:
            print(
                item.get("title", ""),
                "->",
                item.get("price", "")
            )

        print(f"Found {len(shopping_results)} shopping results")

        if not shopping_results:

            return {
                "price": "Not Found",
                "link": ""
            }

        # Iterate results and find the first plausible product (price >= 10,000 INR)
        for idx, item in enumerate(shopping_results[:10]):

            title = item.get(
                "title",
                ""
            ).lower()

            price = item.get(
                "price",
                "Not Found"
            )

            # debug log first few items
            if idx < 3:
                print("  candidate:", title[:120], "| price:", price)

            if any(
                word in title
                for word in blocked_words
            ):
                # skip accessories
                continue

            if price == "Not Found":
                continue

            price_value = convert_price(
                price
            )

            # Ignore fake accessory prices or obviously too low values
            if price_value < 10000:
                print(f"  ignored price (too low): {price} -> {price_value}")
                continue

            link = item.get(
                "product_link",
                item.get(
                    "link",
                    ""
                )
            )

            # Return a consistent string with currency symbol
            return {
                "price": f"₹{price_value}",
                "link": link
            }

        # nothing matched
        return {
            "price": "Not Found",
            "link": ""
        }

    except Exception as e:

        print(
            "STORE SEARCH ERROR:",
            e
        )

        return {
            "price": "Not Found",
            "link": ""
        }


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


def search_product(phone_name):

    print("\nSearching Amazon...")

    amazon = extract_store_data(
        f"{phone_name} Amazon India"
    )

    print("Searching Flipkart...")

    flipkart = extract_store_data(
        f"{phone_name} Flipkart"
    )

    print("Searching Official Store...")

    official = extract_store_data(
        get_official_query(phone_name)
    )

    prices = {

        "Amazon": amazon["price"],

        "Flipkart": flipkart["price"],

        "Official Store": official["price"]
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

        "Amazon": amazon["price"],

        "Flipkart": flipkart["price"],

        "Official Store": official["price"],

        "amazon_link": amazon["link"],

        "flipkart_link": flipkart["link"],

        "official_link": official["link"],

        "cheapest_store": cheapest_store,

        "best_store": "Amazon",

        "delivery": "Amazon usually delivers faster"
    }
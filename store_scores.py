def get_store_scores():

    return {

        "Amazon": {
            "rating": 4.6,
            "delivery": "Fast",
            "returns": "Easy",
            "trust": 9.5
        },

        "Flipkart": {
            "rating": 4.4,
            "delivery": "Fast",
            "returns": "Good",
            "trust": 9.0
        },

        "Official Store": {
            "rating": 4.8,
            "delivery": "Medium",
            "returns": "Excellent",
            "trust": 10.0
        }
    }


def best_store():

    stores = get_store_scores()

    best = max(
        stores,
        key=lambda x: stores[x]["trust"]
    )

    return best
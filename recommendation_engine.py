PHONE_DATABASE = [

    {
        "name": "Redmi Note 14",
        "price": 14999,
        "camera": 80,
        "battery": 90,
        "gaming": 75,
        "display": 78,
        "storage": 128
    },

    {
        "name": "Realme GT 6",
        "price": 34999,
        "camera": 85,
        "battery": 88,
        "gaming": 92,
        "display": 90,
        "storage": 256
    },

    {
        "name": "Nothing Phone 3",
        "price": 39999,
        "camera": 88,
        "battery": 87,
        "gaming": 85,
        "display": 92,
        "storage": 256
    },

    {
        "name": "Google Pixel 9",
        "price": 74999,
        "camera": 99,
        "battery": 84,
        "gaming": 80,
        "display": 90,
        "storage": 256
    },

    {
        "name": "OnePlus 13",
        "price": 69999,
        "camera": 91,
        "battery": 98,
        "gaming": 97,
        "display": 92,
        "storage": 512
    },

    {
        "name": "Samsung Galaxy S25",
        "price": 84999,
        "camera": 93,
        "battery": 90,
        "gaming": 90,
        "display": 95,
        "storage": 256
    },

    {
        "name": "Samsung Galaxy S25 Ultra",
        "price": 129999,
        "camera": 98,
        "battery": 93,
        "gaming": 95,
        "display": 99,
        "storage": 512
    }
]


def recommend_alternative(
    phone,
    budget,
    priority
):

    filtered = [
        p for p in PHONE_DATABASE
        if p["price"] <= budget
    ]

    if not filtered:

        return {
            "name": "No phone found",
            "price": "N/A",
            "comparison": []
        }

    feature_map = {

        "Camera": "camera",
        "Battery": "battery",
        "Gaming": "gaming",
        "Display": "display",
        "Storage": "storage",
        "Value": "price"
    }

    feature = feature_map[priority]

    if priority == "Value":

        best_phone = min(
            filtered,
            key=lambda x: x["price"]
        )

    else:

        best_phone = max(
            filtered,
            key=lambda x: x[feature]
        )

    return {

        "name": best_phone["name"],

        "price": f"₹{best_phone['price']:,}",

        "comparison": [

            {
                "Feature": "Camera",
                "Score": best_phone["camera"]
            },

            {
                "Feature": "Battery",
                "Score": best_phone["battery"]
            },

            {
                "Feature": "Gaming",
                "Score": best_phone["gaming"]
            },

            {
                "Feature": "Display",
                "Score": best_phone["display"]
            },

            {
                "Feature": "Storage",
                "Score": best_phone["storage"]
            }
        ]
    }
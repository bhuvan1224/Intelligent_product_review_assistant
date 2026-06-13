PHONE_DATABASE = {

    "Apple": [
        "iPhone 16 Pro Max",
        "iPhone 16 Pro",
        "iPhone 16 Plus",
        "iPhone 16",
        "iPhone 15 Pro Max",
        "iPhone 15 Pro",
        "iPhone 15 Plus",
        "iPhone 15",
        "iPhone 14 Pro Max",
        "iPhone 14 Pro",
        "iPhone 14 Plus",
        "iPhone 14"
    ],

    "Samsung": [
        "Samsung Galaxy S25 Ultra",
        "Samsung Galaxy S25 Plus",
        "Samsung Galaxy S25",
        "Samsung Galaxy S24 Ultra",
        "Samsung Galaxy S24 Plus",
        "Samsung Galaxy S24",
        "Samsung Galaxy A56",
        "Samsung Galaxy A36"
    ],

    "Google": [
        "Google Pixel 9 Pro XL",
        "Google Pixel 9 Pro",
        "Google Pixel 9",
        "Google Pixel 8 Pro",
        "Google Pixel 8"
    ],

    "OnePlus": [
        "OnePlus 13",
        "OnePlus 13R",
        "OnePlus 12",
        "OnePlus 12R"
    ],

    "Nothing": [
        "Nothing Phone 3",
        "Nothing Phone 2",
        "Nothing Phone 2a"
    ],

    "Vivo": [
        "Vivo X200 Pro",
        "Vivo X100 Pro",
        "Vivo V50"
    ],

    "Oppo": [
        "Oppo Find X8 Pro",
        "Oppo Reno 13 Pro"
    ],

    "Realme": [
        "Realme GT 7 Pro",
        "Realme GT 6"
    ],

    "Xiaomi": [
        "Xiaomi 15 Ultra",
        "Xiaomi 14 Ultra"
    ],

    "Motorola": [
        "Motorola Edge 60 Pro",
        "Motorola Edge 50 Ultra"
    ]
}


def get_brand_models(brand):
    return PHONE_DATABASE.get(brand, [])
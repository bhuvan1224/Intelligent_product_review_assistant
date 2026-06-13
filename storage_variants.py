STORAGE_VARIANTS = {

    "iPhone 16 Pro Max": [
        "256GB",
        "512GB",
        "1TB"
    ],

    "iPhone 16 Pro": [
        "128GB",
        "256GB",
        "512GB",
        "1TB"
    ],

    "Samsung Galaxy S25 Ultra": [
        "256GB",
        "512GB",
        "1TB"
    ],

    "Google Pixel 9": [
        "128GB",
        "256GB"
    ],

    "OnePlus 13": [
        "256GB",
        "512GB"
    ]
}


def get_storage_variants(phone):

    return STORAGE_VARIANTS.get(
        phone,
        ["128GB", "256GB"]
    )
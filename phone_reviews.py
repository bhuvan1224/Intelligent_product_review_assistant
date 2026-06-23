PHONE_REVIEWS = {

    "iPhone 16 Pro Max": [

        "The camera quality is outstanding, especially in low light conditions.",
        "Battery easily lasts a full day even with heavy usage.",
        "Video recording quality is exceptional.",
        "The display is bright, sharp and vibrant.",
        "Performance is extremely smooth with no lag.",
        "The phone feels premium and well built.",
        "Face ID works quickly and accurately.",
        "Charging speed could be faster for the price.",
        "The device is expensive but delivers a flagship experience.",
        "Gaming performance is excellent."
    ],

    "iPhone 16 Pro": [

        "Compact design makes it comfortable to use.",
        "Camera quality is excellent for photos and videos.",
        "Performance is incredibly fast.",
        "Battery life is reliable throughout the day.",
        "Display quality is impressive.",
        "Build quality feels premium.",
        "Face ID is fast and convenient.",
        "Charging speed could be improved.",
        "The phone is expensive compared to competitors.",
        "Software experience is smooth."
    ],

    "Samsung Galaxy S25 Ultra": [

        "The display is one of the best available.",
        "Zoom camera performance is outstanding.",
        "Battery life easily lasts a full day.",
        "The S Pen is useful for productivity tasks.",
        "Gaming performance is smooth and responsive.",
        "Camera versatility is excellent.",
        "The device feels premium and durable.",
        "Charging speed is good.",
        "The phone is slightly heavy.",
        "The large display is great for multimedia."
    ],

    "Google Pixel 9": [

        "Photos look natural and highly detailed.",
        "AI features are genuinely useful.",
        "Android experience feels clean and smooth.",
        "Camera quality is excellent.",
        "Battery life is decent but not exceptional.",
        "Software updates are a major advantage.",
        "Display quality is good.",
        "Performance is smooth for daily tasks.",
        "Charging speed could be better.",
        "The phone feels lightweight and comfortable."
    ],

    "OnePlus 13": [

        "Performance is incredibly fast.",
        "Battery backup is fantastic.",
        "Fast charging is one of the biggest strengths.",
        "Gaming performance is excellent.",
        "Display quality is top notch.",
        "Software feels smooth and responsive.",
        "The phone offers great value for money.",
        "Camera quality is good but not class leading.",
        "Build quality is premium.",
        "The device stays cool during most tasks."
    ],

    "Nothing Phone 3": [

        "The transparent design looks unique.",
        "Glyph lighting features are useful and fun.",
        "Battery life is good.",
        "Display quality is impressive.",
        "Performance is smooth in daily usage.",
        "Software experience feels clean and minimal.",
        "Camera quality is decent.",
        "The phone offers excellent value for money.",
        "Build quality feels solid.",
        "Users appreciate the unique design language."
    ],

    "Samsung Galaxy S25": [

        "Display quality is excellent.",
        "Battery life is reliable.",
        "Performance is smooth and responsive.",
        "Camera quality is very good.",
        "The phone is compact and comfortable.",
        "Software experience is polished.",
        "Build quality feels premium.",
        "Charging speed is decent.",
        "Speakers are loud and clear.",
        "Overall user experience is excellent."
    ],

    "iQOO 13": [

        "Gaming performance is outstanding.",
        "Battery backup is impressive.",
        "Fast charging is extremely useful.",
        "Display refresh rate feels very smooth.",
        "The phone handles heavy games easily.",
        "Performance is flagship level.",
        "Camera quality is acceptable.",
        "The device offers excellent value.",
        "Thermal management is good.",
        "Users love the gaming experience."
    ]
}


def get_reviews(phone_name):

    return PHONE_REVIEWS.get(
        phone_name,
        [
            "Good performance for daily use.",
            "Battery life is decent.",
            "Display quality is good.",
            "Overall value for money product.",
            "Camera performance is satisfactory."
        ]
    )
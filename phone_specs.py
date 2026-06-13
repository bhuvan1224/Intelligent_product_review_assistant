def get_phone_specs(phone_name):

    phone_name = phone_name.lower()

    if "iphone" in phone_name:

        return {

            "features": [
                "A18 Pro Chip",
                "48MP Camera",
                "Super Retina XDR Display",
                "5G Connectivity",
                "Face ID"
            ],

            "pros": [
                "Excellent Camera",
                "Premium Build",
                "Industry Leading Performance"
            ],

            "cons": [
                "Expensive",
                "Slow Charging"
            ]
        }

    elif "samsung" in phone_name or "galaxy" in phone_name:

        return {

            "features": [
                "Dynamic AMOLED Display",
                "Snapdragon Processor",
                "200MP Camera",
                "5000mAh Battery",
                "5G Connectivity"
            ],

            "pros": [
                "Excellent Display",
                "Strong Camera",
                "Good Battery"
            ],

            "cons": [
                "Premium Price",
                "Large Size"
            ]
        }

    elif "pixel" in phone_name:

        return {

            "features": [
                "Google Tensor Chip",
                "AI Camera Features",
                "OLED Display",
                "5G",
                "Android Updates"
            ],

            "pros": [
                "Best Camera",
                "Clean Android",
                "AI Features"
            ],

            "cons": [
                "Average Gaming",
                "Charging Could Be Faster"
            ]
        }

    return {

        "features": [
            "5G Connectivity",
            "AMOLED Display",
            "Fast Charging",
            "High Performance Processor",
            "Multi Camera Setup"
        ],

        "pros": [
            "Good Performance",
            "Modern Features",
            "Value For Money"
        ],

        "cons": [
            "Average Low Light Camera",
            "Software Updates Limited"
        ]
    }
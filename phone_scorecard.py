def generate_scorecard(
    preference
):

    scores = {

        "Camera": 8,

        "Gaming": 8,

        "Battery": 8,

        "Display": 8,

        "Value": 8
    }

    if preference == "camera":

        scores["Camera"] = 10

    elif preference == "gaming":

        scores["Gaming"] = 10

    elif preference == "battery":

        scores["Battery"] = 10

    elif preference == "overall":

        scores = {

            "Camera": 9,

            "Gaming": 9,

            "Battery": 9,

            "Display": 9,

            "Value": 9
        }

    return scores
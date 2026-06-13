import pandas as pd
import plotly.express as px


def generate_scores(phone_name):

    phone = phone_name.lower()

    camera = 85
    battery = 85
    display = 85
    gaming = 85
    value = 85

    if "pro max" in phone:
        camera += 10
        display += 10
        gaming += 10

    elif "pro" in phone:
        camera += 8
        display += 8

    elif "ultra" in phone:
        camera += 10
        battery += 10
        display += 10

    elif "pixel" in phone:
        camera += 12
        value += 5

    elif "oneplus" in phone:
        gaming += 10
        battery += 5

    elif "nothing" in phone:
        value += 10

    elif "realme" in phone:
        value += 8
        gaming += 5

    elif "vivo" in phone:
        camera += 8

    elif "oppo" in phone:
        camera += 6

    return {
        "Camera": camera,
        "Battery": battery,
        "Display": display,
        "Gaming": gaming,
        "Value": value
    }


def comparison_table(phone1, phone2):

    scores1 = generate_scores(phone1)
    scores2 = generate_scores(phone2)

    rows = []

    for feature in scores1.keys():

        if scores1[feature] > scores2[feature]:
            winner = phone1

        elif scores2[feature] > scores1[feature]:
            winner = phone2

        else:
            winner = "Tie"

        rows.append(
            [
                feature,
                scores1[feature],
                scores2[feature],
                winner
            ]
        )

    return pd.DataFrame(
        rows,
        columns=[
            "Feature",
            phone1,
            phone2,
            "Winner"
        ]
    )


def score_chart(phone1, phone2):

    scores1 = generate_scores(phone1)
    scores2 = generate_scores(phone2)

    df = pd.DataFrame({
        "Feature": list(scores1.keys()),
        phone1: list(scores1.values()),
        phone2: list(scores2.values())
    })

    chart_df = df.melt(
        id_vars="Feature",
        var_name="Phone",
        value_name="Score"
    )

    fig = px.bar(
        chart_df,
        x="Feature",
        y="Score",
        color="Phone",
        barmode="group",
        title="Feature Comparison"
    )

    return fig


def overall_score(phone1, phone2):

    s1 = generate_scores(phone1)
    s2 = generate_scores(phone2)

    score1 = round(
        sum(s1.values()) / len(s1)
    )

    score2 = round(
        sum(s2.values()) / len(s2)
    )

    return score1, score2
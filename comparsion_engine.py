from phone_database import PHONE_SCORES
import pandas as pd


def compare_phones(phone1, phone2):

    p1 = PHONE_SCORES.get(phone1)
    p2 = PHONE_SCORES.get(phone2)

    if not p1 or not p2:
        return None

    rows = []

    for feature in p1:

        rows.append({

            "Feature": feature,

            phone1: p1[feature],

            phone2: p2[feature]
        })

    return pd.DataFrame(rows)


def overall_score(phone):

    scores = PHONE_SCORES.get(phone)

    if not scores:
        return 0

    return round(
        sum(scores.values()) /
        len(scores),
        1
    )
from utils import extract_price


def recommend_best_phone(
    shopping_data,
    budget,
    preference
):

    valid = []

    for item in shopping_data:

        price = extract_price(
            item.get("price")
        )

        if (
            price and
            price <= budget
        ):

            score = 0

            rating = float(
                item.get("rating", 0)
            )

            score += rating * 10

            if preference == "overall":
                score += 20

            elif preference == "camera":
                score += 15

            elif preference == "gaming":
                score += 15

            elif preference == "battery":
                score += 15

            item["score"] = score

            valid.append(item)

    if not valid:
        return None

    valid.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return valid[0]
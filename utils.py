import re


def extract_price(text):

    try:

        value = re.sub(
            r"[^\d]",
            "",
            str(text)
        )

        return int(value)

    except:

        return None
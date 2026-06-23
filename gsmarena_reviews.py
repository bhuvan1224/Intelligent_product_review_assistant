import requests
from bs4 import BeautifulSoup


def get_reviews(phone_name):

    try:

        search_url = (
            f"https://www.gsmarena.com/results.php3?sQuickSearch=yes&sName={phone_name}"
        )

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            search_url,
            headers=headers,
            timeout=15
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        phone_link = soup.select_one(
            ".makers ul li a"
        )

        if not phone_link:

            print("Phone not found")

            return []

        phone_url = (
            "https://www.gsmarena.com/"
            + phone_link["href"]
        )

        print("Phone URL:", phone_url)

        response = requests.get(
            phone_url,
            headers=headers,
            timeout=15
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        reviews = []

        comments = soup.find_all(
            "p"
        )

        for comment in comments:

            text = comment.get_text(
                strip=True
            )

            if len(text) > 40:

                reviews.append(text)

        return reviews[:50]

    except Exception as e:

        print("ERROR:", e)

        return []
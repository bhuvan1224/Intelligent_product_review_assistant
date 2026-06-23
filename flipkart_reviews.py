import os
from dotenv import load_dotenv
from apify_client import ApifyClient

load_dotenv()

client = ApifyClient(
    os.getenv("APIFY_API_TOKEN")
)


def get_flipkart_reviews(product_url):

    reviews = []

    try:

        actor = client.actor(
            "runtime/flipkart-reviews-scraper"
        )

        run_input = {
            "startUrls": [
                {
                    "url": product_url
                }
            ]
        }

        run = actor.call(
            run_input=run_input
        )

        dataset = client.dataset(
            run["defaultDatasetId"]
        )

        for item in dataset.iterate_items():

            text = item.get(
                "review",
                ""
            )

            if text:
                reviews.append(text)

        return reviews

    except Exception as e:

        print(
            "Flipkart Review Error:",
            e
        )

        return []
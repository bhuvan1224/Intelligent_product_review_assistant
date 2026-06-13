from playwright.sync_api import sync_playwright


def get_amazon_price(phone_name):

    try:
        with sync_playwright() as p:

            browser = p.chromium.launch(headless=True)

            page = browser.new_page()

            search_url = (
                f"https://www.amazon.in/s?k={phone_name}"
            )

            page.goto(search_url, timeout=60000)

            page.wait_for_timeout(3000)

            price = page.locator(
                "span.a-price-whole"
            ).first.inner_text()

            browser.close()

            return f"₹{price}"

    except:
        return "Not Available"
from playwright.sync_api import sync_playwright


def get_flipkart_price(phone_name):

    try:
        with sync_playwright() as p:

            browser = p.chromium.launch(headless=True)

            page = browser.new_page()

            search_url = (
                f"https://www.flipkart.com/search?q={phone_name}"
            )

            page.goto(search_url, timeout=60000)

            page.wait_for_timeout(3000)

            price = page.locator(
                "div.Nx9bqj"
            ).first.inner_text()

            browser.close()

            return price

    except:
        return "Not Available"
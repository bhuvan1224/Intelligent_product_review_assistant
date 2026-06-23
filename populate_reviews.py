"""
Populate Chroma with reviews for phones in PHONE_DATABASE.

Usage:
  source .venv/bin/activate
  python populate_reviews.py --source gsmarena           # dry-run, shows counts
  python populate_reviews.py --source gsmarena --apply   # actually scrape and add reviews
  python populate_reviews.py --source gsmarena --apply --overwrite  # delete existing reviews for phone before adding

Supported sources: gsmarena (uses gsmarena_reviews.get_reviews)

Notes:
- Scraping many phones may be slow and rate-limited. Use --limit to cap reviews per phone.
- The script uses add_reviews(...) from review_vector_store, which appends by default. Use --overwrite to clear previous entries.
"""

import argparse
from gsmarena_scraper import PHONE_DATABASE

# import chosen scrapers and add_reviews
from review_vector_store import add_reviews


def scrape_gsmarena(phone, limit=None):
    from gsmarena_reviews import get_reviews
    reviews = get_reviews(phone)
    if limit:
        return reviews[:limit]
    return reviews


def main(source="gsmarena", apply=False, overwrite=False, limit=None):
    summary = {}
    for brand, phones in PHONE_DATABASE.items():
        for phone in phones:
            print(f"Processing: {phone} ({brand})")
            if source == "gsmarena":
                reviews = scrape_gsmarena(phone, limit=limit)
            else:
                print(f"Unknown source: {source}")
                reviews = []

            print(f"  Found {len(reviews)} reviews")

            if not reviews:
                summary[phone] = {"status": "no_reviews", "count": 0}
                continue

            if apply:
                added = add_reviews(phone, reviews, overwrite=overwrite)
                summary[phone] = {"status": "added" if added else "skipped", "count": added}
                print(f"  Added {added} reviews to Chroma (overwrite={overwrite})")
            else:
                summary[phone] = {"status": "dry_run", "count": len(reviews)}

    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="gsmarena", help="Review source: gsmarena")
    parser.add_argument("--apply", action="store_true", help="Actually add reviews to Chroma")
    parser.add_argument("--overwrite", action="store_true", help="When applying, overwrite existing reviews for each phone")
    parser.add_argument("--limit", type=int, default=None, help="Limit reviews per phone (for testing)")
    args = parser.parse_args()

    result = main(source=args.source, apply=args.apply, overwrite=args.overwrite, limit=args.limit)

    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))

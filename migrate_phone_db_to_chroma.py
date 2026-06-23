"""
Migrate phones from gsmarena_scraper.PHONE_DATABASE into the Chroma collection as metadata entries.

Usage:
  source .venv/bin/activate
  python migrate_phone_db_to_chroma.py         # dry-run: show what will be added
  python migrate_phone_db_to_chroma.py --apply # actually add entries
  python migrate_phone_db_to_chroma.py --apply --overwrite # delete existing entries per phone and re-add metadata

What it does:
- For each brand and phone in PHONE_DATABASE it checks whether Chroma already has any entries for that phone.
- If none found (or --overwrite), it adds a lightweight metadata entry for the phone with keys: phone, brand, features, pros, cons.
- The metadata entry contains a short document (the phone name) and an embedding computed with the same model used by the project.

This makes the phones discoverable via the app when reading from Chroma.
"""

import argparse
from gsmarena_scraper import PHONE_DATABASE
from review_vector_store import collection, model
from phone_specs import get_phone_specs


def migrate(apply=False, overwrite=False):
    added = []
    skipped = []
    for brand, phones in PHONE_DATABASE.items():
        for phone in phones:
            # check existing entries for this phone
            existing = collection.get(where={"phone": phone}, limit=100)
            existing_ids = existing.get("ids", [])
            existing_meta_ids = [eid for eid in existing_ids if str(eid).endswith("_meta")]

            if existing_meta_ids and not overwrite:
                skipped.append(phone)
                continue

            if apply and overwrite and existing_meta_ids:
                try:
                    # delete only previous meta entries for this phone
                    for mid in existing_meta_ids:
                        collection.delete(ids=[mid])
                except Exception:
                    pass

            # prepare metadata using phone_specs
            specs = get_phone_specs(phone)
            meta = {
                "phone": phone,
                "brand": brand,
                "features": specs.get("features", []),
                "pros": specs.get("pros", []),
                "cons": specs.get("cons", [])
            }

            if apply:
                emb = model.encode(phone).tolist()
                # use a deterministic id for the metadata document
                id_ = f"{phone}_meta"

                # If an entry with this id exists and overwrite requested, delete it
                try:
                    existing_check = collection.get(ids=[id_])
                    if existing_check.get("ids") and overwrite:
                        collection.delete(ids=[id_])
                except Exception:
                    pass

                collection.add(
                    ids=[id_],
                    documents=[phone],
                    embeddings=[emb],
                    metadatas=[meta]
                )
                added.append(phone)
            else:
                # dry run
                added.append(phone)

    return added, skipped


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Apply changes to Chroma (default is dry-run)")
    parser.add_argument("--overwrite", action="store_true", help="When applying, overwrite existing meta entries for each phone")
    args = parser.parse_args()

    apply = args.apply
    overwrite = args.overwrite

    added, skipped = migrate(apply=apply, overwrite=overwrite)

    if apply:
        print(f"Added {len(added)} phones to Chroma metadata (skipped {len(skipped)} existing)")
    else:
        print("Dry run: the following phones would have metadata added/updated:")
        for p in added:
            print(" -", p)
        if skipped:
            print()
            print("Phones that already have metadata entries (would be skipped unless --overwrite):")
            for p in skipped:
                print(" -", p)

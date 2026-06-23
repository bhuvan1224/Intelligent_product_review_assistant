import chromadb

from sentence_transformers import (
    SentenceTransformer
)

client = chromadb.PersistentClient(
    path="review_db"
)

collection = client.get_or_create_collection(
    "phone_reviews"
)

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def store_reviews(
    phone_name,
    reviews
):

    collection.delete(
        where={
            "phone": phone_name
        }
    )

    for i, review in enumerate(reviews):

        embedding = model.encode(
            review
        ).tolist()

        collection.add(

            ids=[
                f"{phone_name}_{i}"
            ],

            documents=[
                review
            ],

            embeddings=[
                embedding
            ],

            metadatas=[
                {
                    "phone": phone_name
                }
            ]
        )


def add_reviews(phone_name, reviews, overwrite=False):
    """Add reviews for a phone into the Chroma collection.

    If overwrite is True, existing entries for the phone are deleted first (same as store_reviews).
    If overwrite is False, new reviews are appended by computing a start index from existing ids to avoid id collisions.

    Returns the number of items added.
    """

    if overwrite:
        collection.delete(where={"phone": phone_name})
        start_idx = 0
    else:
        # find how many entries already exist for this phone to avoid id collisions
        existing = collection.get(where={"phone": phone_name}, limit=100000)
        existing_ids = existing.get("ids", [])
        start_idx = len(existing_ids)

    added = 0
    for i, review in enumerate(reviews):
        idx = start_idx + i
        id_ = f"{phone_name}_{idx}"
        embedding = model.encode(review).tolist()
        collection.add(
            ids=[id_],
            documents=[review],
            embeddings=[embedding],
            metadatas=[{"phone": phone_name}]
        )
        added += 1

    return added


def retrieve_reviews(
    phone_name,
    query
):

    query_embedding = model.encode(
        query
    ).tolist()

    results = collection.query(

        query_embeddings=[
            query_embedding
        ],

        n_results=5,

        where={
            "phone": phone_name
        }
    )

    return results["documents"][0]


def list_stored_reviews(phone_name=None, limit=100):
    """Return a list of stored items from the Chroma collection.

    Each item is a dict with: id, document, metadata, embedding_length.
    If phone_name is provided, filter by metadata phone. Otherwise return across all phones.
    """

    # Use collection.get to fetch stored entries; support optional filtering by metadata
    get_kwargs = {"limit": limit}
    if phone_name:
        get_kwargs["where"] = {"phone": phone_name}

    results = collection.get(**get_kwargs)

    ids = results.get("ids", [])
    docs = results.get("documents", [])
    metas = results.get("metadatas", [])
    embs = results.get("embeddings", [])

    items = []
    for i, _id in enumerate(ids):
        emb_len = None
        try:
            emb = embs[i]
            emb_len = len(emb) if emb is not None else None
        except Exception:
            emb_len = None

        items.append({
            "id": ids[i],
            "document": docs[i] if i < len(docs) else None,
            "metadata": metas[i] if i < len(metas) else None,
            "embedding_length": emb_len
        })

    return items


def import_reviews_from_json(json_path, overwrite=False):
    """Import reviews from a JSON file mapping phone_name -> list of reviews.

    Example JSON structure:
    {
      "iPhone 16 Pro Max": ["review1", "review2"],
      "Galaxy S24": ["...", "..."]
    }
    """

    import json

    with open(json_path, "r", encoding="utf-8") as f:
        payload = json.load(f)

    summary = {}
    for phone, reviews in payload.items():
        count = add_reviews(phone, reviews, overwrite=overwrite)
        summary[phone] = count

    return summary


def phones_with_reviews(phone_list):
    """Return a mapping phone_name -> count of stored reviews in Chroma."""

    summary = {}
    for phone in phone_list:
        results = collection.get(where={"phone": phone}, limit=1_000_000)
        count = len(results.get("ids", []))
        summary[phone] = count
    return summary


def get_all_phones():
    """Return a sorted list of unique phone names present in the Chroma collection (from metadata 'phone')."""

    results = collection.get(limit=1_000_000)
    metas = results.get("metadatas", [])

    phones = set()
    for meta in metas:
        if not meta:
            continue
        phone = meta.get("phone") if isinstance(meta, dict) else None
        if phone:
            phones.add(phone)

    return sorted(list(phones))


def get_phone_metadata(phone_name):
    """Return merged metadata for a phone from Chroma entries.

    Looks for keys like 'features', 'pros', 'cons', 'brand' in stored metadatas and merges lists/values.
    If not present, returns an empty dict.
    """

    results = collection.get(where={"phone": phone_name}, limit=1_000_000)
    metas = results.get("metadatas", [])

    merged = {
        "features": [],
        "pros": [],
        "cons": [],
        "brand": None
    }

    for meta in metas:
        if not isinstance(meta, dict):
            continue
        # brand
        if not merged["brand"] and meta.get("brand"):
            merged["brand"] = meta.get("brand")

        # features/pros/cons may be lists or comma-separated strings
        for key in ("features", "pros", "cons"):
            val = meta.get(key)
            if not val:
                continue
            if isinstance(val, list):
                merged[key].extend(val)
            elif isinstance(val, str):
                # split by newline or comma if looks like a list
                if "\n" in val:
                    items = [x.strip() for x in val.splitlines() if x.strip()]
                    merged[key].extend(items)
                elif "," in val:
                    items = [x.strip() for x in val.split(",") if x.strip()]
                    merged[key].extend(items)
                else:
                    merged[key].append(val.strip())

    # deduplicate while preserving order
    for key in ("features", "pros", "cons"):
        seen = set()
        unique = []
        for x in merged[key]:
            if x not in seen:
                seen.add(x)
                unique.append(x)
        merged[key] = unique

    return merged


if __name__ == "__main__":
    # Quick CLI-style inspection when running the module directly
    import json
    import sys

    # Usage:
    # python review_vector_store.py                    -> list entries
    # python review_vector_store.py "Phone Name"       -> list entries for phone
    # python review_vector_store.py --import file.json   -> import reviews from JSON (append)
    # python review_vector_store.py --import file.json --overwrite -> import and overwrite existing for each phone
    # python review_vector_store.py --check-phone-db   -> check which phones from PHONE_DATABASE have stored reviews

    args = sys.argv[1:]
    if not args:
        phone = None
        items = list_stored_reviews(phone_name=phone, limit=200)
        print(json.dumps(items, indent=2, ensure_ascii=False))
    elif args[0] == "--import" and len(args) >= 2:
        json_path = args[1]
        overwrite = "--overwrite" in args
        summary = import_reviews_from_json(json_path, overwrite=overwrite)
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    elif args[0] == "--check-phone-db":
        # Check all phones from gsmarena_scraper.PHONE_DATABASE
        try:
            from gsmarena_scraper import PHONE_DATABASE
        except Exception as e:
            print(json.dumps({"error": f"failed to import PHONE_DATABASE: {e}"}, indent=2))
            sys.exit(1)

        all_phones = []
        for brand, models in PHONE_DATABASE.items():
            all_phones.extend(models)

        summary = phones_with_reviews(all_phones)
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        phone = args[0]
        items = list_stored_reviews(phone_name=phone, limit=200)
        print(json.dumps(items, indent=2, ensure_ascii=False))
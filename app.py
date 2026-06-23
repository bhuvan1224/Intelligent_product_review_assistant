import streamlit as st
import pandas as pd

from product_search import search_product
from recommendation_engine import recommend_alternative
from analysis import analyze_product
from storage_variants import get_storage_variants

from review_vector_store import (
    store_reviews,
    retrieve_reviews,
    list_stored_reviews,
    get_all_phones,
    get_phone_metadata
)

from review_rag import analyze_reviews


st.set_page_config(
    page_title="Intelligent Product Review Assistant",
    page_icon="📱",
    layout="wide"
)

st.title("📱 Intelligent Product Review Assistant")

st.write(
    "Compare smartphone prices across Amazon, Flipkart and Official Store with AI-powered recommendations."
)

# --------------------------------------------------
# BRAND & PHONE SELECTION (use Chroma as source)
# --------------------------------------------------

# get all phones stored in Chroma (metadata 'phone')
all_phones = get_all_phones()

# build brand->models map from stored metadata, infer brand if missing
def _infer_brand_from_name(phone_name: str):
    n = phone_name.lower()
    if "iphone" in n:
        return "Apple"
    if "samsung" in n or "galaxy" in n:
        return "Samsung"
    if "pixel" in n:
        return "Google"
    if "oneplus" in n:
        return "OnePlus"
    if "nothing" in n:
        return "Nothing"
    if "vivo" in n:
        return "Vivo"
    if "oppo" in n:
        return "Oppo"
    if "realme" in n:
        return "Realme"
    if "xiaomi" in n or "redmi" in n or "mi" in n:
        return "Xiaomi"
    if "motorola" in n or "edge" in n:
        return "Motorola"
    return None

brand_map = {}
for p in all_phones:
    meta = get_phone_metadata(p)
    brand = None
    if isinstance(meta, dict):
        b = meta.get("brand")
        if isinstance(b, str) and b.strip() and b.strip().lower() != "unknown":
            brand = b.strip()

    if not brand:
        inferred = _infer_brand_from_name(p)
        brand = inferred

    # skip entries where brand cannot be determined
    if not brand:
        continue

    brand_map.setdefault(brand, []).append(p)

# If Chroma has no phones, show error and instruct how to populate
if not brand_map:
    st.error(
        "No phones found in Chroma DB. Populate the database first (use migrate or import scripts)."
    )
    st.info("Run: python migrate_phone_db_to_chroma.py --apply and/or import reviews")
    st.stop()

brands = sorted(brand_map.keys())
selected_brand = st.selectbox("📱 Select Brand", brands)

models = sorted(brand_map.get(selected_brand, []))
if not models:
    st.error("No models found in Chroma DB for this brand")
    st.stop()

selected_phone = st.selectbox("📲 Select Phone", models)

# --------------------------------------------------
# STORAGE VARIANTS
# --------------------------------------------------

storage_options = get_storage_variants(
    selected_phone
)

selected_storage = st.selectbox(
    "💾 Select Storage",
    storage_options
)

full_phone_name = (
    f"{selected_phone} {selected_storage}"
)

# --------------------------------------------------
# ANALYZE PRODUCT (fetch everything from Chroma)
# --------------------------------------------------
if st.button("Analyze Product"):

    # Load reviews from Chroma
    stored_items = list_stored_reviews(phone_name=selected_phone, limit=1000)
    reviews = [it["document"] for it in stored_items]

    if not reviews:
        st.warning("No reviews found in Chroma for this phone. Populate the DB first.")

    # full phone display name
    full_phone = f"{selected_phone} {selected_storage}"

    # product search (prices) remains external
    data = search_product(full_phone)

    # specs come from Chroma metadata
    specs = get_phone_metadata(selected_phone) or {}
    # ensure expected keys exist
    specs.setdefault("features", [])
    specs.setdefault("pros", [])
    specs.setdefault("cons", [])

    st.session_state["data"] = data
    st.session_state["specs"] = specs
    st.session_state["phone"] = selected_phone
    st.session_state["storage"] = selected_storage
    st.session_state["full_phone"] = full_phone
# --------------------------------------------------
# RESULTS
# --------------------------------------------------

if "data" in st.session_state:

    data = st.session_state["data"]
    specs = st.session_state["specs"]
    phone = st.session_state["phone"]
    storage = st.session_state.get(
    "storage",
    "128GB"
    )
    full_phone = st.session_state.get(
    "full_phone",
    f"{selected_phone} {selected_storage}"
    )

    st.markdown("---")

    st.header(
        f"📱 {phone} ({storage})"
    )

    # --------------------------------------------------
    # PRICE COMPARISON
    # --------------------------------------------------

    st.subheader("💰 Price Comparison")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Amazon",
            data.get(
                "Amazon",
                "Not Found"
            )
        )

    with col2:
        st.metric(
            "Flipkart",
            data.get(
                "Flipkart",
                "Not Found"
            )
        )

    with col3:
        st.metric(
            "Official Store",
            data.get(
                "Official Store",
                "Not Found"
            )
        )

    st.success(
        f"🏆 Cheapest Store: {data.get('cheapest_store','Unknown')}"
    )

    st.info(
        f"⭐ Best Store Overall: {data.get('best_store','Unknown')}"
    )

    st.write(
        f"🚚 Delivery Insight: {data.get('delivery','-')}"
    )

    st.markdown("---")

    st.subheader(
        "📝 Review Intelligence (RAG)"
    )

    try:

        # Ensure 'priority' is available (comes from user input later). Use session state default if not set.
        priority = st.session_state.get("priority", "Value")
        priority = str(priority).lower()

        retrieved_reviews = retrieve_reviews(

            phone,

            priority
        )

        st.subheader(
            "🛒 Real Customer Reviews"
        )

        for review in retrieved_reviews[:10]:

            st.write(
                f"• {review}"
            )

        review_summary = analyze_reviews(

            phone,

            retrieved_reviews
        )

        st.subheader(
            "🤖 AI Review Summary"
        )

        st.write(
            review_summary
        )

    except Exception as e:

        st.warning(
            f"Review analysis unavailable: {e}"
        )

    # --------------------------------------------------
    # FEATURES
    # --------------------------------------------------

    st.subheader("📋 Key Features")

    for feature in specs.get("features", []):
        st.write(
            f"✅ {feature}"
        )

    st.subheader("👍 Pros")

    for pro in specs.get("pros", []):
        st.write(
            f"✔️ {pro}"
        )

    st.subheader("👎 Cons")

    for con in specs.get("cons", []):
        st.write(
            f"❌ {con}"
        )

    st.markdown("---")

    # --------------------------------------------------
    # USER REQUIREMENTS
    # --------------------------------------------------

    st.subheader(
        "💸 Budget & Preference"
    )

    budget = st.number_input(
        "Budget (₹)",
        min_value=10000,
        max_value=300000,
        value=50000,
        step=1000
    )

    priority = st.selectbox(
        "🎯 Preferred Feature",
        [
            "Camera",
            "Battery",
            "Gaming",
            "Storage",
            "Display",
            "Value"
        ]
    )

    # --------------------------------------------------
    # RECOMMENDATION
    # --------------------------------------------------

    if st.button(
        "🤖 Get AI Recommendation"
    ):

        recommendation = recommend_alternative(
            full_phone,
            budget,
            priority
        )

        recommended_phone = recommendation["name"]

        st.markdown("---")

        st.subheader(
            "🏆 Recommended Phone"
        )

        st.success(
            recommendation["name"]
        )       

        st.metric(
            "Recommended Price",
            recommendation["price"]
        )

        # --------------------------------------------------
        # COMPARISON TABLE
        # --------------------------------------------------

        st.subheader(
            "📊 Feature Comparison"
        )

        comparison_df = pd.DataFrame(
            recommendation["comparison"]
        )

        st.dataframe(
            comparison_df,
            use_container_width=True
        )

        # --------------------------------------------------
        # SIMPLE SCORE CHART
        # --------------------------------------------------

        chart_df = pd.DataFrame({

            "Feature": [
                "Camera",
                "Battery",
                "Gaming",
                "Storage",
                "Display"
            ],

            full_phone: [
                88,
                87,
                90,
                85,
                89
            ],

            recommended_phone: [
                92,
                91,
                88,
                90,
                91
            ]
        })

        st.subheader(
            "📈 Visual Comparison"
        )

        st.bar_chart(
            chart_df.set_index(
                "Feature"
            )
        )

        # --------------------------------------------------
        # AI VERDICT
        # --------------------------------------------------

        st.subheader(
            "🤖 AI Verdict"
        )

        verdict = analyze_product(
            full_phone,
            recommended_phone,
            budget,
            priority
        )

        st.write(
            verdict
        )
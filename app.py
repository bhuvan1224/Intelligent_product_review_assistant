import streamlit as st
import pandas as pd

from gsmarena_scraper import get_brand_models
from product_search import search_product
from phone_specs import get_phone_specs
from recommendation_engine import recommend_alternative
from analysis import analyze_product
from storage_variants import get_storage_variants

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
# BRAND SELECTION
# --------------------------------------------------

brands = [
    "Apple",
    "Samsung",
    "Google",
    "OnePlus",
    "Nothing",
    "Vivo",
    "Oppo",
    "Realme",
    "Xiaomi",
    "Motorola"
]

selected_brand = st.selectbox(
    "📱 Select Brand",
    brands
)

# --------------------------------------------------
# PHONE MODELS
# --------------------------------------------------

models = get_brand_models(selected_brand)

if not models:
    st.error("No models found")
    st.stop()

selected_phone = st.selectbox(
    "📲 Select Phone",
    models
)

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
# ANALYZE PRODUCT
# --------------------------------------------------

if st.button("🔍 Analyze Product"):

    with st.spinner("Fetching prices..."):

        data = search_product(
            full_phone_name
        )

        specs = get_phone_specs(
            selected_phone
        )

        st.session_state["data"] = data
        st.session_state["specs"] = specs
        st.session_state["phone"] = selected_phone
        st.session_state["storage"] = selected_storage
        st.session_state["full_phone"] = full_phone_name

# --------------------------------------------------
# RESULTS
# --------------------------------------------------

if "data" in st.session_state:

    data = st.session_state["data"]
    specs = st.session_state["specs"]
    phone = st.session_state["phone"]
    storage = st.session_state["storage"]
    full_phone = st.session_state["full_phone"]

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

    # --------------------------------------------------
    # FEATURES
    # --------------------------------------------------

    st.subheader("📋 Key Features")

    for feature in specs["features"]:
        st.write(
            f"✅ {feature}"
        )

    st.subheader("👍 Pros")

    for pro in specs["pros"]:
        st.write(
            f"✔️ {pro}"
        )

    st.subheader("👎 Cons")

    for con in specs["cons"]:
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
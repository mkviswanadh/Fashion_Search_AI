import streamlit as st
from llm.filter_extractor import extract_filters
from search.product_retriever import search_products
from utils.helper import display_products

# --- Page config
st.set_page_config(
    page_title="Myntra Fashion Assistant",
    page_icon="🛍️",
    layout="wide"
)

# --- Custom CSS for styling
st.markdown("""
    <style>
    body {
        background-color: #f6f9fc;
    }
    h1, h2, h3 {
        color: #6C63FF;
        text-align: center;
        margin-bottom: 0.1rem;
    }
    .stTextInput>div>div>input {
        border: 2px solid #6C63FF;
        border-radius: 5px;
        padding: 8px;
        font-size: 16px;
    }
    .stButton>button {
        background-color: #6C63FF;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        transition: 0.3s;
        font-weight: 500;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #574b90;
    }
    .chat-box {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        max-height: 600px;
        overflow-y: auto;
        background-color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- First Row: Centered Title
st.markdown("<h1>🛍️ Myntra Fashion Product Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; margin-top: 0; margin-bottom: 20px;'>Search for fashion items using natural language queries. E.g., <i>Red ethnic kurta under 2000 with good rating</i></p>", unsafe_allow_html=True)

# --- Second Row: Image and Chat Side by Side
col1, col2 = st.columns([1, 1])

with col1:
    st.image("title_banner.jpg")

with col2:
    # Query Input
    if "query" not in st.session_state:
        st.session_state.query = ""

    user_query = st.text_input(
        label="What are you looking for today?",
        value=st.session_state.query,
        placeholder="E.g. Kurta under ₹1500 with good rating",
        key="query_input"
    )

    # Buttons side by side
    btn_col1, btn_col2 = st.columns(2)
    search_clicked = btn_col1.button("🔍 Search")
    clear_clicked = btn_col2.button("🧹 Clear")

    # Clear functionality
    if clear_clicked:
        st.session_state.query = ""
        st.experimental_rerun()

    # Chat box container
    st.markdown('<div class="chat-box">', unsafe_allow_html=True)

    # Perform Search and render chat-like display
    if search_clicked and user_query.strip():
        st.session_state.query = user_query.strip()

        with st.spinner("🔎 Searching for products..."):
            filters = extract_filters(user_query)
            results = search_products(user_query, filters, top_k=3)

        if results is not None and not results.empty:
            html = display_products(results)
            st.components.v1.html(html, height=400, scrolling=True)
        else:
            st.warning("⚠️ No matching products found. Try refining your query.")

    st.markdown('</div>', unsafe_allow_html=True)

# --- Optional Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>Built with ❤️ using Streamlit & LangChain</div>",
    unsafe_allow_html=True
)

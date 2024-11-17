import streamlit as st
from bert import bert_sentiment

# Page Configuration
st.set_page_config(
    page_title="Sentiment Analysis",
    page_icon="🍎",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS for Apple-Inspired UI
st.markdown(
    """
    <style>
    /* General background and font styling */
    body {
        background-color: #FFFFFF;
        color: #1D1D1F;
        font-family: -apple-system, BlinkMacSystemFont, 'San Francisco', 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    }
    /* Main header */
    .main-header {
        font-size: 48px;
        font-weight: bold;
        color: #1D1D1F;
        text-align: center;
        margin-top: 30px;
        margin-bottom: 10px;
    }
    /* Subheader */
    .sub-header {
        font-size: 20px;
        color: #6E6E73;
        text-align: center;
        margin-bottom: 40px;
    }
    /* Text area label */
    .text-area-label {
        font-size: 18px;
        color: #1D1D1F;
        margin-bottom: 10px;
    }
    /* Result box styling */
    .result-box {
        font-size: 24px;
        font-weight: 500;
        color: #FFFFFF;
        background-color: #0071E3; /* Apple's signature blue */
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin-top: 30px;
    }
    /* Streamlit button customization */
    div.stButton > button {
        background-color: #0071E3;
        color: #FFFFFF;
        font-size: 16px;
        padding: 10px 20px;
        border-radius: 8px;
        border: none;
        font-family: -apple-system, BlinkMacSystemFont, 'San Francisco', 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #005bb5;
    }
    /* Footer styling */
    .footer {
        text-align: center;
        color: #6E6E73;
        font-size: 14px;
        margin-top: 50px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# App Header
st.markdown('<div class="main-header">Sentiment Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Analyze the sentiment of customer reviews with ease.</div>', unsafe_allow_html=True)

# Input Section
st.markdown('<div class="text-area-label">Enter your review:</div>', unsafe_allow_html=True)
review_text = st.text_area("", placeholder="Type your review here...", height=150)

# Analyze Button and Sentiment Prediction
if st.button("Analyze Sentiment"):
    if review_text.strip():  # Check if input is not empty
        sentiment = bert_sentiment(review_text)
        st.markdown(f'<div class="result-box">The sentiment of the review is **{sentiment}**.</div>', unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please enter a review to analyze.")

# Footer
st.markdown(
    """
    <div class="footer">
        Built with ❤️ using <b>BERT</b> and <b>Streamlit</b>. Inspired by Apple's elegant design principles.
    </div>
    """,
    unsafe_allow_html=True,
)

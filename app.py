import streamlit as st
from bert import bert_sentiment
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Sentilytics",
    page_icon="🔎",
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
        color: #F6F6F6;
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
        color: #6E6E73;
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

    .text-area-label {
    text-align: center;
    }
    /* Streamlit button customization */
    .stButton {
    text-align: center;
    }
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
        color: #FFFFFF;
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

# Initialize a DataFrame to store reviews and their sentiments
if "review_data" not in st.session_state:
    st.session_state["review_data"] = pd.DataFrame(columns=["Review", "Sentiment"])

# Tabs for navigation
tabs = st.tabs(["Sentiment Analysis", "Dashboard"])

# Tab 1: Sentiment Analysis
with tabs[0]:
    st.markdown('<div class="main-header">Sentilytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Analyze the sentiment of customer reviews with ease.</div>', unsafe_allow_html=True)

    st.markdown('<div class="text-area-label">Enter your review:</div>', unsafe_allow_html=True)
    review_text = st.text_area("", placeholder="Type your review here...", height=150)

    if st.button("Analyze Sentiment"):
        if review_text.strip():  # Check if input is not empty
            sentiment = bert_sentiment(review_text)

            # Add review and sentiment to the DataFrame
            new_data = {"Review": review_text, "Sentiment": sentiment}
            st.session_state["review_data"] = pd.concat(
                [st.session_state["review_data"], pd.DataFrame([new_data])],
                ignore_index=True,
            )

            # Display the sentiment
            st.markdown(
                f'<div class="result-box">The sentiment of the review is **{sentiment}**.</div>',
                unsafe_allow_html=True,
            )
        else:
            st.warning("⚠️ Please enter a review to analyze.")

# Tab 2: Dashboard
with tabs[1]:
    st.markdown('<div class="main-header">Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Sentiment Distribution and Analytics</div>', unsafe_allow_html=True)

    # Check if there is data
    if not st.session_state["review_data"].empty:
        st.markdown("### Sentiment Distribution")

        # Display sentiment counts as a bar chart
        sentiment_counts = st.session_state["review_data"]["Sentiment"].value_counts()
        st.bar_chart(sentiment_counts)

        # Display editable data table
        st.markdown("### Collected Reviews (Resizable Table)")
        editable_table = st.data_editor(
            st.session_state["review_data"],
            use_container_width=True,
            key="data_editor",
        )
        st.markdown(
            """
            <small style="color: #6E6E73;">You can resize rows and columns by dragging edges in the table above.</small>
            """,
            unsafe_allow_html=True,
        )

        # Save back changes made in the data editor
        st.session_state["review_data"] = editable_table

        # Generate Insights
        st.markdown("### Insights Based on Reviews")
        
        # Insight 1: Percentage of each sentiment
        total_reviews = len(st.session_state["review_data"])
        positive_reviews = sentiment_counts.get("Positive", 0)
        neutral_reviews = sentiment_counts.get("Neutral", 0)
        negative_reviews = sentiment_counts.get("Negative", 0)

        st.markdown(f"- **Total Reviews:** {total_reviews}")
        st.markdown(f"- **Positive Reviews:** {positive_reviews} ({(positive_reviews / total_reviews) * 100:.2f}%)")
        st.markdown(f"- **Neutral Reviews:** {neutral_reviews} ({(neutral_reviews / total_reviews) * 100:.2f}%)")
        st.markdown(f"- **Negative Reviews:** {negative_reviews} ({(negative_reviews / total_reviews) * 100:.2f}%)")

        # Insight 2: Most Common Words in Reviews
        from collections import Counter

        all_words = " ".join(st.session_state["review_data"]["Review"]).split()
        common_words = Counter(all_words).most_common(5)
        st.markdown("### Most Common Words in Reviews")
        for word, count in common_words:
            st.markdown(f"- **{word}**: {count} times")

        # Insight 3: Review Length Analysis
        review_lengths = st.session_state["review_data"]["Review"].str.split().apply(len)
        avg_length = review_lengths.mean()
        max_length = review_lengths.max()
        min_length = review_lengths.min()

        st.markdown("### Review Length Analysis")
        st.markdown(f"- **Average Review Length:** {avg_length:.2f} words")
        st.markdown(f"- **Longest Review:** {max_length} words")
        st.markdown(f"- **Shortest Review:** {min_length} words")

    else:
        st.info("No data available yet. Analyze some reviews to populate the dashboard!")



# Footer
st.markdown(
    """
    <div class="footer">
        Built with ❤️ using <b>Streamlit</b>.
    </div>
    """,
    unsafe_allow_html=True,
)

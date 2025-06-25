import streamlit as st
import pandas as pd
import numpy as np
from textblob import TextBlob
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import re

# Set page config
st.set_page_config(
    page_title="Car Rental Feedback Analyzer",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    font-size: 3rem;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.metric-card {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

def clean_text(text):
    """Clean and preprocess text"""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = ' '.join(text.split())
    return text

def analyze_sentiment_textblob(text):
    """Analyze sentiment using TextBlob"""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    if polarity > 0.1:
        sentiment = 'Positive'
    elif polarity < -0.1:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'

    return sentiment, polarity, subjectivity

def extract_issues(text):
    """Extract common issues from negative reviews"""
    issues = []
    text_lower = text.lower()

    issue_keywords = {
        'cleanliness': ['dirty', 'unclean', 'smell', 'stain'],
        'vehicle_condition': ['broken', 'damage', 'scratch', 'problem', 'issue'],
        'service_quality': ['rude', 'unprofessional', 'poor service', 'bad service'],
        'wait_time': ['long wait', 'delay', 'slow', 'took too long'],
        'pricing': ['expensive', 'hidden charge', 'overpriced', 'costly']
    }

    for issue, keywords in issue_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            issues.append(issue)

    return issues

def main():
    # Header
    st.markdown('<h1 class="main-header">🚗 Car Rental Feedback Analyzer</h1>', unsafe_allow_html=True)
    st.markdown("---")

    # Sidebar
    with st.sidebar:
        st.header("📊 Analysis Options")
        analysis_type = st.selectbox(
            "Choose Analysis Type:",
            ["Single Review Analysis", "Bulk CSV Analysis"]
        )

    if analysis_type == "Single Review Analysis":
        st.header("🔍 Single Review Analysis")

        # Input text area
        review_text = st.text_area(
            "Enter customer review:",
            placeholder="Type the customer review here...",
            height=100
        )

        if st.button("Analyze Review", type="primary"):
            if review_text.strip():
                # Analyze sentiment
                sentiment, polarity, subjectivity = analyze_sentiment_textblob(review_text)

                # Display results
                col1, col2, col3 = st.columns(3)

                with col1:
                    if sentiment == "Positive":
                        st.success(f"😊 {sentiment}")
                    elif sentiment == "Negative":
                        st.error(f"😞 {sentiment}")
                    else:
                        st.info(f"😐 {sentiment}")

                with col2:
                    st.metric("Polarity Score", f"{polarity:.3f}")

                with col3:
                    st.metric("Subjectivity", f"{subjectivity:.3f}")

                # Extract issues if negative
                if sentiment == "Negative":
                    issues = extract_issues(review_text)
                    if issues:
                        st.subheader("⚠️ Identified Issues:")
                        for issue in issues:
                            st.write(f"• {issue.replace('_', ' ').title()}")

                # Polarity explanation
                st.subheader("📈 Score Explanation:")
                st.write("**Polarity:** -1 (very negative) to +1 (very positive)")
                st.write("**Subjectivity:** 0 (objective) to 1 (subjective)")

            else:
                st.warning("Please enter a review to analyze.")

    else:  # Bulk CSV Analysis
        st.header("📁 Bulk CSV Analysis")

        # File uploader
        uploaded_file = st.file_uploader(
            "Upload CSV file with reviews",
            type=['csv'],
            help="CSV should have columns: 'review_text' and optionally 'rating'"
        )

        # Sample data option
        if st.button("Use Sample Data"):
            # Create sample data
            sample_data = {
                'customer_name': [f'Customer_{i+1}' for i in range(10)],
                'review_text': [
                    "Great service! The car was clean and staff was helpful.",
                    "The car had engine issues and rental process took too long.",
                    "Excellent experience. Car was in perfect condition.",
                    "Very disappointed with the service. Car was dirty.",
                    "Good value for money. Decent car and professional staff.",
                    "Terrible experience. Car broke down during trip.",
                    "Amazing service! Quick rental process and new car.",
                    "Average experience. Car was okay but could be cleaner.",
                    "Outstanding customer service. Staff was very helpful.",
                    "Poor service quality. Long waiting times and unclean vehicle."
                ],
                'rating': [5, 2, 5, 1, 4, 1, 5, 3, 5, 2]
            }
            df = pd.DataFrame(sample_data)
            st.success("Sample data loaded!")

        elif uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.success(f"File uploaded successfully! Shape: {df.shape}")
            except Exception as e:
                st.error(f"Error reading file: {e}")
                df = None
        else:
            df = None

        if df is not None:
            # Display data preview
            st.subheader("📋 Data Preview")
            st.dataframe(df.head())

            # Check required columns
            if 'review_text' not in df.columns:
                st.error("CSV must contain 'review_text' column")
                return

            # Analyze button
            if st.button("Analyze All Reviews", type="primary"):
                with st.spinner("Analyzing reviews..."):
                    # Perform analysis
                    df['cleaned_text'] = df['review_text'].apply(clean_text)

                    # Analyze sentiment
                    sentiment_results = df['cleaned_text'].apply(analyze_sentiment_textblob)
                    df['sentiment'] = [result[0] for result in sentiment_results]
                    df['polarity'] = [result[1] for result in sentiment_results]
                    df['subjectivity'] = [result[2] for result in sentiment_results]

                    # Extract issues
                    df['issues'] = df.apply(lambda row: extract_issues(row['review_text']) 
                                          if row['sentiment'] == 'Negative' else [], axis=1)

                # Display results
                st.success("Analysis completed!")

                # Summary metrics
                st.subheader("📊 Summary Metrics")
                col1, col2, col3, col4 = st.columns(4)

                sentiment_counts = df['sentiment'].value_counts()
                total_reviews = len(df)

                with col1:
                    st.metric("Total Reviews", total_reviews)

                with col2:
                    positive_pct = (sentiment_counts.get('Positive', 0) / total_reviews) * 100
                    st.metric("Positive Reviews", f"{positive_pct:.1f}%")

                with col3:
                    negative_pct = (sentiment_counts.get('Negative', 0) / total_reviews) * 100
                    st.metric("Negative Reviews", f"{negative_pct:.1f}%")

                with col4:
                    avg_polarity = df['polarity'].mean()
                    st.metric("Average Polarity", f"{avg_polarity:.3f}")

                # Visualizations
                st.subheader("📈 Visualizations")

                col1, col2 = st.columns(2)

                with col1:
                    # Sentiment distribution pie chart
                    fig_pie = px.pie(
                        values=sentiment_counts.values,
                        names=sentiment_counts.index,
                        title="Sentiment Distribution",
                        color_discrete_map={
                            'Positive': '#2E8B57',
                            'Negative': '#DC143C',
                            'Neutral': '#FFD700'
                        }
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)

                with col2:
                    # Polarity distribution histogram
                    fig_hist = px.histogram(
                        df, x='polarity',
                        title="Polarity Score Distribution",
                        nbins=20,
                        color_discrete_sequence=['#1f77b4']
                    )
                    fig_hist.add_vline(x=0, line_dash="dash", line_color="red")
                    st.plotly_chart(fig_hist, use_container_width=True)

                # Issues analysis
                if df['sentiment'].value_counts().get('Negative', 0) > 0:
                    st.subheader("⚠️ Common Issues Analysis")

                    all_issues = []
                    for issues_list in df['issues']:
                        all_issues.extend(issues_list)

                    if all_issues:
                        issue_counts = Counter(all_issues)
                        issue_df = pd.DataFrame(
                            list(issue_counts.items()),
                            columns=['Issue', 'Count']
                        ).sort_values('Count', ascending=True)

                        fig_bar = px.bar(
                            issue_df, x='Count', y='Issue',
                            title="Most Common Issues",
                            orientation='h',
                            color='Count',
                            color_continuous_scale='Reds'
                        )
                        st.plotly_chart(fig_bar, use_container_width=True)
                    else:
                        st.info("No specific issues identified in negative reviews.")

                # Download results
                st.subheader("💾 Download Results")

                # Convert to CSV
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download Analysis Results",
                    data=csv,
                    file_name="sentiment_analysis_results.csv",
                    mime="text/csv"
                )

                # Detailed results table
                st.subheader("📋 Detailed Results")
                st.dataframe(
                    df[['review_text', 'sentiment', 'polarity', 'subjectivity']],
                    use_container_width=True
                )

if __name__ == "__main__":
    main()

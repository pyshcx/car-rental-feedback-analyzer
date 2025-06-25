# Car Rental Customer Feedback Analyzer
# Simple Sentiment Analysis Project for College

import pandas as pd
import numpy as np
from textblob import TextBlob
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
import warnings
warnings.filterwarnings('ignore')

def load_data(file_path):
    """Load the car rental reviews dataset"""
    try:
        df = pd.read_csv(file_path)
        print(f"Dataset loaded successfully! Shape: {df.shape}")
        return df
    except FileNotFoundError:
        print("File not found. Please check the file path.")
        return None

def clean_text(text):
    """Clean and preprocess text"""
    # Convert to lowercase
    text = text.lower()
    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text

def analyze_sentiment_textblob(text):
    """Analyze sentiment using TextBlob"""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    # Classify sentiment
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

    # Define issue keywords
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

def perform_analysis(df):
    """Perform comprehensive sentiment analysis"""
    print("Performing sentiment analysis...")

    # Clean text
    df['cleaned_text'] = df['review_text'].apply(clean_text)

    # Analyze sentiment
    sentiment_results = df['cleaned_text'].apply(analyze_sentiment_textblob)
    df['sentiment'] = [result[0] for result in sentiment_results]
    df['polarity'] = [result[1] for result in sentiment_results]
    df['subjectivity'] = [result[2] for result in sentiment_results]

    # Extract issues from negative reviews
    df['issues'] = df.apply(lambda row: extract_issues(row['review_text']) 
                           if row['sentiment'] == 'Negative' else [], axis=1)

    return df

def generate_summary_report(df):
    """Generate summary report"""
    total_reviews = len(df)

    # Sentiment distribution
    sentiment_counts = df['sentiment'].value_counts()

    # Average ratings by sentiment
    sentiment_ratings = df.groupby('sentiment')['rating'].mean()

    # Most common issues
    all_issues = []
    for issues_list in df['issues']:
        all_issues.extend(issues_list)
    issue_counts = Counter(all_issues)

    # Create summary report
    report = """
===============================================================================
                        CAR RENTAL FEEDBACK ANALYSIS REPORT
===============================================================================

OVERVIEW:
---------
Total Reviews Analyzed: {}
Analysis Date: {}

SENTIMENT DISTRIBUTION:
----------------------
Positive Reviews: {} ({:.1f}%)
Negative Reviews: {} ({:.1f}%)
Neutral Reviews: {} ({:.1f}%)

AVERAGE RATINGS BY SENTIMENT:
----------------------------""".format(
        total_reviews,
        pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
        sentiment_counts.get('Positive', 0),
        sentiment_counts.get('Positive', 0)/total_reviews*100,
        sentiment_counts.get('Negative', 0),
        sentiment_counts.get('Negative', 0)/total_reviews*100,
        sentiment_counts.get('Neutral', 0),
        sentiment_counts.get('Neutral', 0)/total_reviews*100
    )

    for sentiment in sentiment_ratings.index:
        report += f"\n    {sentiment}: {sentiment_ratings[sentiment]:.2f}/5.0"

    report += "\n\nMOST COMMON ISSUES (Top 5):"
    report += "\n---------------------------"

    for issue, count in issue_counts.most_common(5):
        report += f"\n    {issue.replace('_', ' ').title()}: {count} occurrences"

    report += "\n\nRECOMMENDATIONS:"
    report += "\n---------------"

    if sentiment_counts.get('Negative', 0) > total_reviews * 0.3:
        report += "\n    • High negative sentiment detected. Immediate action required."

    top_issues = [issue for issue, count in issue_counts.most_common(3)]
    if 'cleanliness' in top_issues:
        report += "\n    • Improve vehicle cleaning procedures."
    if 'vehicle_condition' in top_issues:
        report += "\n    • Enhance vehicle maintenance and inspection."
    if 'service_quality' in top_issues:
        report += "\n    • Provide customer service training for staff."

    report += "\n\n==============================================================================="

    return report

def create_visualizations(df):
    """Create visualizations for the analysis"""
    plt.style.use('default')
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Car Rental Customer Feedback Analysis', fontsize=16, fontweight='bold')

    # 1. Sentiment Distribution
    sentiment_counts = df['sentiment'].value_counts()
    colors = ['#2E8B57', '#DC143C', '#FFD700']  # Green, Red, Gold
    axes[0, 0].pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%', 
                   colors=colors, startangle=90)
    axes[0, 0].set_title('Sentiment Distribution')

    # 2. Rating Distribution
    axes[0, 1].hist(df['rating'], bins=5, color='skyblue', edgecolor='black', alpha=0.7)
    axes[0, 1].set_title('Rating Distribution')
    axes[0, 1].set_xlabel('Rating')
    axes[0, 1].set_ylabel('Frequency')
    axes[0, 1].set_xticks(range(1, 6))

    # 3. Sentiment vs Rating
    sentiment_order = ['Negative', 'Neutral', 'Positive']
    df_ordered = df.copy()
    df_ordered['sentiment'] = pd.Categorical(df_ordered['sentiment'], categories=sentiment_order, ordered=True)
    df_ordered = df_ordered.sort_values('sentiment')

    sns.boxplot(data=df_ordered, x='sentiment', y='rating', ax=axes[1, 0])
    axes[1, 0].set_title('Rating by Sentiment')
    axes[1, 0].set_xlabel('Sentiment')
    axes[1, 0].set_ylabel('Rating')

    # 4. Polarity Distribution
    axes[1, 1].hist(df['polarity'], bins=15, color='lightcoral', edgecolor='black', alpha=0.7)
    axes[1, 1].set_title('Polarity Score Distribution')
    axes[1, 1].set_xlabel('Polarity Score')
    axes[1, 1].set_ylabel('Frequency')
    axes[1, 1].axvline(x=0, color='black', linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig('sentiment_analysis_report.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """Main function to run the analysis"""
    print("=== Car Rental Customer Feedback Analyzer ===\n")

    # Load data
    df = load_data('car_rental_reviews.csv')
    if df is None:
        return

    print("\nSample data:")
    print(df.head())

    # Perform analysis
    df_analyzed = perform_analysis(df)

    # Generate and display report
    report = generate_summary_report(df_analyzed)
    print(report)

    # Save results
    df_analyzed.to_csv('analyzed_reviews.csv', index=False)
    print("Results saved to 'analyzed_reviews.csv'")

    # Save report
    with open('sentiment_analysis_report.txt', 'w') as f:
        f.write(report)
    print("Report saved to 'sentiment_analysis_report.txt'")

    # Create visualizations
    create_visualizations(df_analyzed)
    print("Visualizations saved to 'sentiment_analysis_report.png'")

    print("\n=== Analysis Complete! ===")

if __name__ == "__main__":
    main()

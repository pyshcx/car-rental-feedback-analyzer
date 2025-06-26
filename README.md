# [Car Rental Customer Feedback Analyzer](https://car-rental-feedback-analyzer.streamlit.app/)
## Simple Sentiment Analysis Project - One Day Implementation

### 🎯 Project Overview
This project analyzes customer reviews of car rental services using sentiment analysis to:
- Identify positive, negative, and neutral sentiments
- Extract key issues from customer feedback
- Generate automated reports for service teams
- Provide visual insights through charts and graphs

### 📁 Project Structure
```
car-rental-feedback-analyzer/
├── car_rental_reviews.csv          # Sample dataset
├── sentiment_analyzer.py           # Main analysis script
├── streamlit_app.py                # Web app interface
├── requirements.txt                # Python dependencies
├── README.md                       # This file
└── results/                        # Output files (generated)
    ├── analyzed_reviews.csv
    ├── sentiment_analysis_report.txt
    └── sentiment_analysis_report.png
```

### 🚀 Quick Start Guide

#### Step 1: Setup Environment
```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download TextBlob corpora (first time only)
python -c "import nltk; nltk.download('punkt'); nltk.download('brown')"
```

#### Step 2: Run Command Line Analysis
```bash
python sentiment_analyzer.py
```

#### Step 3: Run Web App
```bash
streamlit run streamlit_app.py
```

### 📊 Features

#### Command Line Tool (`sentiment_analyzer.py`)
- Loads CSV data with customer reviews
- Performs sentiment analysis using TextBlob
- Extracts common issues from negative reviews
- Generates comprehensive report
- Creates visualizations
- Saves results to CSV and report files

#### Web Application (`streamlit_app.py`)
- Interactive web interface
- Single review analysis
- Bulk CSV file upload and analysis
- Real-time visualizations
- Downloadable results
- Sample data option

### 📈 Sample Output

#### Sentiment Distribution:
- Positive Reviews: 45% (Happy customers)
- Negative Reviews: 30% (Issues to address)
- Neutral Reviews: 25% (Room for improvement)

#### Common Issues Identified:
1. Vehicle Condition (scratches, mechanical problems)
2. Service Quality (staff behavior, wait times)
3. Cleanliness (dirty cars, odors)
4. Pricing (hidden charges, overpricing)

### 🎓 College Project Presentation Tips

#### What to Include:
1. **Problem Statement**: Why sentiment analysis is important for car rental companies
2. **Methodology**: TextBlob for sentiment analysis, feature extraction techniques
3. **Implementation**: Python code walkthrough, web app demo
4. **Results**: Show sample analysis, visualizations, insights
5. **Business Impact**: How this helps car rental companies improve service

#### Demo Script:
1. Show the web app interface
2. Analyze a sample positive review
3. Analyze a sample negative review showing issue extraction
4. Upload the CSV file and show bulk analysis
5. Explain the visualizations and metrics
6. Discuss practical applications

### 🔧 Customization Options

#### Add More Sentiment Libraries:
- VADER Sentiment for social media text
- Hugging Face Transformers for advanced analysis
- Custom trained models

#### Extend Issue Detection:
- Add more issue categories
- Use machine learning for automatic issue categorization
- Implement keyword extraction algorithms

#### Enhanced Visualizations:
- Time-series analysis of sentiment trends
- Geographic sentiment mapping
- Customer journey sentiment analysis

### 📝 Technical Implementation Details

#### Sentiment Analysis:
- Uses TextBlob's rule-based approach
- Polarity score: -1 (negative) to +1 (positive)
- Subjectivity score: 0 (objective) to 1 (subjective)

#### Issue Extraction:
- Keyword matching approach
- Categorizes issues into predefined buckets
- Extensible for new issue types

#### Data Processing:
- Text cleaning and preprocessing
- Handles missing data gracefully
- Supports multiple input formats

### 🎯 Evaluation Criteria for College Project

#### Technical Implementation (40%):
- Code quality and structure
- Use of appropriate libraries
- Error handling and robustness

#### Results and Analysis (30%):
- Accuracy of sentiment classification
- Quality of insights generated
- Visualization effectiveness

#### Presentation and Documentation (20%):
- Clear explanation of methodology
- Professional presentation
- Complete documentation

#### Innovation and Extensions (10%):
- Additional features implemented
- Creative solutions to problems
- Future improvement suggestions

### 📚 Learning Outcomes
- Natural Language Processing basics
- Sentiment analysis techniques
- Web application development with Streamlit
- Data visualization and reporting
- Real-world business problem solving

### 🚀 Next Steps for Advanced Implementation
1. Deploy the web app to cloud platforms (Heroku, Streamlit Cloud)
2. Integrate with real-time data sources (APIs, databases)
3. Add user authentication and data persistence
4. Implement advanced ML models for better accuracy
5. Create automated alerting system for negative reviews

### 📞 Support
This is a college project template. Modify and extend according to your specific requirements and institutional guidelines.

Good luck with your project! 🎉

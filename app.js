// Car Rental Customer Feedback Analyzer - JavaScript functionality

// Sample data from the application_data_json
const applicationData = {
  sampleReviews: [
    {
      text: "Great service! The car was clean and the staff was very helpful. Highly recommend.",
      sentiment: "Positive",
      polarity: 0.7,
      issues: []
    },
    {
      text: "The car had some issues with the engine and the rental process took too long.",
      sentiment: "Negative", 
      polarity: -0.4,
      issues: ["vehicle_condition", "wait_time"]
    },
    {
      text: "Very disappointed with the service. The car was dirty and had scratches.",
      sentiment: "Negative",
      polarity: -0.6,
      issues: ["cleanliness", "vehicle_condition"]
    }
  ],
  sentimentDistribution: {
    positive: 6,
    negative: 8, 
    neutral: 6
  },
  commonIssues: [
    {issue: "Vehicle Condition", count: 4},
    {issue: "Service Quality", count: 3},
    {issue: "Cleanliness", count: 2},
    {issue: "Wait Time", count: 2},
    {issue: "Pricing", count: 1}
  ],
  projectFiles: [
    {
      name: "sentiment_analyzer.py",
      description: "Main analysis script that processes CSV files and generates reports"
    },
    {
      name: "streamlit_app.py", 
      description: "Web application for interactive sentiment analysis"
    },
    {
      name: "car_rental_reviews.csv",
      description: "Sample dataset with 20 customer reviews"
    },
    {
      name: "requirements.txt",
      description: "Python dependencies list"
    },
    {
      name: "README.md",
      description: "Complete setup guide and documentation"
    }
  ]
};

// Sentiment analysis keywords
const sentimentKeywords = {
  positive: [
    'excellent', 'great', 'good', 'amazing', 'wonderful', 'fantastic', 'perfect',
    'clean', 'helpful', 'professional', 'recommend', 'satisfied', 'happy',
    'efficient', 'smooth', 'easy', 'comfortable', 'reliable', 'outstanding'
  ],
  negative: [
    'terrible', 'awful', 'bad', 'horrible', 'disappointing', 'poor', 'worst',
    'dirty', 'broken', 'damaged', 'rude', 'unhelpful', 'expensive', 'overpriced',
    'delayed', 'late', 'problem', 'issue', 'complaint', 'dissatisfied', 'angry'
  ]
};

// Issue detection keywords
const issueKeywords = {
  'vehicle_condition': ['broken', 'damaged', 'scratches', 'dents', 'mechanical', 'engine', 'problem', 'issues', 'faulty'],
  'cleanliness': ['dirty', 'unclean', 'messy', 'stains', 'smell', 'odor'],
  'service_quality': ['rude', 'unhelpful', 'unprofessional', 'poor service', 'bad service'],
  'wait_time': ['long wait', 'delayed', 'slow', 'took too long', 'waiting'],
  'pricing': ['expensive', 'overpriced', 'costly', 'too much', 'high price']
};

// Simple sentiment analysis function
function analyzeSentiment(text) {
  const words = text.toLowerCase().split(/\s+/);
  let positiveScore = 0;
  let negativeScore = 0;
  
  words.forEach(word => {
    if (sentimentKeywords.positive.some(keyword => word.includes(keyword))) {
      positiveScore++;
    }
    if (sentimentKeywords.negative.some(keyword => word.includes(keyword))) {
      negativeScore++;
    }
  });
  
  const totalSentimentWords = positiveScore + negativeScore;
  const polarity = totalSentimentWords > 0 ? 
    (positiveScore - negativeScore) / totalSentimentWords : 0;
  
  // Normalize polarity to -1 to 1 range
  const normalizedPolarity = Math.max(-1, Math.min(1, polarity));
  
  // Calculate subjectivity (simplified)
  const subjectivity = Math.min(1, totalSentimentWords / words.length * 3);
  
  // Determine sentiment category
  let sentiment;
  if (normalizedPolarity > 0.1) {
    sentiment = 'Positive';
  } else if (normalizedPolarity < -0.1) {
    sentiment = 'Negative';
  } else {
    sentiment = 'Neutral';
  }
  
  // Detect issues
  const issues = [];
  const lowerText = text.toLowerCase();
  
  Object.keys(issueKeywords).forEach(issueType => {
    if (issueKeywords[issueType].some(keyword => lowerText.includes(keyword))) {
      issues.push(issueType);
    }
  });
  
  return {
    sentiment,
    polarity: parseFloat(normalizedPolarity.toFixed(2)),
    subjectivity: parseFloat(subjectivity.toFixed(2)),
    issues
  };
}

// Format issue names for display
function formatIssueName(issue) {
  return issue.split('_').map(word => 
    word.charAt(0).toUpperCase() + word.slice(1)
  ).join(' ');
}

// Display analysis results
function displayResults(results) {
  const resultsSection = document.getElementById('results');
  const sentimentResult = document.getElementById('sentimentResult');
  const polarityResult = document.getElementById('polarityResult');
  const subjectivityResult = document.getElementById('subjectivityResult');
  const issuesSection = document.getElementById('issuesSection');
  const issuesList = document.getElementById('issuesList');
  
  // Show results section
  resultsSection.classList.remove('hidden');
  
  // Display sentiment
  sentimentResult.textContent = results.sentiment;
  sentimentResult.className = `sentiment-badge sentiment-${results.sentiment.toLowerCase()}`;
  
  // Display scores
  polarityResult.textContent = results.polarity;
  subjectivityResult.textContent = results.subjectivity;
  
  // Display issues if any
  if (results.issues.length > 0) {
    issuesSection.classList.remove('hidden');
    issuesList.innerHTML = '';
    results.issues.forEach(issue => {
      const issueTag = document.createElement('span');
      issueTag.className = 'issue-tag';
      issueTag.textContent = formatIssueName(issue);
      issuesList.appendChild(issueTag);
    });
  } else {
    issuesSection.classList.add('hidden');
  }
}

// Initialize charts
function initializeCharts() {
  // Sentiment Distribution Chart
  const sentimentCtx = document.getElementById('sentimentChart').getContext('2d');
  new Chart(sentimentCtx, {
    type: 'doughnut',
    data: {
      labels: ['Positive', 'Negative', 'Neutral'],
      datasets: [{
        data: [
          applicationData.sentimentDistribution.positive,
          applicationData.sentimentDistribution.negative,
          applicationData.sentimentDistribution.neutral
        ],
        backgroundColor: ['#1FB8CD', '#B4413C', '#5D878F'],
        borderWidth: 2,
        borderColor: '#fff'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            padding: 20,
            usePointStyle: true
          }
        }
      }
    }
  });
  
  // Common Issues Chart
  const issuesCtx = document.getElementById('issuesChart').getContext('2d');
  new Chart(issuesCtx, {
    type: 'bar',
    data: {
      labels: applicationData.commonIssues.map(item => item.issue),
      datasets: [{
        label: 'Number of Reports',
        data: applicationData.commonIssues.map(item => item.count),
        backgroundColor: '#FFC185',
        borderColor: '#DB4545',
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            stepSize: 1
          }
        }
      },
      plugins: {
        legend: {
          display: false
        }
      }
    }
  });
}

// Display sample reviews
function displaySampleReviews() {
  const container = document.getElementById('sampleReviewsContainer');
  
  applicationData.sampleReviews.forEach(review => {
    const reviewCard = document.createElement('div');
    reviewCard.className = 'sample-review-card';
    
    const reviewText = document.createElement('div');
    reviewText.className = 'sample-review-text';
    reviewText.textContent = `"${review.text}"`;
    
    const reviewResults = document.createElement('div');
    reviewResults.className = 'sample-review-results';
    
    const sentimentSpan = document.createElement('span');
    sentimentSpan.className = `sentiment-badge sentiment-${review.sentiment.toLowerCase()}`;
    sentimentSpan.textContent = review.sentiment;
    sentimentSpan.style.fontSize = 'var(--font-size-sm)';
    sentimentSpan.style.padding = 'var(--space-4) var(--space-8)';
    
    const polaritySpan = document.createElement('span');
    polaritySpan.textContent = `Polarity: ${review.polarity}`;
    polaritySpan.style.fontSize = 'var(--font-size-sm)';
    polaritySpan.style.fontWeight = 'var(--font-weight-medium)';
    
    reviewResults.appendChild(sentimentSpan);
    reviewResults.appendChild(polaritySpan);
    
    reviewCard.appendChild(reviewText);
    reviewCard.appendChild(reviewResults);
    
    // Add issues if any
    if (review.issues.length > 0) {
      const issuesDiv = document.createElement('div');
      issuesDiv.style.marginTop = 'var(--space-8)';
      issuesDiv.innerHTML = '<small><strong>Issues:</strong> ' + 
        review.issues.map(formatIssueName).join(', ') + '</small>';
      reviewCard.appendChild(issuesDiv);
    }
    
    container.appendChild(reviewCard);
  });
}

// Display project files
function displayProjectFiles() {
  const container = document.getElementById('projectFiles');
  
  applicationData.projectFiles.forEach(file => {
    const fileCard = document.createElement('div');
    fileCard.className = 'file-card';
    
    const fileName = document.createElement('div');
    fileName.className = 'file-name';
    fileName.textContent = file.name;
    
    const fileDescription = document.createElement('p');
    fileDescription.className = 'file-description';
    fileDescription.textContent = file.description;
    
    fileCard.appendChild(fileName);
    fileCard.appendChild(fileDescription);
    container.appendChild(fileCard);
  });
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
  // Initialize charts
  initializeCharts();
  
  // Display sample reviews
  displaySampleReviews();
  
  // Display project files
  displayProjectFiles();
  
  // Analyze button functionality
  const analyzeBtn = document.getElementById('analyzeBtn');
  const reviewInput = document.getElementById('reviewInput');
  
  analyzeBtn.addEventListener('click', function() {
    const reviewText = reviewInput.value.trim();
    
    if (!reviewText) {
      alert('Please enter a review to analyze.');
      return;
    }
    
    // Show loading state
    analyzeBtn.textContent = 'Analyzing...';
    analyzeBtn.disabled = true;
    
    // Simulate processing delay for better UX
    setTimeout(() => {
      const results = analyzeSentiment(reviewText);
      displayResults(results);
      
      // Reset button
      analyzeBtn.textContent = 'Analyze Review';
      analyzeBtn.disabled = false;
      
      // Scroll to results
      document.getElementById('results').scrollIntoView({ 
        behavior: 'smooth', 
        block: 'start' 
      });
    }, 1000);
  });
  
  // Enter key support for textarea
  reviewInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && e.ctrlKey) {
      analyzeBtn.click();
    }
  });
  
  // Add some sample text on page load for demonstration
  reviewInput.placeholder = "Enter a car rental review here... (e.g., 'The car was clean and the service was excellent!' or 'The vehicle had mechanical issues and the staff was unhelpful.')\n\nTip: Press Ctrl+Enter to analyze quickly.";
});
import requests
from textblob import TextBlob

def get_video_comments(video_id, api_key):
    # Make request to YouTube Data API
    params = {
        'part': 'snippet',
        'videoId': video_id,  # Pass the video ID directly
        'maxResults': 100,   # Maximum number of comments to retrieve
        'textFormat': 'plainText',
        'key': api_key
    }
    response = requests.get('https://youtube.googleapis.com/youtube/v3/commentThreads', params=params)
    
    # Check if response is successful
    if response.status_code != 200:
        print(f"Error: Failed to retrieve comments. Status code: {response.status_code}")
        return []
    
    # Extract comments
    data = response.json()
    if 'items' not in data:
        print("Error: No comments found for the given video ID.")
        return []
    
    comments = []
    for item in data['items']:
        comments.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])
    
    return comments

def analyze_sentiment(comments):
    # Initialize counters
    positive_count = 0
    negative_count = 0
    neutral_count = 0
    
    # Analyze sentiment of each comment
    for comment in comments:
        analysis = TextBlob(comment)
        sentiment_score = analysis.sentiment.polarity
        
        # Classify sentiment
        if sentiment_score > 0:
            positive_count += 1
        elif sentiment_score < 0:
            negative_count += 1
        else:
            neutral_count += 1
    
    # Calculate percentages
    total_comments = len(comments)
    positive_percentage = (positive_count / total_comments) * 100
    negative_percentage = (negative_count / total_comments) * 100
    neutral_percentage = (neutral_count / total_comments) * 100
    
    return positive_percentage, negative_percentage, neutral_percentage

def main():
    # YouTube video ID and API key
    video_id = 'AZvTyzkU3MY'
    api_key = 'AIzaSyDleCJ5P28kkQ2YVffk8aemWaSJ2WM4V18'  # Replace with your actual API key
    
    # Get comments from the YouTube video
    
    comments = get_video_comments(video_id, api_key)
    
    # Analyze sentiment of comments
    positive_percentage, negative_percentage, neutral_percentage = analyze_sentiment(comments)
    
    # Display results
    print(f"Positive Comments: {positive_percentage:.2f}%")
    print(f"Negative Comments: {negative_percentage:.2f}%")
    print(f"Neutral Comments: {neutral_percentage:.2f}%")

if __name__ == "__main__":
    main()

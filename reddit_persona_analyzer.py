import streamlit as st
import praw
import re
from datetime import datetime
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import os
from typing import Dict, List, Tuple
import logging

# Download required NLTK data
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RedditPersonaAnalyzer:
    """A class to analyze Reddit user profiles and generate user personas."""
    
    def __init__(self, client_id: str, client_secret: str, user_agent: str):
        """Initialize Reddit API client and sentiment analyzer."""
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        self.sia = SentimentIntensityAnalyzer()
        self.persona = {
            'interests': {},
            'sentiment': {'positive': 0, 'negative': 0, 'neutral': 0},
            'activity_level': 0,
            'subreddits': set(),
            'evidence': []
        }

    def clean_text(self, text: str) -> str:
        """Clean text by removing special characters and extra whitespace."""
        text = re.sub(r'\s+', ' ', text.strip())
        text = re.sub(r'[^\w\s,.]', '', text)
        return text

    def analyze_sentiment(self, text: str) -> str:
        """Analyze sentiment of given text using VADER."""
        scores = self.sia.polarity_scores(text)
        if scores['compound'] >= 0.05:
            return 'positive'
        elif scores['compound'] <= -0.05:
            return 'negative'
        return 'neutral'

    def extract_topics(self, text: str) -> List[str]:
        """Extract key topics from text using simple keyword analysis."""
        words = self.clean_text(text).lower().split()
        common_words = {'the', 'is', 'in', 'and', 'to', 'a', 'of', 'for', 'on', 'with', 'by'}
        topics = [word for word in words if word not in common_words and len(word) > 3]
        return topics[:5]  # Return top 5 topics

    def analyze_user(self, user_url: str) -> Dict:
        """Analyze Reddit user profile and build persona."""
        try:
            username = user_url.split('/user/')[-1].rstrip('/')
            redditor = self.reddit.redditor(username)
            
            # Process comments
            for comment in redditor.comments.new(limit=50):
                self.process_content(comment, 'comment')
                
            # Process posts
            for submission in redditor.submissions.new(limit=50):
                self.process_content(submission, 'post')
                
            # Calculate activity level
            self.persona['activity_level'] = len(self.persona['evidence'])
            
            return self.persona
            
        except Exception as e:
            logger.error(f"Error analyzing user {user_url}: {str(e)}")
            return {}

    def process_content(self, content, content_type: str) -> None:
        """Process individual comment or post."""
        text = content.body if content_type == 'comment' else content.title + ' ' + (content.selftext or '')
        cleaned_text = self.clean_text(text)
        
        # Update sentiment
        sentiment = self.analyze_sentiment(cleaned_text)
        self.persona['sentiment'][sentiment] += 1
        
        # Update subreddits
        subreddit = str(content.subreddit)
        self.persona['subreddits'].add(subreddit)
        
        # Update interests
        topics = self.extract_topics(cleaned_text)
        for topic in topics:
            self.persona['interests'][topic] = self.persona['interests'].get(topic, 0) + 1
            
        # Store evidence
        evidence = {
            'type': content_type,
            'subreddit': subreddit,
            'text': cleaned_text[:100] + '...' if len(cleaned_text) > 100 else cleaned_text,
            'permalink': f"https://www.reddit.com{content.permalink}",
            'timestamp': datetime.fromtimestamp(content.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
            'topics': topics,
            'sentiment': sentiment
        }
        self.persona['evidence'].append(evidence)

    def generate_persona_output(self, username: str) -> str:
        """Generate formatted persona output."""
        output = f"User Persona for Reddit User: {username}\n"
        output += "=" * 50 + "\n\n"
        
        output += "Interests:\n"
        for topic, count in sorted(self.persona['interests'].items(), key=lambda x: x[1], reverse=True)[:5]:
            output += f"- {topic} (mentioned {count} times)\n"
            relevant_evidence = [e for e in self.persona['evidence'] if topic in e['topics']]
            for evidence in relevant_evidence[:2]:  # Limit to 2 evidence per topic
                output += f"  * {evidence['type'].capitalize()} in r/{evidence['subreddit']} ({evidence['timestamp']}): "
                output += f"{evidence['text']}\n  * Source: {evidence['permalink']}\n"
        output += "\n"

        output += "Sentiment Analysis:\n"
        total = sum(self.persona['sentiment'].values())
        for sentiment, count in self.persona['sentiment'].items():
            percentage = (count / total * 100) if total > 0 else 0
            output += f"- {sentiment.capitalize()}: {count} ({percentage:.1f}%)\n"
        output += "\n"

        output += f"Activity Level: {self.persona['activity_level']} posts/comments analyzed\n\n"
        
        output += "Active Subreddits:\n"
        for subreddit in sorted(self.persona['subreddits'])[:5]:
            output += f"- r/{subreddit}\n"
            relevant_evidence = [e for e in self.persona['evidence'] if e['subreddit'] == subreddit]
            for evidence in relevant_evidence[:2]:  # Limit to 2 evidence per subreddit
                output += f"  * {evidence['type'].capitalize()} ({evidence['timestamp']}): "
                output += f"{evidence['text']}\n  * Source: {evidence['permalink']}\n"
                
        return output

def main():
    """Main Streamlit application."""
    st.title("Reddit User Persona Analyzer")
    
    # Input for Reddit API credentials
    st.sidebar.header("Reddit API Credentials")
    client_id = st.sidebar.text_input("Client ID", type="password")
    client_secret = st.sidebar.text_input("Client Secret", type="password")
    user_agent = st.sidebar.text_input("User Agent", value="RedditPersonaAnalyzer/1.0")
    
    # Input for Reddit user URL
    user_url = st.text_input("Enter Reddit User Profile URL (e.g., https://www.reddit.com/user/username/)")
    
    if st.button("Analyze User"):
        if not user_url or not client_id or not client_secret:
            st.error("Please provide all required inputs.")
            return
            
        try:
            analyzer = RedditPersonaAnalyzer(client_id, client_secret, user_agent)
            persona = analyzer.analyze_user(user_url)
            
            if not persona:
                st.error("Failed to analyze user. Please check the URL and API credentials.")
                return
                
            username = user_url.split('/user/')[-1].rstrip('/')
            output = analyzer.generate_persona_output(username)
            
            # Display results
            st.subheader("User Persona")
            st.text_area("Persona Details", output, height=400)
            
            # Save to file
            output_dir = "persona_outputs"
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, f"{username}_persona.txt")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output)
                
            st.success(f"Persona saved to {output_file}")
            
            # Provide download button
            with open(output_file, 'r', encoding='utf-8') as f:
                st.download_button(
                    label="Download Persona",
                    data=f,
                    file_name=f"{username}_persona.txt",
                    mime="text/plain"
                )
                
        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()

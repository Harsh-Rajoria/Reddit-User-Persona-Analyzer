# Reddit-User-Persona-Analyzer
Reddit User Persona Analyzer
This project is a Streamlit-based Python application that analyzes a Reddit user's profile to create a comprehensive user persona based on their posts and comments.
Prerequisites

Python 3.8 or higher
Reddit API credentials (Client ID, Client Secret)
A Reddit user profile URL to analyze

Installation

Clone the repository:

git clone https://github.com/Harsh-Rajoria/Reddit-User-Persona-Analyzer.git
cd Reddit-User-Persona-Analyzer 


Create a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install required packages:

pip install -r requirements.txt

Setup

Obtain Reddit API credentials:

Go to https://www.reddit.com/prefs/apps
Create a new application
Note down the Client ID and Client Secret
Use a unique User Agent (e.g., "RedditPersonaAnalyzer/1.0")


Create a requirements.txt file with the following content:


streamlit==1.31.0
praw==7.7.1
nltk==3.8.1


Install NLTK data:

import nltk
nltk.download('vader_lexicon')

Usage

Run the Streamlit app:

streamlit run reddit_persona_analyzer.py


Open your browser and go to the URL displayed (usually http://localhost:8501)

Enter your Reddit API credentials in the sidebar:

Client ID
Client Secret
User Agent


Enter a Reddit user profile URL (e.g., https://www.reddit.com/user/username/)

Click "Analyze User" to generate the persona

The results will be displayed on the screen and saved to a text file in the persona_outputs directory


Output Format
The output is saved as a text file named <username>_persona.txt containing:

User interests with frequency and evidence citations
Sentiment analysis of posts/comments
Activity level
Active subreddits with example posts/comments
Links to original content for verification

Each characteristic includes citations to specific posts or comments used as evidence.
Notes

The script follows PEP-8 guidelines
It uses PRAW for Reddit API access, NLTK for sentiment analysis, and Streamlit for the UI
Output files are saved in the persona_outputs directory
The script limits analysis to the 50 most recent comments and posts
Error handling is implemented for invalid URLs and API issues

Troubleshooting

Ensure your Reddit API credentials are valid
Check your internet connection
Verify the user profile URL is correct
Make sure the Reddit user has public posts/comments

For any issues, check the logs in the console or contact support through Internshala.Reddit User Persona Analyzer
This project is a Streamlit-based Python application that analyzes a Reddit user's profile to create a comprehensive user persona based on their posts and comments.
Prerequisites

Python 3.8 or higher
Reddit API credentials (Client ID, Client Secret)
A Reddit user profile URL to analyze

Installation

Clone the repository:

git clone https://github.com/your-username/reddit-persona-analyzer.git
cd reddit-persona-analyzer


Create a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install required packages:

pip install -r requirements.txt

Setup

Obtain Reddit API credentials:

Go to https://www.reddit.com/prefs/apps
Create a new application
Note down the Client ID and Client Secret
Use a unique User Agent (e.g., "RedditPersonaAnalyzer/1.0")


Create a requirements.txt file with the following content:


streamlit==1.31.0
praw==7.7.1
nltk==3.8.1


Install NLTK data:

import nltk
nltk.download('vader_lexicon')

Usage

Run the Streamlit app:

streamlit run reddit_persona_analyzer.py


Open your browser and go to the URL displayed (usually http://localhost:8501)

Enter your Reddit API credentials in the sidebar:

Client ID
Client Secret
User Agent


Enter a Reddit user profile URL (e.g., https://www.reddit.com/user/username/)

Click "Analyze User" to generate the persona

The results will be displayed on the screen and saved to a text file in the persona_outputs directory


Output Format
The output is saved as a text file named <username>_persona.txt containing:

User interests with frequency and evidence citations
Sentiment analysis of posts/comments
Activity level
Active subreddits with example posts/comments
Links to original content for verification

Each characteristic includes citations to specific posts or comments used as evidence.
Notes

The script follows PEP-8 guidelines
It uses PRAW for Reddit API access, NLTK for sentiment analysis, and Streamlit for the UI
Output files are saved in the persona_outputs directory
The script limits analysis to the 50 most recent comments and posts
Error handling is implemented for invalid URLs and API issues

Troubleshooting

Ensure your Reddit API credentials are valid
Check your internet connection
Verify the user profile URL is correct
Make sure the Reddit user has public posts/comments

For any issues, check the logs in the console or contact support through Internshala.
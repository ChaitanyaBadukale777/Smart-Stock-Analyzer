import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Function to get stock news from NewsAPI
def get_stock_news(stock_name):
    try:
        api_key = os.getenv("NEWSAPI_API_KEY")  # Add your NewsAPI key in the .env file
        url = f"https://newsapi.org/v2/everything?q={stock_name}+stock&apiKey={api_key}&language=en"

        response = requests.get(url)
        data = response.json()

        if data['status'] == 'ok' and data['totalResults'] > 0:
            print(f"\nLatest news about {stock_name}:\n")
            for article in data['articles'][:5]:  # Fetching top 5 news articles
                title = article['title']
                description = article['description']
                url = article['url']
                print(f"- {title}\n  Description: {description}\n  URL: {url}\n")
        else:
            print("No news found for this stock.")
    
    except Exception as e:
        print(f"Error fetching stock news: {e}")

# Main function
if __name__ == "__main__":
    stock_name = input("Enter the stock name or ticker (e.g., Apple, AAPL): ")
    get_stock_news(stock_name)

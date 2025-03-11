import os
import requests
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import streamlit as st
from textblob import TextBlob

# Load environment variables from .env file
load_dotenv()

# Function to get stock news from NewsAPI
def get_stock_news(stock_name):
    try:
        api_key = os.getenv("NEWSAPI_API_KEY")
        url = f"https://newsapi.org/v2/everything?q={stock_name}+stock&apiKey={api_key}&language=en"

        response = requests.get(url)
        data = response.json()

        if data['status'] == 'ok' and data['totalResults'] > 0:
            return data['articles'][:5]
        return None
    except Exception as e:
        st.error(f"Error fetching news: {e}")
        return None

# Function to get stock data from Alpha Vantage
def get_stock_data(symbol):
    try:
        api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
        
        response = requests.get(url)
        data = response.json()
        
        if 'Time Series (Daily)' not in data:
            st.error("Error fetching stock data: Invalid symbol or API limit reached")
            return None
            
        daily_data = data['Time Series (Daily)']
        dates = list(daily_data.keys())[:20]  # Last 20 days
        closes = [float(daily_data[date]['4. close']) for date in dates]
        return {
            'current_price': closes[0],
            '20_day_avg': sum(closes)/len(closes),
            'latest_close': closes[0],
            'previous_close': closes[1]
        }
    except Exception as e:
        st.error(f"Error fetching stock data: {e}")
        return None

# Function to get historical data for the chart
def get_historical_data(symbol):
    try:
        api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={api_key}"
        
        response = requests.get(url)
        data = response.json()
        
        if 'Time Series (Daily)' not in data:
            return None
            
        daily_data = data['Time Series (Daily)']
        df = pd.DataFrame.from_dict(daily_data, orient='index')
        df = df.rename(columns={'4. close': 'Close'})
        df['Close'] = df['Close'].astype(float)
        df.index = pd.to_datetime(df.index)
        df = df.sort_index(ascending=True)
        
        # Filter last 2 years of data
        return df.last('2Y')
    except Exception as e:
        st.error(f"Error fetching historical data: {e}")
        return None

# Function to analyze news sentiment
def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

# Generate recommendation
def generate_recommendation(stock_data, news_sentiment):
    if not stock_data:
        return "Insufficient data for recommendation"
    
    current = stock_data['current_price']
    ma_20 = stock_data['20_day_avg']
    
    recommendation = ""
    if current > ma_20:
        recommendation += "Technical: Price above 20-day MA (+) "
    else:
        recommendation += "Technical: Price below 20-day MA (-) "
    
    if news_sentiment > 0.1:
        recommendation += "| Positive News Sentiment (+) "
    elif news_sentiment < -0.1:
        recommendation += "| Negative News Sentiment (-) "
    else:
        recommendation += "| Neutral News Sentiment "
    
    if current > ma_20 and news_sentiment > 0.1:
        return "Recommendation: STRONG BUY 🟢", recommendation
    elif current > ma_20 and news_sentiment >= -0.1:
        return "Recommendation: BUY 🟢", recommendation
    elif current < ma_20 and news_sentiment < -0.1:
        return "Recommendation: STRONG SELL 🔴", recommendation
    else:
        return "Recommendation: HOLD 🟡", recommendation

# Streamlit App
st.title("📈 Smart Stock Analyzer")
st.write("Comprehensive stock analysis with news and technical indicators")

# Input Section
col1, col2 = st.columns(2)
with col1:
    symbol = st.text_input("Enter stock ticker (e.g., AAPL):", value="AAPL").upper()
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_btn = st.button("Analyze Stock")

if analyze_btn:
    with st.spinner("Analyzing stock..."):
        stock_data = get_stock_data(symbol)
        news_articles = get_stock_news(symbol)
        historical_data = get_historical_data(symbol)
        
        news_sentiment = 0
        if news_articles:
            all_headlines = " ".join([art['title'] for art in news_articles])
            news_sentiment = analyze_sentiment(all_headlines)
        
        if stock_data:
            st.subheader(f"{symbol} Stock Analysis")
            
            # Price Info Columns
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Current Price", f"${stock_data['current_price']:.2f}")
            with col2:
                change = stock_data['current_price'] - stock_data['previous_close']
                st.metric("Daily Change", f"${change:.2f}", 
                          f"{change/stock_data['previous_close']*100:.2f}%")
            with col3:
                st.metric("20-Day Average", f"${stock_data['20_day_avg']:.2f}")
            
            # Recommendation
            rec_text, rec_details = generate_recommendation(stock_data, news_sentiment)
            st.success(rec_text)
            st.caption(f"Analysis: {rec_details}")
            
            # Price History Chart
            st.subheader("2-Year Price History")
            if historical_data is not None:
                fig = px.line(historical_data, x=historical_data.index, y='Close',
                              labels={'x': 'Date', 'Close': 'Price ($)'},
                              title=f"{symbol} Closing Price History")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Could not load historical price data")
            
            # News Section
            if news_articles:
                st.subheader("Trending Insights & Market Buzz")
                for article in news_articles:
                    art_sentiment = analyze_sentiment(article['title'])
                    sentiment_emoji = "🟢" if art_sentiment > 0.1 else "🔴" if art_sentiment < -0.1 else "🟡"
                    
                    with st.expander(f"{sentiment_emoji} {article['title']}"):
                        st.write(article['description'])
                        st.markdown(f"[Read more]({article['url']})", unsafe_allow_html=True)
            else:
                st.warning("No news articles found")
            
            # Disclaimer
            st.markdown("---")
            st.caption("⚠️ Note: This is automated analysis, not financial advice. Always do your own research before investing.")
        
        else:
            st.error("Failed to retrieve stock data. Please check the ticker symbol.")
st.markdown("Made with ❤️ by Chaitanya Badukale")
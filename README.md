# 📈 Smart Stock Analyzer – StockVision

A **real-time stock analysis** web application built with Python and Streamlit, offering automated insights using **market data, sentiment analysis**, and **technical indicators**.

![StockVision Demo](https://your-screenshot-or-demo-link.png)

---

## 🚀 Features

- 🔍 Real-time stock data using **Alpha Vantage API**
- 📰 **Sentiment Analysis** on stock-related news via **NewsAPI** and **TextBlob**
- 📊 Visualizations powered by **Plotly** for interactive charting
- 🧠 Stock recommendations based on:
  - **20-day Moving Average**
  - **News Sentiment Score**

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Data Analysis**: Pandas, NumPy
- **Visualization**: Plotly
- **APIs**: Alpha Vantage, NewsAPI
- **NLP**: TextBlob for sentiment analysis

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/stockvision.git
cd stockvision

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```
## Run the App
```bash
streamlit run filename.py
```
## File Structure
```bash
stockvision/
│
├── app.py                  # Main Streamlit app
├── analysis.py             # Technical and sentiment analysis logic
├── news_fetcher.py         # News API integration
├── requirements.txt
└── README.md
```
## 📊 Sample Output
Interactive candlestick chart

Real-time moving average plot

Sentiment polarity indicator

Buy/Sell/Hold recommendation tag

## 🔑 API Setup
### Alpha Vantage API:

Sign up at https://www.alphavantage.co

```Replace API_KEY in your app.py```

NewsAPI:

Sign up at https://newsapi.org

```Replace NEWS_API_KEY in your news_fetcher.py```

## 📌 To-Do
 Add more technical indicators (RSI, MACD)

 Include user portfolio tracking

 Deploy the app on Streamlit Cloud

 ## 🙌 Acknowledgements
Streamlit

Alpha Vantage API

NewsAPI

TextBlob

Plotly



## 📄 License
This project is licensed under the MIT License.

# 📈 MACD Sentiment & Signal Dashboard

A real-time financial visualization tool built with Flask and Plotly that identifies market momentum, calculates trend sentiment, and triggers algorithmic Buy/Sell alerts.

# 🚀 Key Features

Algorithmic Signal Alerts: Real-time detection of MACD crossovers, providing instant BUY or SELL notifications based on price-action conviction.

Dynamic Sentiment Meter: A custom-built UI component that quantifies the "Bullish vs. Bearish" tug-of-war using MACD histogram data.

Volume Strength Verification: Analyzes Relative Volume (RVOL) against a 20-period average to confirm if a trend is backed by high market activity.

Unified Dual-Axis Charting: An interactive Plotly dashboard featuring a secondary Y-axis layout, allowing users to view price action and indicators in one seamless view.

Asynchronous Data Handling: Uses AJAX (Fetch API) to update stats and charts without refreshing the page.

# 🛠️ Tech Stack

Backend: Python (Flask)
Data Source: yfinance (Live Market Data)
Analysis: Pandas, NumPy
Frontend: HTML5, CSS3 (Modern Glossy UI), JavaScript (ES6+)
Visualization: Plotly.js

# 📸 Dashboard Preview

Sentiment Meter	Signal Alerts
[Insert Screenshot of your Green/Red bar]	[Insert Screenshot of your Buy/Sell popup]

# 🧬 How the Signal Logic Works

The dashboard uses a combination of two factors to trigger alerts:
Crossover: The MACD Line must cross the Signal Line.
Threshold (The Gap): To avoid "false signals" during flat markets, the Histogram (gap between lines) must exceed a specific volatility threshold before an alert is fired.

# ⚙️ Installation & Setup
Clone the repository:

[git clone https://github.com](https://github.com/ceewa30/StockMarketMACD.git)


# Install dependencies:

pip install flask yfinance pandas plotly numpy


# Run the application:

python app.py


Access in browser: http://127.0.0.1:5000

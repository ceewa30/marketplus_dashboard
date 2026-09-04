import json
from flask import Flask, jsonify, render_template, request
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.utils import PlotlyJSONEncoder
import yfinance as yf

app = Flask(__name__)

def calculate_indicators(df):
    """
    Advanced Quantitative Processing Pipeline
    Calculates Trend Sentiment, Momentum (RSI), MACD, Bollinger Bands, and Signals.
    """
    if df.empty or len(df) < 20:  # Safeguard for short dataframes
        return df

    # Ensure column headers match what yfinance returns
    # Sometimes yfinance outputs MultiIndex columns, flatten them if so
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # 1. Trend Sentiment Engine (EMA Crossovers)
    df['EMA_9'] = df['Close'].ewm(span=9, adjust=False).mean()
    df['EMA_21'] = df['Close'].ewm(span=21, adjust=False).mean()
    df['Sentiment_Score'] = np.where(df['EMA_9'] > df['EMA_21'], 1, -1)
    
    # 2. Market Momentum Engine (RSI)
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / (loss + 1e-10)
    df['RSI'] = 100 - (100 / (1 + rs))

    # 3. Bollinger Bands Engine (20-Period, 2 Standard Deviations)
    df['BB_MA'] = df['Close'].rolling(window=20).mean()
    df['BB_STD'] = df['Close'].rolling(window=20).std()
    df['BB_Upper'] = df['BB_MA'] + (df['BB_STD'] * 2)
    df['BB_Lower'] = df['BB_MA'] - (df['BB_STD'] * 2)

    # 4. MACD Engine (12, 26, 9)
    df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD_Line'] = df['EMA_12'] - df['EMA_26']
    df['MACD_Signal'] = df['MACD_Line'].ewm(span=9, adjust=False).mean()
    df['MACD_Hist'] = df['MACD_Line'] - df['MACD_Signal']

    # 5. Volumetric / Dynamic Algorithmic Alerts
    df['Signal'] = 'Hold'
    df['Alert_Color'] = 'gray'
    
    # Start iterating safely past the Bollinger Band warm-up window
    for i in range(20, len(df)):
        # BUY Trigger: RSI is oversold (<45) AND Price is near Lower Bollinger Band AND MACD Histogram is gaining strength
        if (df['RSI'].iloc[i] < 45 and 
            df['Close'].iloc[i] <= df['BB_Lower'].iloc[i] * 1.01 and 
            df['MACD_Hist'].iloc[i] > df['MACD_Hist'].iloc[i-1]):
            df.at[df.index[i], 'Signal'] = 'BUY'
            
        # SELL Trigger: RSI is overbought (>55) AND Price is near Upper Bollinger Band AND MACD Histogram is losing strength
        elif (df['RSI'].iloc[i] > 55 and 
              df['Close'].iloc[i] >= df['BB_Upper'].iloc[i] * 0.99 and 
              df['MACD_Hist'].iloc[i] < df['MACD_Hist'].iloc[i-1]):
            df.at[df.index[i], 'Signal'] = 'SELL'
            
    return df

def generate_plotly_json(df, ticker):
    """
    Generates a 3-tier subplot stack mapping out Price/Bands, Volume, and MACD.
    """
    df = df.reset_index()
    # Rename the first column to 'Date' regardless of if it's named 'Date' or 'Datetime'
    df.rename(columns={df.columns[0]: 'Date'}, inplace=True)

    # Filter out initial warm-up rows
    df_clean = df.dropna(subset=['RSI', 'BB_Lower', 'MACD_Hist'])
    # print(df_clean)
    
    fig = make_subplots(
        rows=3, cols=1, 
        shared_xaxes=True, 
        vertical_spacing=0.03,
        row_heights=[0.55, 0.15, 0.30]
    )

    # Convert timestamps to string to bypass timezone formatting bugs in JSON serialization
    time_index = df['Date'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist()

    # --- PANEL 1: Candlesticks & Volatility Bands ---
    fig.add_trace(go.Candlestick(
        x=time_index, open=df_clean['Open'].tolist(), high=df_clean['High'].tolist(),
        low=df_clean['Low'].tolist(), close=df_clean['Close'].tolist(), name='Price'
    ), row=1, col=1)
    
    fig.add_trace(go.Scatter(x=time_index, y=df_clean['BB_Upper'].tolist(), name='BB Upper', line=dict(color='rgba(147, 51, 234, 0.4)', dash='dash')), row=1, col=1)
    fig.add_trace(go.Scatter(x=time_index, y=df_clean['BB_Lower'].tolist(), name='BB Lower', line=dict(color='rgba(147, 51, 234, 0.4)', dash='dash'), fill='tonexty', fillcolor='rgba(147, 51, 234, 0.02)'), row=1, col=1)
    fig.add_trace(go.Scatter(x=time_index, y=df_clean['BB_MA'].tolist(), name='BB Basis', line=dict(color='purple', width=1)), row=1, col=1)

    # # Mapping Signal Markers
    buys = df_clean[df_clean['Signal'] == 'BUY']
    # print(buys)
    sells = df_clean[df_clean['Signal'] == 'SELL']
    
    fig.add_trace(go.Scatter(x=buys['Date'].tolist(), y=(buys['Close'] * 0.98).tolist(), mode='markers', name='Buy Alert', marker=dict(symbol='triangle-up', size=13, color='#10b981')), row=1, col=1)
    fig.add_trace(go.Scatter(x=sells['Date'].tolist(), y=(sells['Close'] * 1.02).tolist(), mode='markers', name='Sell Alert', marker=dict(symbol='triangle-down', size=13, color='#ef4444')), row=1, col=1)

    # # --- PANEL 2: Volumetric Analytics ---
    vol_colors = ['#10b981' if df_clean['Close'].iloc[i] >= df_clean['Open'].iloc[i] else '#ef4444' for i in range(len(df_clean))]
    fig.add_trace(go.Bar(x=time_index, y=df_clean['Volume'].tolist(), name='Volume', marker_color=vol_colors, opacity=0.7), row=2, col=1)

    # # --- PANEL 3: MACD Oscillators & Histograms ---
    fig.add_trace(go.Scatter(x=time_index, y=df_clean['MACD_Line'].tolist(), name='MACD', line=dict(color='#2563eb', width=1.5)), row=3, col=1)
    fig.add_trace(go.Scatter(x=time_index, y=df_clean['MACD_Signal'].tolist(), name='Signal', line=dict(color='#d97706', width=1.5)), row=3, col=1)
    
    hist_colors = ['#10b981' if val >= 0 else '#ef4444' for val in df_clean['MACD_Hist'].tolist()]
    fig.add_trace(go.Bar(x=time_index, y=df_clean['MACD_Hist'].tolist(), name='Histogram', marker_color=hist_colors), row=3, col=1)

    # Dark Mode Structural Architecture Layout
    fig.update_layout(
        title=f"MarketPlus Matrix: {ticker}",
        template="plotly_dark",
        height=750,  # Increased from 600 to give all 3 subplots breathing room
        margin=dict(l=60, r=50, t=80, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(17,24,39,1)',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    # CRITICAL PLOTLY SUBPLOT RULES: Explicitly strip layout constraints from sub-tracks
    fig.update_xaxes(rangeslider_visible=False, row=1, col=1)
    fig.update_xaxes(rangeslider_visible=False, row=2, col=1)
    fig.update_xaxes(rangeslider_visible=False, row=3, col=1)
    
    # Optional: Clear labels to make scanning panel values fast and scannable
    fig.update_yaxes(title_text="Price / Bands", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    fig.update_yaxes(title_text="MACD", row=3, col=1)
    
    return json.dumps(fig, cls=PlotlyJSONEncoder)

@app.route('/')
def index():
    return render_template('index.html', default_ticker="AAPL")

@app.route('/api/update-market')
def update_market():
    ticker = request.args.get('ticker', 'AAPL').upper()
    timeframe = request.args.get('timeframe', '1d')
    interval = '1m' if timeframe == '1d' else '5m' if timeframe == '5d' else '1h'
    
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=timeframe, interval=interval)
        
        # --- AUTOMATIC WEEKEND / MARKET SAFETY FALLBACK ---
        # If the requested window is completely blank, load wider context automatically
        if df.empty or len(df) < 20:
            df = stock.history(period="5d", interval="5m")
            
        if df.empty or len(df) < 20:
            return jsonify({'error': f"Ticker target asset arrays for '{ticker}' returned zero metrics."}), 400
            
        df = calculate_indicators(df)
        latest_row = df.iloc[-1]
        prev_row = df.iloc[-2] if len(df) > 1 else latest_row
        
        sentiment_label = "BULLISH" if latest_row['Sentiment_Score'] == 1 else "BEARISH"
        sentiment_color = "text-emerald-500" if sentiment_label == "BULLISH" else "text-rose-500"
        
        alert_rows = df[df['Signal'] != 'Hold']
        latest_alert = alert_rows.iloc[-1]['Signal'] if not alert_rows.empty else 'HOLD'
        alert_color = "bg-emerald-500" if latest_alert == 'BUY' else "bg-rose-500" if latest_alert == 'SELL' else "bg-gray-600"

        # Safe extraction check for RSI value
        rsi_val = latest_row['RSI']
        rsi_str = f"{rsi_val:.1f}" if not np.isnan(rsi_val) else "--"

        payload = {
            'graph_json': json.loads(generate_plotly_json(df, ticker)),
            'metrics': {
                'price': f"${latest_row['Close']:.2f}",
                'change': f"{((latest_row['Close'] - prev_row['Close'])/prev_row['Close']*100):+.2f}%",
                'momentum_rsi': f"{latest_row['RSI']:.1f}" if not pd.isna(latest_row['RSI']) else "--",
                'sentiment': sentiment_label,
                'sentiment_color': sentiment_color,
                'algo_alert': latest_alert,
                'alert_color': alert_color
            }
        }
        return jsonify(payload)
    except Exception as e:
        return jsonify({'error': f"Internal Server Crash: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

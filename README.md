# ⚡ MarketPlus: Real-Time Algorithmic Trading & Momentum Matrix

MarketPlus is a high-frequency, real-time financial visualization pipeline built using **Flask** and **Plotly.js**. The platform streams live intraday market arrays from Yahoo Finance, routes them through a multi-tier technical indicator engine, and dynamically renders interactive 3-panel charting layouts. 

The tool evaluates market data using a calculation framework that triggers real-time algorithmic `BUY`, `SELL`, or `HOLD` alerts based on the alignment of volatility, trend momentum, and volume.

---

## 🚀 Key Architectural Features

* **Live Streaming Pipeline**: Background AJAX polling loop updates text-telemetry metric arrays and Plotly assets every 10 seconds asynchronously without forcing page reloads.
* **Flicker-Free Coordinate Tracking**: Uses `Plotly.react()` inline updating mechanics to seamlessly inject price ticks while fully preserving user-configured UI mouse pan/zoom scaling.
* **Interactive Control States**: Features an integrated Stream Pause/Resume engine to instantly freeze background threads for historical bar inspections.
* **Fail-Safe Market Context Router**: Detects weekend/after-hours market closures automatically, dropping down to wider context intervals to ensure charts never render empty.

---

## 📊 Quantitative Indicators & Rules Engine

MarketPlus processes active vector streams using five coupled operations:

1. **Trend Sentiment Engine**: Calculates 9-period vs 21-period Exponential Moving Average (EMA) cross-tracks to establish structural baseline directions.
2. **Market Momentum Engine**: Computes relative price speed changes across a smoothed 14-period Relative Strength Index (RSI) matrix.
3. **Volatility Engine**: Plots a 20-period standard deviation envelope (Bollinger Bands) to map historical boundary expansion extremes.
4. **MACD Engine**: Tracks trend convergence and divergence using standard (12, 26, 9) exponential momentum spacing histograms.

### Algorithmic Execution Matrix

```text
       [ MARKET TELEMETRY STREAM ]
                    │
         ┌──────────┴──────────┐
         ▼                     ▼
  (Bullish Matrix)       (Bearish Matrix)
   • RSI < 45             • RSI > 55
   • Price ≤ Lower BB     • Price ≥ Upper BB
   • MACD Hist Gaining    • MACD Hist Declining
         │                     │
         ▼                     ▼
   [ SIGNAL: BUY ]       [ SIGNAL: SELL ]
```

---

## 📂 Directory Layout Structure

```text
marketplus_dashboard/
│
├── app.py                  # Main Flask Web Framework & Quantitative Engine
├── templates/
│   └── index.html          # UI Skeleton Layout (TailwindCSS & Async JS Engine)
└── requirements.txt        # Production Python System Dependency Pins
```

---

## 🛠️ Local Installation & Execution Steps

Follow these instructions to configure and execute MarketPlus locally on your machine:

### 1. Initialize the Target Workspace Environment
Open your terminal window inside your project workspace folder:
```bash
cd path/to/your/marketplus_dashboard
```

### 2. Configure a Isolated Python Virtual Environment
* **On macOS / Linux platforms:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
* **On Windows platforms:**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

### 3. Install Framework Dependencies
Install the pinned libraries directly through the python package manager:
```bash
pip install flask yfinance pandas plotly numpy
```

### 4. Execute the Application Instance
Launch the built-in local development server node directly:
```bash
python app.py
```

Once running, point any web browser to **`http://127.0.0.1:5000`** to stream the live analytical visualization dashboard.

---

## ⚙️ Configuration Properties (API Routing)

Intraday streaming properties can be manipulated natively inside the top-level parameters of your network interface panel:

| Option Parameter | Time Scale Context | Dynamic Polling Resolution |
| :--- | :--- | :--- |
| **`1d`** | 1 Trading Day (Live Window) | 1 Minute Interval Price Action Ticks |
| **`5d`** | 5 Historical Days | 5 Minute Interval Price Action Bars |
| **`1mo`** | 1 Month Context Window | 1 Hour Interval Consolidation Bars |

---

## 📜 License
Distributed under the MIT License. See `LICENSE` for more information.
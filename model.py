import pandas as pd
import numpy as np
from sklearn.svm import SVR
from sklearn.preprocessing import MinMaxScaler
import plotly.graph_objs as go
from datetime import timedelta
def prediction(stock_code, n_days):
    df = pd.read_csv("World-Stock-Prices-Dataset.csv")
    df = df[df['Ticker'].str.upper() == stock_code.upper()].copy()
    df['Date'] = df['Date'].astype(str)
    df['Date'] = pd.to_datetime(df['Date'], utc=True, errors='coerce').dt.tz_convert(None)
    df = df.sort_values('Date')
    close_prices = df['Close'].values.reshape(-1, 1)
    scaler = MinMaxScaler()
    scaled_close = scaler.fit_transform(close_prices)
    X, y = [], []
    window_size = 30
    for i in range(window_size, len(scaled_close)):
    X.append(scaled_close[i-window_size:i, 0])
    y.append(scaled_close[i, 0])
    X, y = np.array(X), np.array(y)
   model = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=0.01)
   model.fit(X, y)
     last_seq = scaled_close[-window_size:].flatten().tolist()
    predictions_scaled = []
    for _ in range(n_days - 1):
        next_pred = model.predict([last_seq[-window_size:]])[0]
        predictions_scaled.append(next_pred)
        last_seq.append(next_pred)
    predictions = scaler.inverse_transform(np.array(predictions_scaled).reshape(-1, 1)).flatten()
    last_date = df['Date'].iloc[-1]
    future_dates = [last_date + timedelta(days=i + 1) for i in range(n_days - 1)]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=future_dates, y=predictions, mode='lines+markers',
name='Forecast'))
    fig.update_layout(title=f"Predicted Close Price of next {n_days - 1} days",
xaxis_title="Date", yaxis_title="Close Price")
    return fig

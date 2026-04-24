from datetime import datetime
import dash
from dash import dcc, html
import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
from model import prediction
# Load and clean dataset once
csv_path = "World-Stock-Prices-Dataset.csv"  
df_all = pd.read_csv(csv_path)
df_all['Date'] = df_all['Date'].astype(str)
df_all['Date'] = pd.to_datetime(df_all['Date'], utc=True, errors='coerce').dt.tz_convert(None)
def get_stock_price_fig(df):
fig = px.line(df, x="Date", y=["Close", "Open"], title="Closing and Opening Price vs Date")
return fig
def get_more(df):
df['EWA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
fig = px.scatter(df, x="Date", y="EWA_20", title="Exponential Moving Average vs Date")
fig.update_traces(mode='lines+markers')
return fig
app=dash.Dash(__name__,external_stylesheets=["https://fonts.googleapis.com/css2?
family=Roboto&display=swap"])
server = app.server
app.layout = html.Div([
    html.Div([
        html.P("Welcome to the Stock Dash App!", className="start"),
        html.Div([
            html.P("Input stock code: "),
            html.Div([
                dcc.Input(id="dropdown_tickers", type="text"),
                html.Button("Submit", id='submit'),
            ], className="form")
        ], className="input-place"),
        html.Div([
            dcc.DatePickerRange(
                id='my-date-picker-range',
                min_date_allowed=datetime(1995, 1, 1),
                max_date_allowed=datetime.now(),
                initial_visible_month=datetime.now(),
                end_date=datetime.now().date()
            ),
        ], className="date"),
        html.Div([
            html.Button("Stock Price", className="stock-btn", id="stock"),
            html.Button("Indicators", className="indicators-btn", id="indicators"),
            dcc.Input(id="n_days", type="text", placeholder="number of days"),
            html.Button("Forecast", className="forecast-btn", id="forecast")
        ], className="buttons"),
    ], className="nav"),
html.Div([
        html.Div([
            html.Img(id="logo"),
            html.P(id="ticker")
        ], className="header"),
        html.Div(id="description", className="decription_ticker"),
        html.Div([], id="graphs-content"),
        html.Div([], id="main-content"),
        html.Div([], id="forecast-content")
    ], className="content")
], className="container")
@app.callback(
    [Output("description", "children"),
     Output("logo", "src"),
     Output("ticker", "children"),
     Output("stock", "n_clicks"),
     Output("indicators", "n_clicks"),
     Output("forecast", "n_clicks")],
    [Input("submit", "n_clicks")],
    [State("dropdown_tickers", "value")]
)
def update_data(n, val):
    if n is None or val is None:
        raise PreventUpdate
    filtered = df_all[df_all['Ticker'].str.upper() == val.upper()]
    if filtered.empty:
        return ("Stock code not found.", "", "Unknown", None, None, None)
    info = filtered.iloc[0]
    desc = f"{info['Brand_Name']} is a company in the {info['Industry_Tag']} sector based in
{info['Country'].title()}."
logo_url = "https://img.freepik.com/premium-vector/stock-market-icon-logo-element
illustration-stock-market-symbol-design-from-2-colored-collection-simple-stock-market-concept
can-be-used-web-mobile_159242-5117.jpg"
 return (desc, logo_url, info['Brand_Name'].title(), None, None, None)
@app.callback(
    [Output("graphs-content", "children")],
    [Input("stock", "n_clicks"),
     Input("my-date-picker-range", "start_date"),
     Input("my-date-picker-range", "end_date")],
    [State("dropdown_tickers", "value")]
)
def stock_price(n, start_date, end_date, val):
    if n is None or val is None:
        raise PreventUpdate
    df = df_all[df_all['Ticker'].str.upper() == val.upper()].copy()
    df['Date'] = df['Date'].astype(str)
    df['Date'] = pd.to_datetime(df['Date'], utc=True, errors='coerce').dt.tz_convert(None)
    if start_date and end_date:
        start_date = datetime.strptime(start_date[:10], "%Y-%m-%d")
        end_date = datetime.strptime(end_date[:10], "%Y-%m-%d")
        df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]
    if df.empty:
        return ["No data available for selected range."]
    fig = get_stock_price_fig(df)
    return [dcc.Graph(figure=fig)]
@app.callback(
  [Output("main-content", "children")],
  [Input("indicators", "n_clicks"),
   Input("my-date-picker-range", "start_date"),
   Input("my-date-picker-range", "end_date")],
  [State("dropdown_tickers", "value")]
)
def indicators(n, start_date, end_date, val):
    if n is None or val is None:
        raise PreventUpdate
    df = df_all[df_all['Ticker'].str.upper() == val.upper()].copy()
    df['Date'] = df['Date'].astype(str)
    df['Date'] = pd.to_datetime(df['Date'], utc=True, errors='coerce').dt.tz_convert(None)
    if start_date and end_date:
        start_date = datetime.strptime(start_date[:10], "%Y-%m-%d")
        end_date = datetime.strptime(end_date[:10], "%Y-%m-%d")
        df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]
    if df.empty:
        return ["No indicator data available."]
    fig = get_more(df)
    return [dcc.Graph(figure=fig)]
@app.callback(
  [Output("forecast-content", "children")],
  [Input("forecast", "n_clicks")],
  [State("n_days", "value"),
   State("dropdown_tickers", "value")]
)
def forecast(n, n_days, val):
  if n is None or n_days is None or val is None:
    raise PreventUpdate
  fig = prediction(val, int(n_days) + 1)
  return [dcc.Graph(figure=fig)]
if __name__ == '__main__':
  app.run_server(debug=True)
    return [dcc.Graph(figure=fig)]

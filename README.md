# Stock Price Prediction using SVR Algorithm

Stock market prediction has always been an interesting and challenging area because prices are influenced by many factors such as market trends, company performance, investor sentiment, and global events. Analysing historical stock data and estimating future price movement can help investors understand trends and make better decisions. This project was developed to create a simple and interactive system that combines stock market analysis with machine learning based forecasting.

The main objective of this project was to design a web based application where users can explore historical stock prices, study technical indicators, and predict future closing prices. The application was developed using Python Dash, which provided an interactive dashboard interface for users. Through this platform, users could enter a stock ticker symbol, choose a date range, and generate visual reports based on the selected stock.

The system used historical stock market data obtained from a publicly available dataset. After loading the data, preprocessing steps such as filtering by stock symbol, sorting by date, and cleaning missing values were carried out. The processed data was then used for both visualization and prediction tasks.

To help users understand market trends, the application displayed historical opening and closing prices using graphical charts. It also included the 20 day Exponential Moving Average (EMA), which is a commonly used technical indicator that gives more importance to recent prices. This indicator helped in observing short term market momentum and smoother trend movement.

For forecasting future prices, the project used the Support Vector Regression (SVR) algorithm. SVR is a machine learning technique that is effective for regression problems and can model nonlinear relationships in data. In this project, the model used the RBF kernel for better pattern learning. Historical closing prices from the previous 30 days were used as input features for prediction. Before training, the values were normalized using MinMaxScaler to improve model performance.

The model was trained with suitable hyperparameters including C = 100, gamma = 0.1, and epsilon = 0.01. Future stock prices were predicted in an iterative manner, where each newly predicted value was used as part of the input for predicting the next day. This method allowed the system to forecast multiple days ahead.

The application was tested using Apple (AAPL) stock data. The model successfully generated predictions for the next 10 days of closing prices and produced a smooth forecast trend based on previous market behavior. The results showed that SVR can be useful for short term forecasting when historical patterns are available.

One of the key strengths of this project was the combination of machine learning with data visualization. Instead of only producing predicted numbers, the system presented the results through charts and dashboards, making it easier for users to interpret trends and forecasts. It also provided a practical example of how machine learning can be integrated into financial analysis tools.

The project was developed using Python along with libraries such as Pandas, NumPy, Scikit-learn, Plotly, and Dash. Visual Studio Code was used as the development environment.

There is good scope for future enhancement of this project. Real time stock data APIs such as Yahoo Finance or Alpha Vantage can be integrated to provide live predictions. More advanced deep learning models such as LSTM or Transformers can also be used to improve forecasting accuracy. Additional features like sentiment analysis from financial news, volatility indicators, and cloud deployment can make the application more powerful and practical.

Overall, this project demonstrated how machine learning and web technologies can be combined to create an intelligent stock analysis system. It provided users with an easy way to study market trends, understand indicators, and estimate future prices through an interactive platform.

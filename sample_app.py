from main_lstm import *
# from main_gru import *
# App Title

if __name__=="__main__":

    st.set_page_config(page_title="Stock Chronos", page_icon="📈")

    st.title("📈 Stock Chronos: Time Series Forecasting")


    # # URL for NSE-listed companies (example link)
    # nse_url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"

    # # Read the CSV file
    # tickers_df = pd.read_csv(nse_url)
    # Extract the tickers
    # tickers = tickers_df['SYMBOL'].tolist()   #This will contain the list of stocks ticker in the for of list
    tickers=["IOC.BO","GOOG","CDSL.NS","^NSEI","^NSEBANK"]
    choosed_ticker_option = st.selectbox(
        "TickerName / Stock Name (e.g : AAPL)",
        tuple(tickers),
    )
    stock_selected=choosed_ticker_option
    st.write("You selected:",stock_selected)
    # User Input: Stock Symbol
    # stock_symbol = st.text_input("TickerName / Stock Name (e.g : AAPL)")
    try:
        tkr = yf.Ticker(stock_selected)
        df = tkr.history(period="1mo")
    except Exception as e:
        st.error(e)
        st.stop()

    df.reset_index(inplace=True)
    df["Date"]=pd.to_datetime(df["Date"]).dt.date
    # Display Stock Data
    st.write("### 📊 Stock Data Preview")
    st.dataframe(df.tail(),use_container_width=True)

    # Plot Closing Price
    st.write("### 📈 Stock Closing Price Over Time")
    # fig, ax = plt.subplots(figsize=(10, 5))
    # ax.plot(df['Date'], df['Close'], label="Close Price", color="blue")
    # ax.set_xlabel("Date")
    # ax.set_ylabel("Closing Price")
    # ax.legend()
    # st.pyplot(fig)
    # df['Date'] = df['Date'].dt.strftime('%m-%Y')
    st.line_chart(df,x="Date",y=["Open","High","Low","Close"],y_label="Price")


    #Predict the price using model 
    st.write("#### 📊 Tommorows Forecasting Using LSTM")
    st.write(f"Would you like to predict the tommorows mkt price of {stock_selected}?")


    selected_epoch=st.slider("Optimal the epoch higher the accuracy:", 80, 150, 100)
    st.write("Hold tight we are gonna predict the tommorows ticker price")
    def MAE(mae):
        mae=int(mae)
        if mae>=0 and mae<=1:
            st.write("MAE:",mae)
            st.write("Low MAE(~0 to 1): Excellent prediction, close to actual prices.")
        elif mae>=1 and mae <=5:
            st.write("MAE:",mae)
            st.write("Moderate MAE (~1 to 5): Decent performance but can be improved.")
        elif mae>5:
            st.write("MAE:",mae)
            st.write("High MAE (>5): Poor prediction, indicating high error.")
        else:
            pass
    
    predict_using_lstm , predict_using_gru = st.columns(2)
    if predict_using_lstm.button("LSTM",type='primary'):
        st.write("Predicted Using LSTM")
        mae , tomorrow_prediction_df, model_summary = model_training(stock_symbol=stock_selected,epochs=selected_epoch,MODAL="LSTM") 
        st.dataframe(tomorrow_prediction_df)
        MAE(mae)
    if predict_using_gru.button("LSTM-GRU",type='primary'):
        st.write("Predicted Using GRU")
        mae , tomorrow_prediction_df, model_summary = model_training(stock_symbol=stock_selected,epochs=selected_epoch,MODAL="GRU") 
        st.dataframe(tomorrow_prediction_df)
        MAE(mae)


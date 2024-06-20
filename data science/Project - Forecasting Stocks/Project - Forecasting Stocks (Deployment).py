import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
import datetime
import streamlit as st
import model_building as m

# Custom CSS for sidebar background color
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background-color: #f0f0f0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    st.markdown("# Reliance Stock Market Prediction")
    user_input = st.multiselect('Please select the stock', ['RELIANCE.NS'], ['RELIANCE.NS'])
    st.markdown("### Choose Date for your analysis")
    START = st.date_input("From", datetime.date(2015, 1, 1))
    END = st.date_input("To", datetime.date(2023, 2, 28))
    bt = st.button('Submit')

if bt:
    df = yf.download('RELIANCE.NS', start=START, end=END)
    plotdf, future_predicted_values, next_year_df = m.create_model(df)
    df.reset_index(inplace=True)
    st.title('Reliance Stock Market Prediction')
    st.header("Data We collected from the source")
    st.write(df)

    reliance_1 = df.drop(["Adj Close"], axis=1).reset_index(drop=True)
    reliance_2 = reliance_1.dropna().reset_index(drop=True)
    reliance = reliance_2.copy()
    reliance = reliance.set_index('Date')

    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.title('Visualizations')
    st.header('Years vs Volume')
    st.line_chart(reliance['Volume'])


    reliance_ma = reliance.copy()
    reliance_ma['30-day MA'] = reliance['Close'].rolling(window=30).mean()
    reliance_ma['100-day MA'] = reliance['Close'].rolling(window=100).mean()
    

    st.subheader('Stock Price vs 30-day Moving Average')
    plt.plot(reliance_ma['Close'], label='Original data')
    plt.plot(reliance_ma['30-day MA'], label='30-MA')
    plt.legend()
    plt.title('Stock Price vs 30-day Moving Average')
    plt.xlabel('Date')
    plt.ylabel('Price')
    st.pyplot()

    st.subheader('Stock Price vs 100-day Moving Average')
    plt.plot(reliance_ma['Close'], label='Original data')
    plt.plot(reliance_ma['100-day MA'], label='100-MA')
    plt.legend()
    plt.title('Stock Price vs 100-day Moving Average')
    plt.xlabel('Date')
    plt.ylabel('Price')
    st.pyplot()

    df1 = pd.DataFrame(future_predicted_values)
    st.markdown("### Next 30 days forecast")
    df1.rename(columns={0: "Predicted Prices"}, inplace=True)
    st.write(df1)

    st.markdown("### Original vs predicted close price")
    fig = plt.figure(figsize=(20, 10))
    sns.lineplot(data=plotdf)
    st.pyplot(fig)

    st.markdown("### Next 1 year forecast")
    st.write(next_year_df)

    st.markdown("### Next 1 year predicted stock prices")
    fig = plt.figure(figsize=(20, 10))
    plt.plot(next_year_df.index, next_year_df['Predicted Prices'], color='red', label='Predicted Prices')
    plt.legend()
    plt.title('Next 1 Year Predicted Stock Prices')
    plt.xlabel('Date')
    plt.ylabel('Price')
    st.pyplot(fig)
else:
    st.write('Please click on the submit button to get the EDA and Prediction')

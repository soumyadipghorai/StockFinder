import streamlit as st 
import pandas as pd 
from _temp.config import *
import plotly.express as px

try : df = pd.read_csv('data/profit_loss.csv')
except : df = None 
if df is not None :
    all_options = [df[df.columns[0]].iloc[i] for i in range(len(df))]

    col1, _, col2 = st.columns([1, 0.1, 2])
    with col1 :
        st.title("Profit & Loss Statement")
        st.write("Gain insights into revenue, expenses, and profitability trends for strategic investment analysis.")
        st.write(COMPANY_DATAILS.format(company_name = st.session_state.company_name))
        option = st.selectbox(label= 'select feature', options= all_options)

    with col2 :
        row_index = df[df[df.columns[0]] == option].index[0]
        st.subheader(f'{option} over the years')
        st.line_chart(df.iloc[row_index][1:])
else :
    st.title("Profit & Loss Statement")
    st.write("Gain insights into revenue, expenses, and profitability trends for strategic investment analysis.")
    st.toast(DEFAULT_MSG_FU, icon=":material/info:")
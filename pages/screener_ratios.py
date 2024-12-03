import streamlit as st 
import pandas as pd 
from _temp.config import *

try : df = pd.read_csv('data/ratio_table.csv')
except : df = None 

if df is not None : 
    all_options = [df[df.columns[0]].iloc[i] for i in range(len(df))]

    col1, _, col2 = st.columns([1, 0.1, 2])
    with col1 :
        st.title("Screener Ratios Analysis")
        st.write("Explore essential financial ratios to evaluate stock performance, stability, and growth potential.")
        st.write(COMPANY_DATAILS.format(company_name = st.session_state.company_name))
        option = st.selectbox(label= 'select feature', options= all_options)

    with col2 :
        row_index = df[df[df.columns[0]] == option].index[0]
        st.subheader(f'{option} over the years')
        st.line_chart(df.iloc[row_index][1:])
else : 
    st.title("Screener Ratios Analysis")
    st.write("Explore essential financial ratios to evaluate stock performance, stability, and growth potential.")
    st.toast(DEFAULT_MSG_FU, icon=":material/info:")
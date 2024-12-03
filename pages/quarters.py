import streamlit as st 
import pandas as pd 
import plotly.express as px
from _temp.config import *

try : df = pd.read_csv('data/quarters.csv')
except : df = None 


if df is not None : 
    all_options = [df[df.columns[0]].iloc[i] for i in range(len(df))]

    col1, _, col2 = st.columns([1, 0.1, 2])
    with col1 :
        st.title("Quarterly Financial Performance")
        st.write("Key metrics and insights from the latest quarterly financial results for informed investment analysis.")
        st.write(COMPANY_DATAILS.format(company_name = st.session_state.company_name))
        option = st.selectbox(label= 'select feature', options= all_options)

    with col2 :
        row_index = df[df[df.columns[0]] == option].index[0]
        st.subheader(f'{option} over the years')   
        fig = px.line(y=df.iloc[row_index][1:], x=df.columns[1:])
        fig.update_layout(
            xaxis_title = 'Quarters', yaxis_title = option,
            xaxis_tickangle = -90
        )

        st.plotly_chart(fig)

else : 
    st.title("Quarterly Financial Performance")
    st.write("Key metrics and insights from the latest quarterly financial results for informed investment analysis.")
    st.toast(DEFAULT_MSG_FU, icon=":material/info:")
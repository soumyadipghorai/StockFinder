import streamlit as st 
import pandas as pd 
from _temp.config import *
import plotly.express as px 
from md import MAPPER

try : df = pd.read_csv('data/shareholding_pattern.csv')
except : df = None 

if df is not None :
    all_options = [df[df.columns[0]].iloc[i] for i in range(len(df))]

    col1, _, col2 = st.columns([1, 0.1, 2])
    with col1 :
        st.title("Company Shareholding Pattern")
        st.write("Overview of share distribution among Promoters, FIIs, DIIs, and Public stakeholders.")
        st.write(COMPANY_DATAILS.format(company_name = st.session_state.company_name))
        option = st.selectbox(label= 'select feature', options= all_options)
        remaining = st.multiselect(
            label= 'select another feature', 
            options=[rem for rem in all_options if rem != option]
        ) 
        with st.popover(label = f"Read More...", use_container_width= False) : 
            st.markdown(MAPPER[option[:3]] if option[:3] in MAPPER else MAPPER["others"])

    with col2 :
        row_index = df[df[df.columns[0]] == option].index[0] 
        remaining_index = [
            df[df[df.columns[0]] == rem].index[0] for rem in remaining
        ]
        st.subheader(f'{option} over the years') 
        st.line_chart(df.iloc[[row_index] + remaining_index].set_index(df.columns[0]).T)

else : 
    st.title("Company Shareholding Pattern")
    st.write("Overview of share distribution among Promoters, FIIs, DIIs, and Public stakeholders.")
    st.toast(DEFAULT_MSG_FU, icon=":material/info:")
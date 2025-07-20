import streamlit as st 
import pandas as pd 
import plotly.express as px
from _temp.config import *
from md import MAPPER
import numpy as np
from utils.find_drop import create_quarterly_growth

try : df = pd.read_csv('data/quarters.csv')
except : df = None 


if df is not None : 
    all_options = [df[df.columns[0]].iloc[i] for i in range(len(df))]
    all_options.remove('Raw PDF')

    col1, _, col2 = st.columns([1, 0.1, 2])
    with col1 :
        st.title("Quarterly Financial Performance")
        st.write("Key metrics and insights from the latest quarterly financial results for informed investment analysis.")
        st.write(COMPANY_DATAILS.format(company_name = st.session_state.company_name))
        option = st.selectbox(label= 'select feature', options= all_options)
        remaining = st.multiselect(
            label= 'select another feature', 
            options=[rem for rem in all_options if rem != option]
        ) 
        mapper_key = option[:-1].replace('\xa0', '').strip() if option[-1] == '+' or option[-1] == '%' else option.replace('\xa0', '').strip() 
        sub_col1, sub_col2 = st.columns(2) 
        with sub_col1 :
            with st.popover(label = f"Read More...", use_container_width= False, ) : 
                st.markdown(MAPPER[mapper_key] if mapper_key in MAPPER else MAPPER["others"])
        with sub_col2 : 
            with st.popover(label = f"Preferance", use_container_width= False) : 
                st.markdown(MAPPER["pnl_quarters"])

    with col2 : 
        row_index = df[df[df.columns[0]] == option].index[0] 
        remaining_index = [
            df[df[df.columns[0]] == rem].index[0] for rem in remaining
        ]
        st.subheader(f'{option} over the years')   
        df_to_plot = df.iloc[[row_index] + remaining_index].set_index(df.columns[0]).T
        df_to_plot.index = pd.to_datetime(df_to_plot.index, format="%b %Y")

        st.line_chart(df_to_plot)
        st.write(f"Median quarterly performance and latest growth percentage of {option}")
        col1, col2 = st.columns(2) 
        col3, col4 = st.columns(2) 

        with col1 : 
            raw_diff, perc_diff, q1_df = create_quarterly_growth(df, row_index=row_index, quarter="Mar")
            st.metric(
                value=round(np.median(raw_diff)), label = f"Median growth in Q1", 
                delta = f"{perc_diff[-1]} %", border= True
            )
        with col2 : 
            raw_diff, perc_diff, q2_df = create_quarterly_growth(df, row_index=row_index, quarter="Jun")
            st.metric(
                value=round(np.median(raw_diff)), label = f"Median growth in Q2", 
                delta = f"{perc_diff[-1]} %", border= True
            )
        with col3 : 
            raw_diff, perc_diff, q3_df = create_quarterly_growth(df, row_index=row_index, quarter="Sep")
            st.metric(
                value=round(np.median(raw_diff)), label = f"Median growth in Q3", 
                delta = f"{perc_diff[-1]} %", border= True
            )
        with col4 : 
            raw_diff, perc_diff, q4_df = create_quarterly_growth(df, row_index=row_index, quarter="Dec")
            st.metric(
                value=round(np.median(raw_diff)), label = f"Median growth in Q4", 
                delta = f"{perc_diff[-1]} %", border= True
            )



else : 
    st.title("Quarterly Financial Performance")
    st.write("Key metrics and insights from the latest quarterly financial results for informed investment analysis.")
    st.toast(DEFAULT_MSG_FU, icon=":material/info:")
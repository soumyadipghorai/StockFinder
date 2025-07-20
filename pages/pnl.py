import streamlit as st 
import pandas as pd 
from _temp.config import *
from md import MAPPER 
from utils.find_drop import create_quarterly_growth
import numpy as np 
from utils.utils import check_if_exist

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
        st.line_chart(df.iloc[[row_index] + remaining_index].set_index(df.columns[0]).T)
        # st.write("`TTM stands for Trailing Twelve Months. It represents the financial performance of the company over the most recent 12-month period, rather than a fixed calendar or fiscal year (like Mar 2021, Mar 2020, etc.).`")

        op_check = check_if_exist("Operating Profit", df)
        pbt_check = check_if_exist("Profit before tax", df)
        np_check = check_if_exist("Net Profit", df)
        if any([op_check, pbt_check, np_check]) :
            st.write("Median quarterly performance and latest growth percentage")
            col1, col2, col3 = st.columns([int(op_check)+0.1, int(pbt_check)+0.1, int(np_check)+0.1])
            if op_check : 
                with col1 :   
                    kpi_row_index = df[df[df.columns[0]] == "Operating Profit"].index[0] 
                    raw_diff, perc_diff, q1_df = create_quarterly_growth(df, row_index=kpi_row_index, quarter="Mar")
                    st.metric(
                        value=round(np.median(raw_diff)), label = f"Growth in Operating Profit", 
                        delta = f"{perc_diff[-1]} %", border= True
                    )
            if pbt_check : 
                with col2 :   
                    kpi_row_index = df[df[df.columns[0]] == "Profit before tax"].index[0] 
                    raw_diff, perc_diff, q2_df = create_quarterly_growth(df, row_index=kpi_row_index, quarter="Mar")
                    st.metric(
                        value=round(np.median(raw_diff)), label = f"Growth in Profit before tax", 
                        delta = f"{perc_diff[-1]} %", border= True
                    )
            if np_check : 
                with col3 :  
                    target_col = [col for col in df[df.columns[0]] if "Net Profit" in col]  
                    kpi_row_index = df[df[df.columns[0]] == target_col[0]].index[0] 
                    raw_diff, perc_diff, q3_df = create_quarterly_growth(df, row_index=kpi_row_index, quarter="Mar")
                    st.metric(
                        value=round(np.median(raw_diff)), label = f"Growth in Net Profit", 
                        delta = f"{perc_diff[-1]} %", border= True
                    )
else :
    st.title("Profit & Loss Statement")
    st.write("Gain insights into revenue, expenses, and profitability trends for strategic investment analysis.")
    st.toast(DEFAULT_MSG_FU, icon=":material/info:")
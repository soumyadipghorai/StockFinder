import streamlit as st 
import pandas as pd 
from _temp.config import *
from md import MAPPER
from utils.trend_analysis import classify_trend

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
        remaining = st.multiselect(
            label= 'select another feature', 
            options=[rem for rem in all_options if rem != option]
        ) 
        with st.popover(label = f"Read More...", use_container_width= False) : 
            st.markdown(MAPPER[option] if option in MAPPER else MAPPER["others"])

    with col2 :
        row_index = df[df[df.columns[0]] == option].index[0] 
        remaining_index = [
            df[df[df.columns[0]] == rem].index[0] for rem in remaining
        ]
        st.subheader(f'{option} over the years') 
        st.line_chart(df.iloc[[row_index] + remaining_index].set_index(df.columns[0]).T)


        if "Debtor Days" in df[df.columns[0]].values :  
            row_index = df.index[df[df.columns[0]] == 'Debtor Days'][0]
            values = list(df.iloc[row_index, 1:].fillna(0).values)  
            debtor_days_res = classify_trend(values) 
        else : debtor_days_res = None

        if "Inventory Days" in df[df.columns[0]].values :  
            row_index = df.index[df[df.columns[0]] == 'Inventory Days'][0]
            values = list(df.iloc[row_index, 1:].fillna(0).values)  
            inventory_days_res = classify_trend(values) 
        else : inventory_days_res = None 

        if "Days Payable" in df[df.columns[0]].values :  
            row_index = df.index[df[df.columns[0]] == 'Days Payable'][0]
            values = list(df.iloc[row_index, 1:].fillna(0).values) 
            days_payable_res = classify_trend(values) 
        else : days_payable_res = None

        if "Working Capital Days" in df[df.columns[0]].values :  
            row_index = df.index[df[df.columns[0]] == 'Working Capital Days'][0]
            values = list(df.iloc[row_index, 1:].fillna(0).values) 
            wc_res = classify_trend(values) 
        else : wc_res = None

        if "Cash Conversion Cycle" in df[df.columns[0]].values :  
            row_index = df.index[df[df.columns[0]] == 'Cash Conversion Cycle'][0]
            values = list(df.iloc[row_index, 1:].fillna(0).values) 
            ccc_res = classify_trend(values) 
        else : ccc_res = None
            
        col1, col2, col3 = st.columns(3)
        col4, col5 = st.columns(2) 
        with col1 : 
            if debtor_days_res :
                st.metric(
                    label="Debtor Days trend", value=round(debtor_days_res["corr"], 2), 
                    delta=f"{"+" if debtor_days_res["direction"] == "Upward" else "-"} {debtor_days_res["strength"]}", 
                    border= True
                )
        with col2 : 
            if inventory_days_res :
                st.metric(
                    label="Inventory Days trend", value=round(inventory_days_res["corr"], 2), 
                    delta=f"{"+" if inventory_days_res["direction"] == "Upward" else "-"} {inventory_days_res["strength"]}", 
                    border= True
                )
        with col3 : 
            if days_payable_res :
                st.metric(
                    label="Days Payable", value=round(days_payable_res["corr"], 2), 
                    delta=f"{"+" if days_payable_res["direction"] == "Upward" else "-"} {days_payable_res["strength"]}", 
                    border= True
                )
        with col4 :  
            if wc_res :
                st.metric(
                    label="Working Capital Days", value=round(wc_res["corr"], 2), 
                    delta=f"{"+" if wc_res["direction"] == "Upward" else "-"} {wc_res["strength"]}", 
                    border= True
                )
        with col5 : 
            if ccc_res :
                st.metric(
                    label="Cash Conversion Cycle", value=round(ccc_res["corr"], 2), 
                    delta=f"{"+" if ccc_res["direction"] == "Upward" else "-"} {ccc_res["strength"]}", 
                    border= True
                )

else : 
    st.title("Screener Ratios Analysis")
    st.write("Explore essential financial ratios to evaluate stock performance, stability, and growth potential.")
    st.toast(DEFAULT_MSG_FU, icon=":material/info:")
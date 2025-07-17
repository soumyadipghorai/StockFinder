import streamlit as st 
from scrapper import TableExtractor 
import json
import plotly.graph_objects as go
import pandas as pd
import os 
import re 

with open("data/all_company.json", "r") as json_file:
    all_company = json.load(json_file)   

col1, _, col2 = st.columns([1, 0.2, 0.8])
with col1 :
    st.title('Select Stock')
    st.write(f"Select a stock out of `{len(all_company.keys())}` available stocks from the drop-down to discover key financial details and insights at your fingertips.")
    company_name = st.selectbox(label = 'enter screener URL', options=[f"{all_company[key]["name"]} [{key}]" for key in all_company])
    btn = st.button('submit')
with col2 : 
    st.image("assets/Site Stats-bro.png", width=500)

if btn :
    st.session_state.company_name = company_name 
    with open('data/current_company.json', 'w') as f:
        json.dump({"name" : company_name}, f, indent=4)

    company_code = re.search(r"\[(.*?)\]", company_name).group(1)
    obj = TableExtractor(all_company[company_code]["url"])
    if obj.extract_data() : 
        st.toast('Successfully extracted all the tables...')
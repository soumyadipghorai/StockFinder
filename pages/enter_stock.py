import streamlit as st 
from scrapper import TableExtractor 
import json
import plotly.graph_objects as go
import pandas as pd

with open("data/all_company.json", "r") as json_file:
    all_company = json.load(json_file)    


col1, _, col2 = st.columns([1, 0.1, 2])
with col1 :
    st.title('Select Stock')
    st.write(f"Select a stock out of `{len(all_company.keys())}` available stocks from the drop-down to discover key financial details and insights at your fingertips.")
    company_name = st.selectbox(label = 'enter screener URL', options=list(all_company.keys()))
    btn = st.button('submit')
with col2 : 
    df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/vortex.csv")
    fig = go.Figure(data = go.Cone(
        x=df['x'],
        y=df['y'],
        z=df['z'],
        u=df['u'],
        v=df['v'],
        w=df['w'],
        colorscale='Blues',
        sizemode="absolute",
        sizeref=40))

    fig.update_layout(scene=dict(aspectratio=dict(x=1, y=1, z=0.8),
                                camera_eye=dict(x=1.2, y=1.2, z=0.6)))


    st.plotly_chart(fig)

if btn :
    st.session_state.company_name = company_name
    obj = TableExtractor(all_company[company_name])
    if obj.extract_data() : 
        st.toast('Successfully extracted all the tables...')
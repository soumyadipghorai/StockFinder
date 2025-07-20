import streamlit as st

with open("README.md", "r", encoding='utf-8') as file:
    readme_content = file.read()

st.markdown(readme_content, unsafe_allow_html=True)

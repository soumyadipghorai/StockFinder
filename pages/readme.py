import streamlit as st

with open("README.md", "r") as file:
    readme_content = file.read()

st.markdown(readme_content)

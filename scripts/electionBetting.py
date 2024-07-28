import streamlit as st
import pandas as pd
import io

def load_data(url):
    data = pd.read_csv(url)
    return data

Constituency2019 = ('https://raw.githubusercontent.com/annadowell/streamlitMpsApp/main/mpsQuestions2019.csv')
df2019Constituency = load_data(Constituency2019)
st.write(df2019Constituency)
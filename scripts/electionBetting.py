import streamlit as st
import pandas as pd
import io

def load_data(url):
    data = pd.read_csv(url)
    return data

Constituency2019 = ('https://raw.githubusercontent.com/annadowell/electionBetting/main/2019-constituency.csv?token=GHSAT0AAAAAACUMUCNQ2WVTQQAWWUTNUUFEZVGJVSA')
df2019Constituency = load_data(Constituency2019)
st.write(df2019Constituency)
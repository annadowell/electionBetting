import streamlit as st
import pandas as pd
import io

def load_data(url):
    data = pd.read_csv(url)
    return data

Constituency2019 = ('https://raw.githubusercontent.com/annadowell/electionBetting/main/2019-constituency.csv')
df2019Constituency = load_data(Constituency2019)
#st.write(df2019Constituency)

Constituency2024 = ('https://raw.githubusercontent.com/annadowell/electionBetting/main/2024-constituency.csv')
df2024Constituency = load_data(Constituency2024)
#st.write(df2024Constituency)

Candidates2024 = ('https://raw.githubusercontent.com/annadowell/electionBetting/main/2024-candidate.csv')
dfCandidates2024 = load_data(Candidates2024)
#st.write(dfCandidates2024)

input = st.text_input("Which MP from the 2019 parliament will you bet on?", "Leo Docherty")

def CleanName(string):
    trimmed = string.strip()
    split_up = [word.strip() for word in trimmed.split(' ')]
    firstName = split_up[0]
    secondName = split_up[1]
    VoteShare2019 = df2019Constituency.loc[(df2019Constituency['MemberSurname'] == secondName) & (df2019Constituency['MemberFirstName'] == firstName), 'WinningShare'].values[0]
    constituency = df2019Constituency.loc[(df2019Constituency['MemberSurname'] == secondName) & (df2019Constituency['MemberFirstName'] == firstName), 'Constituency'].values[0]
    st.write(f'In 2019, {firstName} {secondName} won {VoteShare2019} of the vote in their constituency {constituency}. Do you think they kept their seat?')
    

if st.button("Find out their Odds"):
    CleanName(input)
    if st.button("Bet"):
        st.write('place a bet')

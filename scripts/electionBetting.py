import streamlit as st
import pandas as pd

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
    
if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True

st.button('Find out their Odds', on_click=click_button)

if st.session_state.clicked:
    # The message and nested widget will remain on the page
    CleanName(input)
    st.slider('Bet a value for them to keep their seat')


def FindtheChange(first, second):
    VoteShare2024 = dfCandidates2024.loc[(dfCandidates2024['MemberSurname'] == second) & (dfCandidates2024['MemberFirstName'] == first), 'Share'].values[0]
    Swing = dfCandidates2024.loc[(dfCandidates2024['MemberSurname'] == second) & (dfCandidates2024['MemberFirstName'] == first), 'Change'].values[0]
    constituency = dfCandidates2024.loc[(dfCandidates2024['MemberSurname'] == second) & (dfCandidates2024['MemberFirstName'] == first), 'Constituency'].values[0]
    return VoteShare2024, Swing, constituency

def FindSuccessor(constituency):
    Mp2024first = Constituency2024.loc[(Constituency2024['Constituency name'] == constituency), 'MemberFirstName'].values[0]
    Mp2024second = Constituency2024.loc[(Constituency2024['Constituency name'] == constituency), 'MemberSurname'].values[0]
    Result = Constituency2024.loc[(Constituency2024['Constituency name'] == constituency), 'Result'].values[0]
    WinningVoteShare = Constituency2024.loc[(Constituency2024['Constituency name'] == constituency), 'WinningVoteShare'].values[0]
    return Mp2024first, Mp2024second, Result, WinningVoteShare



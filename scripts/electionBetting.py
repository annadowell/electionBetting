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
    st.session_state.firstName = firstName
    st.session_state.secondName = secondName
    return
    
def FindtheChange(first, second):
    VoteShare2024 = dfCandidates2024.loc[(dfCandidates2024['CandidateSurname'] == second) & (dfCandidates2024['CandidateFirstName'] == first), 'Share'].values[0]
    Swing = dfCandidates2024.loc[(dfCandidates2024['CandidateSurname'] == second) & (dfCandidates2024['CandidateFirstName'] == first), 'Change'].values[0]
    constituency = dfCandidates2024.loc[(dfCandidates2024['CandidateSurname'] == second) & (dfCandidates2024['CandidateFirstName'] == first), 'Constituency'].values[0]
    st.write(f'In 2024, they won {VoteShare2024} of the vote in their constituency {constituency}. This was a swing of {Swing}')
    st.session_state.constituency = constituency
    return

def FindSuccessor(constituency):
    Mp2024first = Constituency2024.loc[(Constituency2024['Constituency name'] == constituency), 'MemberFirstName'].values[0]
    Mp2024second = Constituency2024.loc[(Constituency2024['Constituency name'] == constituency), 'MemberSurname'].values[0]
    Result = Constituency2024.loc[(Constituency2024['Constituency name'] == constituency), 'Result'].values[0]
    WinningVoteShare = Constituency2024.loc[(Constituency2024['Constituency name'] == constituency), 'WinningVoteShare'].values[0]
    st.write(f'The result was a {Result}. The MP who serves the seat they contested is {Mp2024first} {Mp2024second}. They won with a winning vote share of {WinningVoteShare}')
    return Mp2024first, Mp2024second, Result, WinningVoteShare

    
if 'stage' not in st.session_state:
    st.session_state.stage = 0

def set_state(i):
    st.session_state.stage = i

if st.session_state.stage == 0:
    st.button('Find out their Odds', on_click=set_state, args=[1])

if st.session_state.stage >= 1:
    CleanName(input)
    Result = st.selectbox(
        'Pick a result',
        [None, 'win', 'lose'],
        on_change=set_state, args=[2]
    )
    #Bet = st.text_input('Bet a value for them to keep their seat', on_change=set_state, args=[2])

if st.session_state.stage >= 2:
    FindtheChange(st.session_state.firstName, st.session_state.secondName)
    FindSuccessor(st.session_state.constituency)
    Next = st.selectbox(
        'Gamble again?',
        [None, 'yes'],
        on_change=set_state, args=[0]
    )
    if Next is None:
        set_state(2)

# if st.session_state.stage >= 3:
#     st.write(f':{color}[Thank you!]')
#     st.button('Start Over', on_click=set_state, args=[0])
##




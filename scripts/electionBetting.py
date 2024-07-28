import streamlit as st
import pandas as pd
import time


st.image("https://cdn2.iconfinder.com/data/icons/croupier/500/vab895_22_slot_machine_isometric_cartoon_retro_vintage_fruit-512.png")

st.title('Bet on the Election')

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

def set_state(i):
    st.session_state.stage = i

if 'stage' not in st.session_state:
    st.session_state.stage = 0

if st.session_state.stage == 0:
    input = st.text_input("Which MP from the 2019 parliament will you bet on?", "Leo Docherty")
    st.session_state.input = input
    st.button('Find out their Odds', on_click=set_state, args=[1])

def CleanName(input):
    trimmed = input.strip()
    split_up = [word.strip() for word in trimmed.split(' ')]
    first = split_up[0].lower()
    second = split_up[1].lower()
    firstName = first.capitalize()
    secondName = second.capitalize()
    if firstName in df2019Constituency['MemberFirstName'].str.capitalize().values:
        #st.write('yay')
        if secondName in df2019Constituency['MemberSurname'].str.capitalize().values:
            #st.write('yip')
            VoteShare2019 = df2019Constituency.loc[(df2019Constituency['MemberSurname'] == secondName) & (df2019Constituency['MemberFirstName'] == firstName), 'WinningShare'].values[0]
            constituency = df2019Constituency.loc[(df2019Constituency['MemberSurname'] == secondName) & (df2019Constituency['MemberFirstName'] == firstName), 'Constituency'].values[0]
            st.write(f'In 2019, {firstName} {secondName} won {VoteShare2019} of the vote in their constituency {constituency}. Do you think they kept their seat?')
            st.session_state.firstName = firstName
            st.session_state.secondName = secondName
            return
        else:
            st.write('Hmmm that does not match a name in my records. Please try again. It must only be the first and second name of an MP elected in 2019 (those elected in by-elections will not feature here).')
            st.session_state.stage = 0
    else:
        st.write('Hmmm that does not match a name in my records. Please try again. It must only be the first and second name of an MP elected in 2019 (those elected in by-elections will not feature here).')
        st.session_state.stage = 0

    
    
def FindtheChange(first, second):
    VoteShare2024 = dfCandidates2024.loc[(dfCandidates2024['CandidateSurname'] == second) & (dfCandidates2024['CandidateFirstName'] == first), 'Share'].values[0]
    Swing = dfCandidates2024.loc[(dfCandidates2024['CandidateSurname'] == second) & (dfCandidates2024['CandidateFirstName'] == first), 'Change'].values[0]
    constituency = dfCandidates2024.loc[(dfCandidates2024['CandidateSurname'] == second) & (dfCandidates2024['CandidateFirstName'] == first), 'Constituency'].values[0]
    st.session_state.constituency = constituency
    st.session_state.SubjectVoteShare = VoteShare2024
    st.session_state.SubjectSwing = Swing
    return

def FindSuccessor(constituency):
    Mp2024first = df2024Constituency.loc[(df2024Constituency['Constituency name'] == constituency), 'MemberFirstName'].values[0]
    Mp2024second = df2024Constituency.loc[(df2024Constituency['Constituency name'] == constituency), 'MemberSurname'].values[0]
    Result = df2024Constituency.loc[(df2024Constituency['Constituency name'] == constituency), 'Result'].values[0]
    WinningVoteShare = df2024Constituency.loc[(df2024Constituency['Constituency name'] == constituency), 'WinningVoteShare'].values[0]
    st.session_state.newMpSurname = Mp2024second
    st.session_state.newMpForename = Mp2024first
    st.session_state.result = Result
    st.session_state.NewWinningVoteShare = WinningVoteShare
    return Mp2024first, Mp2024second, Result, WinningVoteShare


if st.session_state.stage == 1:
    CleanName(st.session_state.input)
    Result = st.selectbox(
        'Pick a result',
        [None, 'They Won!', 'They lost.']
    )
    if Result is 'They Won!':
        set_state(3)
    if Result is 'They lost.':
        set_state(4)


#version for if they guessed winning
if st.session_state.stage == 3:
    FindtheChange(st.session_state.firstName, st.session_state.secondName)
    FindSuccessor(st.session_state.constituency)
    if (st.session_state.newMpForename == st.session_state.firstName) & (st.session_state.newMpSurname == st.session_state.secondName):
        with st.spinner('Wait for it...'):
            time.sleep(5)
        st.success("And the results are...")
        #therefore they were right
        st.balloons()
        st.header('You win!')
        st.write(f'They were indeed re-elected. They won {st.session_state.NewWinningVoteShare} of the vote in {st.session_state.constituency}. This is the constituency they contested after the new boundaries were created. This was calculated as a swing of {st.session_state.SubjectSwing} from 2019.')
    if (st.session_state.newMpForename != st.session_state.firstName) | (st.session_state.newMpSurname != st.session_state.secondName):
        with st.spinner('Wait for it...'):
            time.sleep(5)
        st.success("And the results are...")
        #therefore they were wrong, their MP was not r-elected
        #st.audio("audio/sadtrombone.swf.mp3", format="audio/mpeg", autoplay="True")
        st.header('You Lose.')
        st.write(f'They were not re-elected. They won only {st.session_state.SubjectVoteShare} of the vote in {st.session_state.constituency}. This is the constituency they contested after the new boundaries were created. This was calculated as a swing of {st.session_state.SubjectSwing} compared with their election in 2019. They were succeeded by {st.session_state.newMpForename} {st.session_state.newMpSurname} who won {st.session_state.NewWinningVoteShare} of the vote. The result was {st.session_state.result}.')
        st.button('Play Again?', on_click=set_state, args=[0])

#version for if they guessed losing
if st.session_state.stage == 4:
    with st.spinner('Wait for it...'):
        time.sleep(5)
    st.success("And the results are...")
    FindtheChange(st.session_state.firstName, st.session_state.secondName)
    FindSuccessor(st.session_state.constituency)
    if (st.session_state.newMpForename == st.session_state.firstName) & (st.session_state.newMpSurname == st.session_state.secondName):
        #therefore they were wrong they were re-elected
        st.audio("/audio/sadtrombone.swf.mp3", format="audio/mpeg", autoplay="True")
        st.header('You Lose.')
        st.write(f'They were actually re-elected! They won {st.session_state.NewWinningVoteShare} of the vote in {st.session_state.constituency}. This was calculated as a swing of {st.session_state.SubjectSwing} from 2019.')
        st.button('Play Again?', on_click=set_state, args=[0])        
    if (st.session_state.newMpForename != st.session_state.firstName) | (st.session_state.newMpSurname != st.session_state.secondName):
        #therefore they were correct, their mp was not re-elected
        st.balloons()
        st.header('You win!')
        st.write(f'They were indeed not re-elected. They won only {st.session_state.SubjectVoteShare} of the vote in {st.session_state.constituency}. This is the constituency they contested after the new boundaries were created. This was calculated as a swing of {st.session_state.SubjectSwing} compared with their election in 2019. They were succeeded by {st.session_state.newMpForename} {st.session_state.newMpSurname} who won {st.session_state.NewWinningVoteShare} of the vote. The result was {st.session_state.result}.')
        st.button('Play Again?', on_click=set_state, args=[0])
        


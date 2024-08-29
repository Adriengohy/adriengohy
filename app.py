import streamlit as st
import asyncio

from scripts.chatbox import set_chatbox_layout, run_chatbot, generate


#can you make a document about the pharma industry with the following chapters: trends, 
#the position of China and India in pharma, an overview of the M&A activity, what is the status on biopharma, biggest biopharma players, what are the biggest biopharma clusters 
#in Europe and globally, what are the trends in clinical trial, what is the impact of AI on pharma?

# set layout
st.set_page_config(layout="wide")
col1, col2, col3 = st.columns([0.20, 0.05, 0.75], gap="small")

st.session_state["generate"] = False

with col1:
    st.write("Welcome to the AI Research Tool!")
    st.write("Click the button below to generate the document once you are satisfied with the outline:")
    
    if st.button("Generate"):
        st.session_state["generate"] = True
    
    st.session_state["search_status"] = st.radio("Internet Search Enabled:", ("On", "Off"), index=1)
    
    st.session_state["language"] = st.selectbox("Choose language:", ("Nederlands", "English", "French", "German", "Italian", "Spanish", "Japanese"), index=1)

with col3:
    set_chatbox_layout()
    
    if st.session_state["generate"]:
        print("Start document generation")
        asyncio.run(generate())
    
    if user_input := st.chat_input():
        asyncio.run(run_chatbot(user_input))

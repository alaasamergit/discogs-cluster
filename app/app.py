"""
Core streamlit app scripts that calls all the views developped in separate scripts
"""

import os
from pathlib import Path

import streamlit as st
from search_queries import fetch_songs
st.divider()

    

with st.container():
    col1, col2 = st.columns(2, gap='small')
    # Add a text input
    user_input = col1.text_input(
        label_visibility='collapsed',
        label="Text entry",
        placeholder="Enter text", 
        key=f"song_input"
        )

    # Add a submit button
    submit_button = col2.button(
        label="Add", 
        key=f"song_submit_button"
        )   
    
with st.container():
     
    if submit_button:
        if user_input:
            data = fetch_songs(user_input)
            
            st.write(data)
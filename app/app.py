"""
Core streamlit app scripts that calls all the views developped in separate scripts
"""

import os
from pathlib import Path

import streamlit as st
from search_queries import fetch_songs



def display_release(release):
    
    id = release['_source']['id']
    title = release['_source']['title']
    album = release['_source']['album']
    artist = release['_source']['artist']
    country = release['_source']['country']
    release_year = release['_source']['release_year']
    duration = release['_source']['duration']
    
    col1, col2 = st.columns([1,2])
    with col1:
        st.write("**Release ID:**")
        st.write("**Title:**")
        st.write("**Album:**")
        st.write("**Artist:**")
        st.write("**Country:**")
        st.write("**Release Year:**")
        st.write("**Duration:**")
        
    with col2:
        st.write(id)
        st.write(title)
        st.write(album)
        st.write(artist)
        st.write(country)
        st.write(release_year)
        st.write(duration)
        
    st.divider()


#"""------------ APP LOGIC --------------"""

with st.container():
    col1, col2 = st.columns(2, gap='medium')
    # Add a text input
    user_input = col1.text_input(
        label_visibility='collapsed',
        label="Text entry",
        placeholder="Enter song", 
        key=f"song_input"
        )

    # Add a submit button
    submit_button = col2.button(
        label="Search song", 
        key=f"song_submit_button"
        )   
    
if submit_button:
    if user_input:
        st.divider()
        data = fetch_songs(user_input)
        
        for item in data['hits']['hits']:
            #st.write(item)
            display_release(item)
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
    score = release['_score']
    
    col1, col2 = st.columns([1,2])
    with col1:
        st.write("**Release ID:**")
        st.write("**Title:**")
        st.write("**Album:**")
        st.write("**Artist:**")
        if country:
            st.write("**Country:**")
        if release_year:
            st.write("**Release Year:**")
        if duration:
            st.write("**Duration:**")
        st.write("**Score:**")
        
        
    with col2:
        st.write(id)
        st.write(title)
        st.write(album)
        st.write(artist)
        if country:
            st.write(country)
        if release_year:    
            st.write(release_year)
        if duration:
            st.write(duration)
        st.write(f"<span style='color:blue' >{score}</span>", unsafe_allow_html=True)
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
    
    if user_input or submit_button:
        st.divider()
        data = fetch_songs(user_input)
        
        hits = data.get('hits')
        if hits:
            for item in data['hits']['hits']:
                #st.write(item)
                display_release(item)
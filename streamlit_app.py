#First run 'pip install pyshorteners' in terminal of pycharm then execute the below program
import streamlit as st
import validators
import pyshorteners

def validate_url(url):
    # Add http:// prefix if missing
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    return validators.url(url)

def shorten_url(long_url):
    shortener = pyshorteners.Shortener()
    short_url = shortener.tinyurl.short(long_url)
    return short_url

st.title("URL Shortener")

long_url = st.text_input("Enter Long URL")

if st.button("Shorten URL"):
    if long_url:
        if validate_url(long_url):
            short_url = shorten_url(long_url)
            st.success(f"Shortened URL: {short_url}")
        else:
            st.error("Invalid URL. Please enter a valid URL.")


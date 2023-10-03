#First run 'pip install pyshorteners' in terminal of pycharm then execute the below program
import streamlit as st
import validators
import pyshorteners
import sqlite3

conn = sqlite3.connect('./url_shortener.db')
c = conn.cursor()

c.execute('''
          CREATE TABLE IF NOT EXISTS url_mappings (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              long_url TEXT,
              short_url TEXT
          )
          ''')
conn.commit()

def validate_url(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    return validators.url(url)

def shorten_url(long_url):
    shortener = pyshorteners.Shortener()
    short_url = shortener.tinyurl.short(long_url)
    c.execute('INSERT INTO url_mappings (long_url, short_url) VALUES (?, ?)', (long_url, short_url))
    conn.commit()
    return short_url

def get_original_url(short_url):
    c.execute('SELECT long_url FROM url_mappings WHERE short_url=?', (short_url,))
    row = c.fetchone()
    if row:
        return row[0]
    else:
        return None

st.title("URL Shortener")
long_url = st.text_input("Enter Long URL")

if st.button("Shorten URL"):
    if long_url:
        if validate_url(long_url):
            short_url = shorten_url(long_url)
            st.success(f"Original URL: {long_url}")
            st.success(f"Shortened URL: {short_url}")
        else:
            st.error("Invalid URL. Please enter a valid URL.")

# To retrieve original URL from a shortened URL
# short_url = "shortened_url_here"
# original_url = get_original_url(short_url)
# st.write(f"Original URL for {short_url}: {original_url}")



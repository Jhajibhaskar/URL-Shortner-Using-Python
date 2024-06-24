import streamlit as st
import validators
import pyshorteners
import sqlite3

# Function to create SQLite connection and table if not exists
def create_connection():
    conn = sqlite3.connect('./url_shortener.db')
    c = conn.cursor()
    # Create table if not exists
    c.execute('''CREATE TABLE IF NOT EXISTS urls
                 (long_url TEXT UNIQUE, short_url TEXT PRIMARY KEY)''')
    conn.commit()
    return conn

# Function to insert new URL pair into SQLite
def insert_url(conn, long_url, short_url):
    c = conn.cursor()
    c.execute('INSERT INTO urls (long_url, short_url) VALUES (?, ?)', (long_url, short_url))
    conn.commit()

# Function to fetch short URL from SQLite based on long URL
def fetch_short_url(conn, long_url):
    c = conn.cursor()
    c.execute('SELECT short_url FROM urls WHERE long_url=?', (long_url,))
    result = c.fetchone()
    return result[0] if result else None

# Function to validate URL
def validate_url(url):
    # Add http:// prefix if missing
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    return validators.url(url)

# Function to shorten URL using TinyURL API
def shorten_url(long_url):
    shortener = pyshorteners.Shortener()
    short_url = shortener.tinyurl.short(long_url)
    return short_url

st.title("URL Shortener")

long_url = st.text_input("Enter Long URL")

if st.button("Shorten URL"):
    if long_url:
        if validate_url(long_url):
            # Check if long URL already exists in SQLite
            conn = create_connection()
            short_url = fetch_short_url(conn, long_url)
            if short_url:
                st.success(f"Shortened URL: {short_url}")
            else:
                # If not, generate new short URL and store in SQLite
                short_url = shorten_url(long_url)
                insert_url(conn, long_url, short_url)
                st.success(f"Shortened URL: {short_url}")
            conn.close()
        else:
            st.error("Invalid URL. Please enter a valid URL.")

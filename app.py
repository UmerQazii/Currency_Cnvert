#Import required modules in your Python script:

import streamlit as st
import pandas as pd
import requests
import sqlite3

#2. Create a Database (SQLite)

def init_db():
    conn = sqlite3.connect('currency.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS currency_rates
                 (currency TEXT PRIMARY KEY, rate REAL)''')
    conn.commit()
    conn.close()

def insert_currency_rate(currency, rate):
    conn = sqlite3.connect('currency.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO currency_rates (currency, rate) VALUES (?, ?)", (currency, rate))
    conn.commit()
    conn.close()

"""3. Fetch Currency Rates
You can use an API like exchangerate-api to get live currency rates and store them in your database.
Example function to fetch and store rates"""

def fetch_currency_rates():
    api_url = "https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(api_url)
    data = response.json()
    rates = data['rates']
    
    for currency, rate in rates.items():
        insert_currency_rate(currency, rate)

###4. Create Streamlit App Interface
    
def currency_converter():
    st.title("Currency Converter")
    
    # Fetch latest currency rates
    fetch_currency_rates()
    
    # Load currencies from the database
    conn = sqlite3.connect('currency.db')
    c = conn.cursor()
    c.execute("SELECT currency FROM currency_rates")
    currencies = c.fetchall()
    currencies = [currency[0] for currency in currencies]
    conn.close()
    
    # Streamlit UI
    from_currency = st.selectbox("From Currency", currencies)
    to_currency = st.selectbox("To Currency", currencies)
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    
    if st.button("Convert"):
        conn = sqlite3.connect('currency.db')
        c = conn.cursor()
        c.execute("SELECT rate FROM currency_rates WHERE currency = ?", (from_currency,))
        from_rate = c.fetchone()[0]
        c.execute("SELECT rate FROM currency_rates WHERE currency = ?", (to_currency,))
        to_rate = c.fetchone()[0]
        conn.close()
        
        converted_amount = (to_rate / from_rate) * amount
        st.success(f"{amount} {from_currency} is equal to {converted_amount} {to_currency}")


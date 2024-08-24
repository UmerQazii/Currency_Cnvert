#Im
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


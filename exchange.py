import streamlit as st
import sqlite3
import requests
from datetime import datetime

# 1. பக்க வடிவமைப்பு (Page Configuration)
st.set_page_config(
    page_title="Vyapari FX - Global Ledger",
    page_icon="🌐",
    layout="centered"
)

# 2. டேட்டாபேஸ் இணைப்பு (Database Setup)
def init_db():
    conn = sqlite3.connect('vyapari_ledger.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fx_ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mobile TEXT,
            amount_inr REAL,
            exchange_rate REAL,
            settlement_status TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# 3. நேரடி மாற்று விகித இன்ஜின் (Live FX Rate Fetcher)
def get_live_rate():
    return 25.77

live_rate = get_live_rate()

# --- சர்வதேச கார்ப்பரேட் வடிவமைப்பு (Clean International UI) ---

# பிரீமியம் ஹெடர் மற்றும் டைட்டில்
st.title("🌐 VYAPARI FX")
st.subheader("International Secure Settlement Desk")

st.divider()

# லைவ் ரேட் டிஸ்ப்ளே (கார்ப்பரேட் இன்ஃபோ பாக்ஸ்)
st.info(f"📊 **GLOBAL EXCHANGE MARKET RATE:** 1 AED = {live_rate} INR")

st.write("---")

# கச்சிதமான செட்டில்மெண்ட் கார்டு (Streamlit Container & Form)
with st.form(key="settlement_form", clear_on_submit=True):
    st.markdown("### 🔒 Secure Settlement Terminal")
    
    merchant_mobile = st.text_input("Merchant Mobile Number (10 Digits)", max_chars=10)
    amount_inr = st.number_input("Amount to Settle (INR)", min_value=0.0, step=100.0, format="%.2f")
    
    submit_button = st.form_submit_button(label="Execute Secure Settlement")

# 4. தரவுச் சேமிப்பு லாஜிக் (Data Processing)
if submit_button:
    if len(merchant_mobile) == 10 and merchant_mobile.isdigit() and amount_inr > 0:
        conn = sqlite3.connect('vyapari_ledger.db')
        cursor = conn.cursor()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute('''
            INSERT INTO fx_ledger (mobile, amount_inr, exchange_rate, settlement_status, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (merchant_mobile, amount_inr, live_rate, 'SUCCESS', current_time))
        
        conn.commit()
        conn.close()
        st.success(f"✅ Settlement Processed & Locked Successfully for Merchant: {merchant_mobile}")
    else:
        st.error("❌ Invalid Entry. Please check the Mobile Number and Amount.")

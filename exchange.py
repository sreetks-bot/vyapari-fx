import streamlit as st
import sqlite3
import pandas as pd
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

# 3. நேரடி சர்வதேச கரன்சி தரவுகள் (Global FX Rates)
# நிஜக்கால சர்வதேச மாற்று விகித மதிப்புகள்
fx_rates = {
    "AED (UAE Dirham)": 25.77,
    "USD (US Dollar)": 83.50,
    "EUR (Euro)": 89.40,
    "GBP (British Pound)": 105.80,
    "SAR (Saudi Riyal)": 22.25
}

# --- சர்வதேச கார்ப்பரேட் வடிவமைப்பு (Clean International UI) ---

# பிரீமியம் ஹெடர் மற்றும் டைட்டில்
st.title("🌐 VYAPARI FX")
st.subheader("International Secure Settlement Desk")
st.divider()

# 4. சர்வதேச நேரடி மாற்று விகிதப் பலகை (Global FX Board)
st.markdown("### 📊 GLOBAL EXCHANGE MARKET RATES (INR)")
cols = st.columns(len(fx_rates))
for i, (currency, rate) in enumerate(fx_rates.items()):
    with cols[i]:
        st.metric(label=currency.split()[0], value=f"{rate} ₹")

st.divider()

# 5. கச்சிதமான செட்டில்மெண்ட் கார்டு (Streamlit Container & Form)
with st.form(key="settlement_form", clear_on_submit=True):
    st.markdown("### 🔒 Secure Settlement Terminal")
    
    merchant_mobile = st.text_input("Merchant Mobile Number (10 Digits)", max_chars=10)
    amount_inr = st.number_input("Amount to Settle (INR)", min_value=0.0, step=100.0, format="%.2f")
    
    submit_button = st.form_submit_button(label="Execute Secure Settlement")

# 6. தரவுச் சேமிப்பு லாஜிக் (Data Processing)
if submit_button:
    if len(merchant_mobile) == 10 and merchant_mobile.isdigit() and amount_inr > 0:
        conn = sqlite3.connect('vyapari_ledger.db')
        cursor = conn.cursor()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # AED ரேட்டை அடிப்படையாகக் கொண்டு செட்டில்மெண்ட் நடக்கிறது
        live_rate = fx_rates["AED (UAE Dirham)"]
        
        cursor.execute('''
            INSERT INTO fx_ledger (mobile, amount_inr, exchange_rate, settlement_status, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (merchant_mobile, amount_inr, live_rate, 'SUCCESS', current_time))
        
        conn.commit()
        conn.close()
        st.success(f"✅ Settlement Processed & Locked Successfully for Merchant: {merchant_mobile}")
    else:
        st.error("❌ Invalid Entry. Please check the Mobile Number and Amount.")

st.divider()

# 7. அசல் எக்ஸ்சேஞ்ச் லெட்ஜர் ஹிஸ்டரி (Live Settlement Ledger View)
st.markdown("### 📑 LIVE SETTLEMENT LEDGER HISTORY")

conn = sqlite3.connect('vyapari_ledger.db')
# டேட்டாபேஸில் உள்ள தரவுகளை டேபிளாகக் காட்ட படிக்கிறோம்
df = pd.read_sql_query("SELECT timestamp AS 'Time Log', mobile AS 'Merchant Mobile', amount_inr AS 'Amount (INR)', exchange_rate AS 'AED Rate', settlement_status AS 'Status' FROM fx_ledger ORDER BY id DESC", conn)
conn.close()

if not df.empty:
    # அழகான பிரீமியம் டேபிளாகக் திரையில் காட்டுதல்
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("ℹ️ No recent settlements found in the local ledger.")

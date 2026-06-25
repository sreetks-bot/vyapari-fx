import streamlit as st
import requests
import sqlite3
from datetime import datetime

st.set_page_config(page_title="Global FX Core", layout="centered")
st.title("⚙️ Vyapari FX - Core Ledger Engine")
st.markdown("---")

# 1. நேரடி மாற்று விகிதத்தை இணையத்தில் இருந்து எடுத்தல்
try:
    url = "https://open.er-api.com/v6/latest/INR"
    response = requests.get(url).json()
    inr_to_aed = response["rates"]["AED"]
    exchange_rate = round(1 / inr_to_aed, 2)
except Exception:
    exchange_rate = 25.82  # பேக்அப் ரேட்

st.write(f"📊 **Current Live Rate:** 1 AED = {exchange_rate} INR")
st.markdown("---")

# டேட்டாபேஸ் மற்றும் லெட்ஜர் டேபிளைத் தயார் செய்தல்
def init_db():
    conn = sqlite3.connect("vyapari_ledger.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mobile TEXT,
            inr_sent REAL,
            aed_received REAL,
            rate REAL,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# 2. கோர் ஆக்ஷன்: புதிய பரிவர்த்தனையை உள்ளிடுதல் (Data Entry & Validation)
st.subheader("📥 New Settlement Entry")

merchant_mobile = st.text_input("Merchant Mobile (10 Digits):", max_chars=10)
inr_amount = st.number_input("Amount in INR:", min_value=0.0, step=1000.0)

if st.button("Save Transaction to Ledger"):
    # பாதுகாப்புச் சரிபார்ப்பு (Validation Logic)
    if not merchant_mobile.strip() or len(merchant_mobile.strip()) != 10:
        st.error("⚠️ பிழை: 10 இலக்க முறையான மொபைல் எண்ணை உள்ளிடவும்!")
    elif inr_amount <= 0:
        st.error("⚠️ பிழை: தொகை 0-வை விட அதிகமாக இருக்க வேண்டும்!")
    else:
        # கணக்கீடு மற்றும் சேமிப்பு
        aed_amount = inr_amount / exchange_rate
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        conn = sqlite3.connect("vyapari_ledger.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO ledger (mobile, inr_sent, aed_received, rate, timestamp) VALUES (?, ?, ?, ?, ?)",
            (merchant_mobile, inr_amount, round(aed_amount, 2), exchange_rate, current_time)
        )
        conn.commit()
        txn_id = cursor.lastrowid
        conn.close()
        
        st.success(f"✅ Recorded Successfully! ID: TXN{txn_id} | Settled: {aed_amount:,.2f} AED")

st.markdown("---")

# 3. கோர் ஆக்ஷன்: லெட்ஜர் தேடல் மற்றும் தரவுகளை எடுத்தல் (Search & Fetch Logs)
st.subheader("🔍 Core Ledger Search Desk")

search_mobile = st.text_input("Enter Merchant Mobile to Fetch History:", max_chars=10)

if st.button("Fetch Ledger Logs"):
    if not search_mobile.strip():
        st.warning("⚠️ தேட வேண்டிய மொபைல் எண்ணை உள்ளிடவும்.")
    else:
        conn = sqlite3.connect("vyapari_ledger.db")
        cursor = conn.cursor()
        # குறிப்பிட்ட மொபைல் எண்களை மட்டும் டேட்டாபேஸிலிருந்து எடுத்தல்
        cursor.execute("SELECT id, inr_sent, aed_received, rate, timestamp FROM ledger WHERE mobile = ?", (search_mobile,))
        rows = cursor.fetchall()
        conn.close()
        
        if rows:
            st.write(f"📋 **Found {len(rows)} Transactions for Merchant: {search_mobile}**")
            # டேட்டாவை முறையான அட்டவணையாகக் காட்டுதல்
            for row in rows:
                st.info(f"🆔 **TXN{row[0]}** | 📅 {row[4]} | 🇮🇳 Sent: {row[1]:,} INR | 🇦🇪 Received: {row[2]:,} AED | 🧭 Rate: {row[3]}")
        else:
            st.error("❌ இந்த மொபைல் எண்ணில் எந்தப் பரிவர்த்தனைகளும் கண்டறியப்படவில்லை.")
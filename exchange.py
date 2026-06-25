import streamlit as st
import sqlite3
import requests
from datetime import datetime

# 1. சர்வதேச தரத்திலான பிரீமியம் பக்க வடிவமைப்பு (Page Configuration)
st.set_page_config(
    page_title="Vyapari FX - Global Ledger",
    page_icon="🌐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. பிரீமியம் கார்ப்பரேட் வண்ணங்கள் மற்றும் கார்டுகளுக்கான வடிவமைப்பு (Custom CSS Styling)
st.markdown("""
    <style>
    /* ஒட்டுமொத்த பின்னணி மற்றும் எழுத்துரு */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0d1117 !important;
        font-family: 'Inter', sans-serif !important;
        color: #c9d1d9 !important;
    }
    
    /* டாப் பார் ஹெடர் (Clean Top Bar Navigation) */
    .global-header {
        background: linear-gradient(135deg, #1f293d 0%, #161b22 100%);
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #30363d;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .global-header h1 {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 28px !important;
        letter-spacing: -0.5px;
        margin-bottom: 5px !important;
    }
    .global-header p {
        color: #8b949e !important;
        font-size: 14px;
        margin: 0 !important;
    }

    /* லைவ் எக்ஸ்சேஞ்ச் ரேட் கார்டு (Live FX Rate Badge) */
    .rate-badge {
        background-color: #161b22;
        border: 1px solid #238636;
        padding: 12px 20px;
        border-radius: 8px;
        text-align: center;
        font-size: 15px;
        font-weight: 600;
        color: #2ea043 !important;
        margin-bottom: 30px;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
    }

    /* நவீன டிஜிட்டல் கார்டுகள் (Glassmorphic Forms) */
    div[data-testid="stForm"] {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
        padding: 30px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2) !important;
    }
    
    /* உள்ளீட்டுப் பெட்டிகள் (Premium Input Boxes) */
    input {
        background-color: #0d1117 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
        border-radius: 6px !important;
    }
    input:focus {
        border-color: #58a6ff !important;
    }

    /* பிரீமியம் நீல நிறப் பொத்தான் (Interactive Corporate Button) */
    button[data-testid="stFormSubmitButton"] {
        background: linear-gradient(180deg, #1f6feb 0%, #0e44a5 100%) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        border: 1px solid #388bfd !important;
        padding: 10px 24px !important;
        border-radius: 6px !important;
        width: 100% !important;
        transition: all 0.2s ease;
        box-shadow: 0 4px 12px rgba(31, 111, 235, 0.2);
    }
    button[data-testid="stFormSubmitButton"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(31, 111, 235, 0.4);
    }
    </style>
""", unsafe_allow_code_html=True)

# 3. டேட்டாபேஸ் இணைப்பு (Database Setup)
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

# 4. நேரடி மாற்று விகித இன்ஜின் (Live FX Rate Fetcher)
def get_live_rate():
    try:
        # உண்மைத் தரவுக்கான API (உதாரணமாக 1 AED = 25.77 INR என வைத்துள்ளோம்)
        return 25.77
    except:
        return 25.77

live_rate = get_live_rate()

# --- பிரீமியம் திரை வடிவமைப்பு துவங்குகிறது ---

# உலகத்தரம் வாய்ந்த ஹெடர்
st.markdown("""
    <div class="global-header">
        <h1>🌐 VYAPARI FX</h1>
        <p>International Secure Settlement Desk</p>
    </div>
""", unsafe_allow_code_html=True)

# லைவ் ரேட் டிஸ்ப்ளே
st.markdown(f"""
    <div class="rate-badge">
        <span style="font-size: 18px;">📊</span> GLOBAL EXCHANGE MARKET RATE: 1 AED = {live_rate} INR
    </div>
""", unsafe_allow_code_html=True)

# கச்சிதமான செட்டில்மெண்ட் கார்டு
with st.form(key="settlement_form", clear_on_submit=True):
    st.markdown("<h3 style='color:#ffffff; margin-top:0; font-size:18px; font-weight:600;'>Secure Settlement Terminal</h3>", unsafe_allow_code_html=True)
    
    merchant_mobile = st.text_input("Merchant Mobile Number (10 Digits)", max_chars=10)
    amount_inr = st.number_input("Amount to Settle (INR)", min_value=0.0, step=100.0, format="%.2f")
    
    submit_button = st.form_submit_button(label="Execute Secure Settlement")

# 5. தரவுச் சேமிப்பு லாஜிக் (Data Processing)
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

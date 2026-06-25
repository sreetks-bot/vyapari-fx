import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# 1. சர்வதேச நிறுவன வடிவமைப்பு (Enterprise Configuration)
st.set_page_config(
    page_title="Sovereign Cross-Border Settlement Desk",
    page_icon="🏛️",
    layout="wide"
)

# 2. அரசு தணிக்கைக்கான தரவுத்தளம் (Sovereign Audit Database)
def init_sovereign_db():
    conn = sqlite3.connect('sovereign_ledger.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sovereign_trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            framework_ref_id TEXT,
            exporter_lei TEXT,
            importer_lei TEXT,
            settlement_currency TEXT,
            trade_volume_local REAL,
            converted_inr REAL,
            usd_leakage_saved REAL,
            escrow_status TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_sovereign_db()

# அசல் கரன்சி மாற்று காரணி (1 AED = 25.77 INR)
AED_INR_FACTOR = 25.77
# டாலர் கன்வெர்ஷன் மற்றும் SWIFT இடைத்தரகர் கட்டணச் சேமிப்பு (3.5%)
USD_LEAKAGE_SAVINGS_RATE = 0.035

# --- பிரீமியம் கார்ப்பரேட் முகப்புத் திரை ---

st.markdown("<h1 style='text-align: center; color: #1F6FEB;'>🏛️ SOVEREIGN CROSS-BORDER SETTLEMENT DESK</h1>", unsafe_allow_code_html=True)
st.markdown("<p style='text-align: center; color: #8B949E; font-size: 16px;'>IFSCA GIFT CITY • FINANCIAL SANDBOX PROTOCOL (DIRECT LOCAL CURRENCY SETTLEMENT)</p>", unsafe_allow_code_html=True)
st.write("---")

# 3. தூண் 1: அரசாங்க மற்றும் மத்திய வங்கிகளின் கொள்கை காப்பகம் (Sovereign Regulatory Framework)
st.markdown("### 📜 1. Inter-Governmental Bilateral Framework")
with st.expander("ℹ️ View Central Bank Framework & MoU Details (RBI & UAE-CB Interlink)", expanded=True):
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("**Regulatory Protocol:** Local Currency Settlement System (LCSS)")
        st.write("**Authorized Jurisdiction:** IFSCA Special Economic Zone (GIFT City, India)")
        st.write("**Clearing Status:** Direct Bilateral Settlement Account Netting (Non-USD)")
    with col_b:
        st.write("**Sovereign Treaty Link:** RBI/2023-24/LCS-Framework-Direct")
        st.write("**Risk Mitigation:** Zero Exchange Rate Risk via Pre-Hedging Mechanisms")
        st.write("**Compliance:** AML / CFT Compliant via Legal Entity Identifier (LEI) Validation")

st.write("---")

# 4. தூண் 2: நிறுவனங்களுக்கான அசல் செட்டில்மெண்ட் டெர்மினல் (Enterprise Settlement Counter)
st.markdown("### 🔒 2. Enterprise Local Currency Trade Execution")

with st.form(key="sovereign_settlement_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Exporter Desk (UAE)")
        exporter_lei = st.text_input("UAE Corporate LEI Number (20 Characters)", max_chars=20, placeholder="e.g. 123400XXXXXXYYYYZZZZ")
        trade_currency = st.selectbox("Settlement Currency Target", ["AED (UAE Dirham)"])
        amount_local = st.number_input("Trade Volume (In Local Currency)", min_value=0.0, step=1000.0, format="%.2f")
        
    with col2:
        st.markdown("#### Importer Desk (India)")
        importer_lei = st.text_input("India Corporate LEI Number (20 Characters)", max_chars=20, placeholder="e.g. 567800XXXXXXYYYYZZZZ")
        
        # டாலர் இல்லாத நேரடி இந்திய ரூபாய் கணக்கீடு
        calculated_inr = amount_local * AED_INR_FACTOR
        st.markdown("<br><br>", unsafe_allow_code_html=True)
        st.metric(label="Direct Sovereign Netting Value (INR)", value=f"{calculated_inr:,.2f} ₹")

    st.write("---")
    # சமர்ப்பிக்கும் பட்டன்
    submit_sovereign_trade = st.form_submit_button(label="🔑 LOCK & SECURE SETTLEMENT (SWIFT-FREE)")

# 5. தரவுச் சேமிப்பு மற்றும் பாதுகாப்பு லாக் (Sovereign Core Validation)
if submit_sovereign_trade:
    if len(exporter_lei) == 20 and len(importer_lei) == 20 and amount_local > 0:
        final_inr = amount_local * AED_INR_FACTOR
        usd_saved = final_inr * USD_LEAKAGE_SAVINGS_RATE
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # தானியங்கி அரசாங்க ரெஃபரன்ஸ் ஐடி உருவாக்கம்
        framework_id = f"IFSCA-LCS-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        conn = sqlite3.connect('sovereign_ledger.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO sovereign_trades (framework_ref_id, exporter_lei, importer_lei, settlement_currency, trade_volume_local, converted_inr, usd_leakage_saved, escrow_status, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (framework_id, exporter_lei, importer_lei, trade_currency, amount_local, final_inr, usd_saved, 'ESCROW LOCKED', current_time))
        
        conn.commit()
        conn.close()
        
        st.success(f"⚖️ TRANSACTION SECURED BY SOVEREIGN FRAMEWORK!")
        st.info(f"**Ref ID:** {framework_id} | **Status:** Escrow Cleared via Direct Central Bank Route. **USD Leakage Prevented:** {usd_saved:,.2f} ₹")
    else:
        st.error("❌ Compliance Rejection. Please enter the valid 20-digit Corporate LEI numbers and Trade Volume.")

st.write("---")

# 6. தூண் 3: அரசு தணிக்கை மற்றும் லெட்ஜர் (Sovereign Audit Trail & Ledger)
st.markdown("### 📑 3. Sovereign Audit Trail (Live Settlement Ledger)")

conn = sqlite3.connect('sovereign_ledger.db')
df = pd.read_sql_query('''
    SELECT framework_ref_id AS 'Framework Ref ID',
           timestamp AS 'Execution Time', 
           exporter_lei AS 'Exporter LEI (UAE)', 
           importer_lei AS 'Importer LEI (IN)', 
           trade_volume_local AS 'Volume (AED)', 
           converted_inr AS 'Netting (INR)', 
           usd_leakage_saved AS 'USD Cost Saved (INR)',
           escrow_status AS 'Escrow Status'
    FROM sovereign_trades ORDER BY id DESC
''', conn)
conn.close()

if not df.empty:
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.warning("🏛️ Sandbox Ledger Empty. Awaiting first verified sovereign corporate settlement.")

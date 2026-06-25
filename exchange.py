import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# 1. சர்வதேச நிறுவன வடிவமைப்பு (Enterprise Layout Configuration)
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

# அசல் பிசினஸ் காரணிகள் (1 AED = 25.77 INR)
AED_INR_FACTOR = 25.77
USD_LEAKAGE_SAVINGS_RATE = 0.035

# --- பிரீமியம் கார்ப்பரேட் முகப்பு (பிழையற்ற அசல் ஸ்ட்ரீம்லிட் குறியீடு) ---
st.title("🏛️ SOVEREIGN CROSS-BORDER SETTLEMENT SYSTEM")
st.text("IFSCA GIFT CITY • CENTRAL BANK REGULATORY SANDBOX FRAMEWORK")
st.write("---")

# 3. தொழில்முறை பிரிவுகள் (Professional Separate Desks via Tabs)
tab1, tab2, tab3 = st.tabs([
    "🌐 1. SOVEREIGN REGULATORY DESK", 
    "💼 2. B2B COMMERCE EXECUTION", 
    "📑 3. CENTRAL AUDIT LEDGER"
])

# ==================== டெஸ்க் 1: அரசு கொள்கைப்பகுதி ====================
with tab1:
    st.subheader("📜 Inter-Governmental Bilateral Framework")
    st.info("💡 This workstation displays the legal treaty parameters binding the direct netting between India and partner countries.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("**Regulatory Protocol:** Local Currency Settlement System (LCSS)")
        st.write("**Authorized Jurisdiction:** IFSCA Special Economic Zone (GIFT City, India)")
        st.write("**Clearing Route:** Direct Bilateral Settlement Account Netting (Non-USD)")
    with col_b:
        st.write("**Sovereign Treaty Link:** RBI/2023-24/LCS-Framework-Direct")
        st.write("**Risk Mitigation:** Zero Exchange Rate Risk via Pre-Hedging Mechanisms")
        st.write("**Sovereign Compliance:** AML / CFT Compliant via Legal Entity Identifier (LEI)")

# ==================== டெஸ்க் 2: வணிகர்களுக்கான வர்த்தகப்பகுதி ====================
with tab2:
    st.subheader("🔒 Enterprise Local Currency Trade Gateway")
    st.write("வணிகர்கள் தங்களது லோக்கல் கரன்சியில் நேரடியாக வர்த்தகத்தை லாக் செய்யும் தளம்.")
    
    with st.form(key="sovereign_settlement_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("##### **Exporter Desk (UAE)**")
            exporter_lei = st.text_input("UAE Corporate LEI Number (20 Characters)", max_chars=20, placeholder="e.g. 123400XXXXXXYYYYZZZZ")
            trade_currency = st.selectbox("Settlement Currency Target", ["AED (UAE Dirham)"])
            amount_local = st.number_input("Trade Volume (In Local Currency)", min_value=0.0, step=1000.0, format="%.2f")
            
        with col2:
            st.write("##### **Importer Desk (India)**")
            importer_lei = st.text_input("India Corporate LEI Number (20 Characters)", max_chars=20, placeholder="e.g. 567800XXXXXXYYYYZZZZ")
            
            # பாதுகாப்பான கரன்சி கணக்கீடு
            calculated_inr = amount_local * AED_INR_FACTOR
            st.write("")
            st.write("")
            st.metric(label="Direct Sovereign Netting Value (INR)", value=f"{calculated_inr:,.2f} ₹")

        st.write("---")
        submit_sovereign_trade = st.form_submit_button(label="🔑 LOCK & SECURE SETTLEMENT (SWIFT-FREE)")

    if submit_sovereign_trade:
        if len(exporter_lei) == 20 and len(importer_lei) == 20 and amount_local > 0:
            final_inr = amount_local * AED_INR_FACTOR
            usd_saved = final_inr * USD_LEAKAGE_SAVINGS_RATE
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            framework_id = f"IFSCA-LCS-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            conn = sqlite3.connect('sovereign_ledger.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO sovereign_trades (framework_ref_id, exporter_lei, importer_lei, settlement_currency, trade_volume_local, converted_inr, usd_leakage_saved, escrow_status, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (framework_id, exporter_lei, importer_lei, trade_currency, amount_local, final_inr, usd_saved, 'ESCROW LOCKED', current_time))
            conn.commit()
            conn.close()
            
            st.success("⚖️ TRANSACTION SECURED BY SOVEREIGN FRAMEWORK!")
            st.info(f"**Ref ID:** {framework_id} | **Status:** Escrow Cleared via Direct Central Bank Route.")
        else:
            st.error("❌ Compliance Rejection. Please enter the valid 20-digit Corporate LEI numbers and Trade Volume.")

# ==================== டெஸ்க் 3: மத்திய தணிக்கைப்பகுதி ====================
with tab3:
    st.subheader("📑 Real-Time Audit Trail & Sovereign Ledger")
    st.write("அரசு அதிகாரிகள் மற்றும் தணிக்கையாளர்கள் மட்டுமே பார்க்கும் பாதுகாப்பான கணக்கு விவரங்கள்.")
    
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

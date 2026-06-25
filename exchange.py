import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# 1. பக்க வடிவமைப்பு
st.set_page_config(
    page_title="Dollar-Free Exchange Portal",
    page_icon="🌐",
    layout="centered"
)

# 2. டேட்டாபேஸ் கட்டமைப்பு
def init_db():
    conn = sqlite3.connect('vyapari_ledger.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS global_trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_mobile TEXT,
            receiver_mobile TEXT,
            amount_aed REAL,
            amount_inr REAL,
            usd_fees_saved REAL,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# அசல் மாற்று விகிதம் (1 AED = 25.77 INR)
FIXED_EXCHANGE_RATE = 25.77
# டாலர் மூலம் அனுப்பினால் வீணாகும் தோராயமான 3% சர்வதேச வங்கிக் கட்டணம்
USD_SAVINGS_PERCENT = 0.03 

# --- அசல் டாலர்-ஃப்ரீ பிளாட்பார வடிவமைப்பு ---

st.title("🌐 DOLLAR-FREE EXCHANGE")
st.subheader("International Cross-Border Settlement Desk (Direct AED ⇄ INR)")
st.write("டாலரின் (USD) தலையீடு இல்லாத நேரடி இருதரப்பு வர்த்தகப் தளம்")
st.divider()

# 3. அப்ளிகேஷன் லெவல் பிசினஸ் கால்குலேட்டர்
st.markdown("### 🧮 Direct Bilateral Trade Counter")

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        input_aed = st.number_input("Enter Amount in UAE Dirham (AED)", min_value=0.0, step=10.0, format="%.2f")
    with col2:
        # டாலர் இல்லாமல் நேரடியாக இந்திய ரூபாயில் கணக்கிடுதல்
        calculated_inr = input_aed * FIXED_EXCHANGE_RATE
        st.metric(label="Direct Settlement Value in India (INR)", value=f"{calculated_inr:,.2f} ₹")
    
    # டாலர் கட்டணம் மிச்சமாவது காட்டும் கவுண்ட்டர்
    saved_fees = calculated_inr * USD_SAVINGS_PERCENT
    st.info(f"💡 **USD-Free Advantage:** By avoiding USD conversion, you have saved **{saved_fees:,.2f} ₹** in international banking fees!")

st.write("---")

# 4. பாதுகாப்பான இருதரப்பு செட்டில்மெண்ட் டெர்மினல்
with st.form(key="trade_settlement_form", clear_on_submit=True):
    st.markdown("### 🔒 Execute Direct Country-to-Country Settlement")
    
    sender_mob = st.text_input("UAE Merchant Mobile (10 Digits)", max_chars=10)
    receiver_mob = st.text_input("India Merchant Mobile (10 Digits)", max_chars=10)
    
    trade_amount_aed = st.number_input("Final Settlement Amount (AED)", min_value=0.0, step=50.0, format="%.2f")
    
    submit_trade = st.form_submit_button(label="Lock Direct Local Currency Settlement")

# 5. தரவுச் சேமிப்பு மற்றும் பாதுகாப்பு லாக்
if submit_trade:
    if len(sender_mob) == 10 and len(receiver_mob) == 10 and trade_amount_aed > 0:
        final_inr = trade_amount_aed * FIXED_EXCHANGE_RATE
        fees_saved_inr = final_inr * USD_SAVINGS_PERCENT
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        conn = sqlite3.connect('vyapari_ledger.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO global_trades (sender_mobile, receiver_mobile, amount_aed, amount_inr, usd_fees_saved, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (sender_mob, receiver_mob, trade_amount_aed, final_inr, fees_saved_inr, current_time))
        
        conn.commit()
        conn.close()
        st.success(f"✅ Trade Secured! Locked {trade_amount_aed} AED directly to {final_inr:,.2f} INR. No USD involved.")
    else:
        st.error("❌ Settlement Failed. Please enter valid 10-digit mobile numbers and trade amount.")

st.divider()

# 6. சர்வதேச அசல் செட்டில்மெண்ட் லெட்ஜர் ஹிஸ்டரி
st.markdown("### 📑 LIVE DOLLAR-FREE SETTLEMENT LEDGER")

conn = sqlite3.connect('vyapari_ledger.db')
df = pd.read_sql_query('''
    SELECT timestamp AS 'Time Log', 
           sender_mobile AS 'UAE Merchant', 
           receiver_mobile AS 'India Merchant', 
           amount_aed AS 'Settled (AED)', 
           amount_inr AS 'Received (INR)', 
           usd_fees_saved AS 'Fees Saved (INR)' 
    FROM global_trades ORDER BY id DESC
''', conn)
conn.close()

if not df.empty:
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("ℹ️ No international bilateral trades recorded in the ledger yet.")

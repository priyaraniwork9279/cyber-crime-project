import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date
import io
import os

st.set_page_config(page_title="Cyber Crime Analysis | Bihar", page_icon="🛡️", layout="wide")

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@400;700;900&display=swap');
html, body, [class*="css"] { font-family: 'Exo 2', sans-serif; background-color: #04080f; color: #c8d8e8; }
[data-testid="stSidebar"] { background: #070d1a; border-right: 1px solid #0d2137; }
[data-testid="stSidebar"] * { color: #a0b8cc !important; }
[data-testid="stAppViewContainer"] > .main { background: #04080f; }
[data-testid="stMetric"] { background: #080f1e; border: 1px solid #0d2a42; border-top: 2px solid #00b4ff; border-radius: 10px; padding: 16px !important; }
[data-testid="stMetricLabel"] { color: #3a7fa8 !important; font-size: 0.72rem !important; letter-spacing: 1.5px; text-transform: uppercase; }
[data-testid="stMetricValue"] { color: #e8f4ff !important; font-size: 1.5rem !important; }
[data-testid="stTextInput"] input { background: #080f1e !important; border: 1px solid #0d2a42 !important; border-radius: 6px !important; color: #c8d8e8 !important; }
[data-testid="stNumberInput"] input { background: #080f1e !important; border: 1px solid #0d2a42 !important; color: #c8d8e8 !important; }
div[data-testid="stSelectbox"] > div { background: #080f1e !important; border: 1px solid #0d2a42 !important; color: #c8d8e8 !important; }
.stButton > button { background: linear-gradient(90deg,#003d6b,#005fa3) !important; color: #a8d8ff !important; border: 1px solid #006dc7 !important; border-radius: 6px !important; font-size: 0.85rem !important; padding: 8px 20px !important; }
.stButton > button:hover { background: linear-gradient(90deg,#005fa3,#0080d4) !important; }
.admin-card { background: #080f1e; border: 1px solid #0d2a42; border-left: 3px solid #00c8ff; border-radius: 10px; padding: 16px 20px; margin: 8px 0; }
.success-box { background: #0a1f0a; border: 1px solid #22c55e; border-radius: 8px; padding: 12px 16px; color: #86efac; margin: 8px 0; }
.delete-btn > button { background: linear-gradient(90deg,#4a0000,#6b0000) !important; border: 1px solid #cc0000 !important; }
</style>
""", unsafe_allow_html=True)

# ── DATA FILE ────────────────────────────────────────────────────────────────
DATA_FILE = "cyber_data.csv"

DEFAULT_DATA = """Crime_ID,Incident_Date,Fraud_Type,Loss_Amount,Region,State,Victim_Age,Status
CYB001,2024-01-08,UPI Phishing,47500,Patna,Bihar,34,Resolved
CYB002,2024-01-15,OTP Fraud,21000,Gaya,Bihar,52,Under Investigation
CYB003,2024-01-22,UPI Phishing,38000,Muzaffarpur,Bihar,29,Resolved
CYB004,2024-02-01,Investment Scam,520000,Patna,Bihar,55,Under Investigation
CYB005,2024-02-07,UPI Phishing,62000,Darbhanga,Bihar,41,Resolved
CYB006,2024-02-13,UPI Phishing,29000,Bhagalpur,Bihar,33,Resolved
CYB007,2024-02-19,Social Media Fraud,15500,Gaya,Bihar,24,Under Investigation
CYB008,2024-02-26,UPI Phishing,55000,Patna,Bihar,38,Resolved
CYB009,2024-03-04,OTP Fraud,18000,Ara,Bihar,46,Closed
CYB010,2024-03-11,UPI Phishing,43000,Nalanda,Bihar,31,Under Investigation
CYB011,2024-03-18,UPI Phishing,36000,Siwan,Bihar,27,Resolved
CYB012,2024-03-25,Investment Scam,890000,Muzaffarpur,Bihar,61,Under Investigation
CYB013,2024-04-01,UPI Phishing,51000,Begusarai,Bihar,35,Resolved
CYB014,2024-04-08,Email Phishing,13000,Patna,Bihar,48,Closed
CYB015,2024-04-15,UPI Phishing,68000,Hajipur,Bihar,30,Under Investigation
CYB016,2024-04-22,UPI Phishing,44000,Samastipur,Bihar,37,Resolved
CYB017,2024-04-29,Investment Scam,670000,Patna,Bihar,58,Under Investigation
CYB018,2024-05-06,UPI Phishing,39000,Gaya,Bihar,26,Resolved
CYB019,2024-05-13,Social Media Fraud,22000,Darbhanga,Bihar,32,Closed
CYB020,2024-05-20,UPI Phishing,57000,Patna,Bihar,43,Resolved
CYB021,2024-05-27,OTP Fraud,16500,Bhagalpur,Bihar,50,Under Investigation
CYB022,2024-06-03,UPI Phishing,71000,Muzaffarpur,Bihar,28,Resolved
CYB023,2024-06-10,UPI Phishing,33000,Ara,Bihar,36,Closed
CYB024,2024-06-17,Investment Scam,1100000,Patna,Bihar,64,Under Investigation
CYB025,2024-06-24,UPI Phishing,49000,Nalanda,Bihar,39,Resolved"""

def load_data():
    if "df" not in st.session_state:
        if os.path.exists(DATA_FILE):
            df = pd.read_csv(DATA_FILE, parse_dates=["Incident_Date"])
        else:
            from io import StringIO
            df = pd.read_csv(StringIO(DEFAULT_DATA), parse_dates=["Incident_Date"])
        st.session_state.df = df
    return st.session_state.df

def save_data(df):
    st.session_state.df = df
    df.to_csv(DATA_FILE, index=False)

def get_next_id(df):
    if len(df) == 0:
        return "CYB001"
    last = df["Crime_ID"].str.replace("CYB","").astype(int).max()
    return f"CYB{str(last+1).zfill(3)}"

# ── SESSION STATE ─────────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "public"

df = load_data()

# ══════════════════════════════════════════════════════════════════════════════
#  LOGIN PAGE
# ══════════════════════════════════════════════════════════════════════════════
def show_login():
    st.markdown("""
    <div style='max-width:420px;margin:60px auto 0;'>
    <div style='background:#080f1e;border:1px solid #0d2a42;border-top:2px solid #00c8ff;
    border-radius:14px;padding:36px 40px;text-align:center;'>
    <div style='font-size:2.5rem;margin-bottom:8px;'>🛡️</div>
    <div style='font-size:1.3rem;font-weight:900;color:#ffffff;letter-spacing:1px;'>ADMIN LOGIN</div>
    <div style='font-size:0.7rem;color:#1e5070;letter-spacing:2px;margin-bottom:24px;'>CYBERSHIELD CONTROL PANEL</div>
    </div></div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        username = st.text_input("👤 Username", placeholder="admin")
        password = st.text_input("🔒 Password", type="password", placeholder="••••••••")
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🚀 LOGIN", use_container_width=True):
            if username == "admin" and password == "cyber123":
                st.session_state.logged_in = True
                st.session_state.page = "admin"
                st.rerun()
            else:
                st.error("❌ Galat username ya password! Try again.")

        st.markdown("""
        <div style='text-align:center;margin-top:16px;font-size:0.72rem;color:#1e4060;'>
        Username: <b style='color:#3a7fa8;'>admin</b> &nbsp;|&nbsp;
        Password: <b style='color:#3a7fa8;'>cyber123</b>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  ADMIN PANEL
# ══════════════════════════════════════════════════════════════════════════════
def show_admin():
    df = load_data()

    with st.sidebar:
        st.markdown("""
        <div style='text-align:center;padding:8px 0 16px;'>
        <div style='font-size:1.2rem;color:#00c8ff;font-weight:900;'>🛡️ ADMIN PANEL</div>
        <div style='font-size:0.62rem;color:#1e4060;letter-spacing:2px;'>CYBERSHIELD CONTROL</div>
        </div>
        """, unsafe_allow_html=True)

        admin_tab = st.radio("📋 Menu", [
            "➕ Naya Case Add Karo",
            "✏️ Case Edit Karo",
            "🗑️ Case Delete Karo",
            "📊 Dashboard Dekho",
        ], label_visibility="collapsed")

        st.markdown("---")
        st.markdown(f"<div style='font-size:0.7rem;color:#1e5070;'>📦 Total Records: <b style='color:#00c8ff;'>{len(df)}</b></div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.page = "public"
            st.rerun()

        if st.button("🌐 Public Site Dekho"):
            st.session_state.page = "public"
            st.rerun()

    # ── ADD NEW CASE ──────────────────────────────────────────────────────────
    if "➕ Naya Case Add Karo" in admin_tab:
        st.markdown("""
        <div style='border-bottom:1px solid #0d2137;padding-bottom:12px;margin-bottom:24px;'>
        <span style='font-size:1.4rem;font-weight:900;color:#ffffff;'>➕ Naya Crime Case Add Karo</span>
        </div>
        """, unsafe_allow_html=True)

        new_id = get_next_id(df)
        st.markdown(f"<div class='admin-card'>🆔 Naya Case ID automatically assign hoga: <b style='color:#00c8ff;font-size:1.1rem;'>{new_id}</b></div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            inc_date = st.date_input("📅 Incident Date", value=date.today())
            fraud_type = st.selectbox("⚠️ Fraud Type", [
                "UPI Phishing", "OTP Fraud", "Investment Scam",
                "Social Media Fraud", "Email Phishing", "Other"
            ])
            loss = st.number_input("💸 Loss Amount (₹)", min_value=0, step=1000, value=10000)

        with col2:
            region = st.selectbox("📍 District / Region", [
                "Patna", "Gaya", "Muzaffarpur", "Darbhanga", "Bhagalpur",
                "Ara", "Nalanda", "Siwan", "Begusarai", "Hajipur",
                "Samastipur", "Other"
            ])
            state = st.text_input("🏛️ State", value="Bihar")
            victim_age = st.number_input("👤 Victim Age", min_value=1, max_value=100, value=30)
            status = st.selectbox("📋 Case Status", [
                "Under Investigation", "Resolved", "Closed"
            ])

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✅ Case Save Karo", use_container_width=True):
            new_row = {
                "Crime_ID": new_id,
                "Incident_Date": pd.to_datetime(inc_date),
                "Fraud_Type": fraud_type,
                "Loss_Amount": loss,
                "Region": region,
                "State": state,
                "Victim_Age": victim_age,
                "Status": status,
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df)
            st.markdown(f"<div class='success-box'>✅ Case <b>{new_id}</b> successfully add ho gaya! Dashboard mein dikhai dega.</div>", unsafe_allow_html=True)
            st.balloons()

    # ── EDIT CASE ─────────────────────────────────────────────────────────────
    elif "✏️ Case Edit Karo" in admin_tab:
        st.markdown("""
        <div style='border-bottom:1px solid #0d2137;padding-bottom:12px;margin-bottom:24px;'>
        <span style='font-size:1.4rem;font-weight:900;color:#ffffff;'>✏️ Existing Case Edit Karo</span>
        </div>
        """, unsafe_allow_html=True)

        case_ids = df["Crime_ID"].tolist()
        sel_id = st.selectbox("🔍 Kaunsa Case Edit Karna Hai?", case_ids)

        row = df[df["Crime_ID"] == sel_id].iloc[0]

        st.markdown(f"<div class='admin-card'>Editing: <b style='color:#00c8ff;'>{sel_id}</b> — {row['Fraud_Type']} — {row['Region']}</div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            new_date = st.date_input("📅 Incident Date", value=pd.to_datetime(row["Incident_Date"]).date())
            new_fraud = st.selectbox("⚠️ Fraud Type", [
                "UPI Phishing","OTP Fraud","Investment Scam",
                "Social Media Fraud","Email Phishing","Other"
            ], index=["UPI Phishing","OTP Fraud","Investment Scam","Social Media Fraud","Email Phishing","Other"].index(row["Fraud_Type"]) if row["Fraud_Type"] in ["UPI Phishing","OTP Fraud","Investment Scam","Social Media Fraud","Email Phishing","Other"] else 0)
            new_loss = st.number_input("💸 Loss Amount (₹)", min_value=0, step=1000, value=int(row["Loss_Amount"]))

        with col2:
            new_region = st.text_input("📍 District", value=str(row["Region"]))
            new_state = st.text_input("🏛️ State", value=str(row["State"]))
            new_age = st.number_input("👤 Victim Age", min_value=1, max_value=100, value=int(row["Victim_Age"]))
            new_status = st.selectbox("📋 Status", ["Under Investigation","Resolved","Closed"],
                index=["Under Investigation","Resolved","Closed"].index(row["Status"]) if row["Status"] in ["Under Investigation","Resolved","Closed"] else 0)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾 Changes Save Karo", use_container_width=True):
            idx = df[df["Crime_ID"] == sel_id].index[0]
            df.at[idx, "Incident_Date"] = pd.to_datetime(new_date)
            df.at[idx, "Fraud_Type"]    = new_fraud
            df.at[idx, "Loss_Amount"]   = new_loss
            df.at[idx, "Region"]        = new_region
            df.at[idx, "State"]         = new_state
            df.at[idx, "Victim_Age"]    = new_age
            df.at[idx, "Status"]        = new_status
            save_data(df)
            st.markdown(f"<div class='success-box'>✅ Case <b>{sel_id}</b> successfully update ho gaya!</div>", unsafe_allow_html=True)

    # ── DELETE CASE ───────────────────────────────────────────────────────────
    elif "🗑️ Case Delete Karo" in admin_tab:
        st.markdown("""
        <div style='border-bottom:1px solid #0d2137;padding-bottom:12px;margin-bottom:24px;'>
        <span style='font-size:1.4rem;font-weight:900;color:#ffffff;'>🗑️ Case Delete Karo</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='background:#1a0505;border:1px solid #cc0000;border-radius:8px;padding:12px 16px;color:#fca5a5;margin-bottom:16px;'>⚠️ Warning: Delete karne ke baad case wapas nahi aayega!</div>", unsafe_allow_html=True)

        case_ids = df["Crime_ID"].tolist()
        del_id = st.selectbox("🔍 Kaunsa Case Delete Karna Hai?", case_ids)

        row = df[df["Crime_ID"] == del_id].iloc[0]

        st.markdown(f"""
        <div class='admin-card'>
        <b style='color:#ef4444;'>{del_id}</b><br>
        <span style='font-size:0.85rem;color:#6a9ab8;'>
        📅 {str(row['Incident_Date'])[:10]} &nbsp;|&nbsp;
        ⚠️ {row['Fraud_Type']} &nbsp;|&nbsp;
        📍 {row['Region']} &nbsp;|&nbsp;
        💸 ₹{int(row['Loss_Amount']):,} &nbsp;|&nbsp;
        📋 {row['Status']}
        </span>
        </div>
        """, unsafe_allow_html=True)

        confirm = st.checkbox(f"✅ Haan, main {del_id} delete karna chahta/chahti hun")

        if confirm:
            st.markdown("<div class='delete-btn'>", unsafe_allow_html=True)
            if st.button("🗑️ PERMANENTLY DELETE KARO", use_container_width=True):
                df = df[df["Crime_ID"] != del_id].reset_index(drop=True)
                save_data(df)
                st.markdown(f"<div class='success-box'>🗑️ Case <b>{del_id}</b> delete ho gaya!</div>", unsafe_allow_html=True)
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br><br>")
        st.markdown("<b style='color:#3a7fa8;font-size:0.8rem;'>📋 CURRENT ALL RECORDS:</b>", unsafe_allow_html=True)
        st.dataframe(df[["Crime_ID","Fraud_Type","Region","Loss_Amount","Status"]], use_container_width=True, hide_index=True)

    # ── DASHBOARD PREVIEW ─────────────────────────────────────────────────────
    elif "📊 Dashboard Dekho" in admin_tab:
        st.markdown("""
        <div style='border-bottom:1px solid #0d2137;padding-bottom:12px;margin-bottom:24px;'>
        <span style='font-size:1.4rem;font-weight:900;color:#ffffff;'>📊 Admin Dashboard Overview</span>
        </div>
        """, unsafe_allow_html=True)

        n = len(df)
        total_loss = df["Loss_Amount"].sum()
        upi_n = len(df[df["Fraud_Type"] == "UPI Phishing"])
        upi_rate = round((upi_n / max(n,1)) * 100, 1)

        c1,c2,c3,c4 = st.columns(4)
        c1.metric("🗂️ Total Cases", f"{n}")
        c2.metric("💸 Total Loss", f"₹{total_loss/100000:.1f}L")
        c3.metric("📶 UPI Rate", f"{upi_rate}%")
        c4.metric("✅ Resolved", f"{len(df[df['Status']=='Resolved'])}")

        PAL = ["#00c8ff","#f59e0b","#ef4444","#22c55e","#a78bfa"]

        l, r = st.columns(2)
        with l:
            fc = df["Fraud_Type"].value_counts().reset_index()
            fc.columns = ["Fraud_Type","Cases"]
            fig = px.bar(fc, x="Fraud_Type", y="Cases", color="Fraud_Type",
                         color_discrete_sequence=PAL, text="Cases")
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              font=dict(color="#6a9ab8"), showlegend=False,
                              title=dict(text="FRAUD TYPES", font=dict(color="#3a7fa8",size=12),x=0))
            fig.update_traces(textposition="outside", textfont=dict(color="#c8d8e8"))
            fig.update_xaxes(showgrid=False); fig.update_yaxes(gridcolor="#0a1f35")
            st.plotly_chart(fig, use_container_width=True)
        with r:
            gl = df.groupby("Region")["Loss_Amount"].sum().reset_index()
            fig2 = px.pie(gl, names="Region", values="Loss_Amount",
                          color_discrete_sequence=PAL, hole=0.42)
            fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#6a9ab8"),
                               title=dict(text="LOSS BY DISTRICT", font=dict(color="#3a7fa8",size=12),x=0))
            fig2.update_traces(textfont=dict(color="#fff"), textinfo="percent+label")
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("<b style='color:#3a7fa8;font-size:0.8rem;'>📋 ALL RECORDS:</b>", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, hide_index=True)

        buf = io.StringIO()
        df.to_csv(buf, index=False)
        st.download_button("⬇️ Full Data Download (.csv)", data=buf.getvalue().encode(),
                           file_name="cyber_data_full.csv", mime="text/csv")

# ══════════════════════════════════════════════════════════════════════════════
#  PUBLIC DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
def show_public():
    df = load_data()

    with st.sidebar:
        st.markdown("""
        <div style='text-align:center;padding:10px 0 16px;'>
        <div style='font-size:1.3rem;color:#00c8ff;letter-spacing:2px;font-weight:900;'>🛡️ CYBERSHIELD</div>
        <div style='font-size:0.65rem;color:#1e4060;letter-spacing:2px;margin-top:3px;'>BIHAR CRIME ANALYSIS</div>
        </div>
        <style>
        @keyframes pulse{0%{box-shadow:0 0 8px rgba(255,30,30,0.4)}50%{box-shadow:0 0 25px rgba(255,30,30,0.8)}100%{box-shadow:0 0 8px rgba(255,30,30,0.4)}}
        @keyframes blink{0%,100%{opacity:1}50%{opacity:0.5}}
        .sos{background:linear-gradient(135deg,#1a0505,#2a0808);border:1.5px solid #cc2020;border-radius:10px;padding:14px;text-align:center;animation:pulse 2s infinite;margin-bottom:16px;}
        .sos-num{font-size:2.4rem;color:#ff4040;letter-spacing:5px;font-weight:900;animation:blink 1.5s infinite;}
        </style>
        <div class='sos'>
        <div style='font-size:0.6rem;color:#993333;letter-spacing:2px;margin-bottom:4px;'>🚨 CYBER CRIME EMERGENCY</div>
        <div class='sos-num'>1930</div>
        <div style='font-size:0.65rem;color:#cc6060;letter-spacing:1.5px;margin-top:4px;'>NATIONAL HELPLINE · 24/7 FREE</div>
        </div>
        """, unsafe_allow_html=True)

        regions = ["All Districts"] + sorted(df["Region"].unique().tolist())
        sel_region = st.selectbox("📍 District Select Karo", regions)
        fraud_types = ["All Types"] + sorted(df["Fraud_Type"].unique().tolist())
        sel_fraud = st.selectbox("⚠️ Fraud Type", fraud_types)
        statuses = ["All Status"] + sorted(df["Status"].unique().tolist())
        sel_status = st.selectbox("📋 Case Status", statuses)

        st.markdown("""
        <div style='margin-top:16px;font-size:0.72rem;color:#2a5070;line-height:2;'>
        <b style='color:#1e5070;font-size:0.65rem;letter-spacing:2px;'>◈ SAFETY TIPS</b><br>
        🔒 OTP kabhi share mat karo<br>
        📵 KYC SMS links ignore karo<br>
        💸 Guaranteed return = SCAM<br>
        🌐 cybercrime.gov.in
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        if st.button("🔐 Admin Login"):
            st.session_state.page = "login"
            st.rerun()

    # Apply filters
    dff = df.copy()
    if sel_region != "All Districts": dff = dff[dff["Region"] == sel_region]
    if sel_fraud  != "All Types":     dff = dff[dff["Fraud_Type"] == sel_fraud]
    if sel_status != "All Status":    dff = dff[dff["Status"] == sel_status]

    # Header
    st.markdown("""
    <div style='background:linear-gradient(135deg,#050d1a,#070f20);border:1px solid #0a1f35;
    border-radius:12px;padding:28px 36px;margin-bottom:24px;border-top:2px solid #00c8ff;'>
    <div style='font-size:0.7rem;color:#1e5070;letter-spacing:3px;margin-bottom:8px;'>◈ AKU · BCA FINAL YEAR PROJECT · 2024-25</div>
    <div style='font-size:1.8rem;font-weight:900;color:#ffffff;margin-bottom:8px;'>
    🛡️ Cyber-Crime Pattern Analysis &<br><span style='color:#00c8ff;'>Public Awareness System</span></div>
    <div style='font-size:0.88rem;color:#4a7090;line-height:1.7;max-width:750px;'>
    Bihar ke districts mein ho rahe digital frauds ka interactive analysis dashboard.
    Sidebar se apna district select karo aur live data dekho.
    </div></div>
    """, unsafe_allow_html=True)

    # KPIs
    n = len(dff)
    total_loss = dff["Loss_Amount"].sum()
    upi_n = len(dff[dff["Fraud_Type"] == "UPI Phishing"])
    upi_rate = round((upi_n / max(n,1)) * 100, 1)
    avg_loss = int(dff["Loss_Amount"].mean()) if n else 0
    resolved = len(dff[dff["Status"] == "Resolved"])

    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("🗂️ Total Cases", f"{n}")
    c2.metric("💸 Total Loss", f"₹{total_loss/100000:.1f}L")
    c3.metric("📶 UPI Phishing", f"{upi_rate}%")
    c4.metric("💰 Avg Loss", f"₹{avg_loss:,}")
    c5.metric("✅ Resolved", f"{resolved}")

    st.markdown("<br>", unsafe_allow_html=True)

    PAL = ["#00c8ff","#f59e0b","#ef4444","#22c55e","#a78bfa","#fb923c"]

    def dark(fig, title):
        fig.update_layout(
            title=dict(text=title, font=dict(size=12, color="#3a7fa8"), x=0),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#6a9ab8"), margin=dict(l=10,r=10,t=45,b=10),
            legend=dict(bgcolor="rgba(0,0,0,0)"),
        )
        return fig

    tab1, tab2, tab3, tab4 = st.tabs(["📊 CHARTS","🗺️ HOTSPOTS","📈 TRENDS","🗄️ DATABASE"])

    with tab1:
        l, r = st.columns(2)
        with l:
            fc = dff["Fraud_Type"].value_counts().reset_index()
            fc.columns = ["Fraud_Type","Cases"]
            fig = px.bar(fc, x="Fraud_Type", y="Cases", color="Fraud_Type",
                         color_discrete_sequence=PAL, text="Cases")
            fig.update_traces(textposition="outside", textfont=dict(color="#c8d8e8"))
            fig.update_xaxes(showgrid=False); fig.update_yaxes(gridcolor="#0a1f35")
            fig.update_layout(showlegend=False)
            dark(fig,"FRAUD CATEGORY — CASE COUNT")
            st.plotly_chart(fig, use_container_width=True)
        with r:
            gl = dff.groupby("Region")["Loss_Amount"].sum().reset_index()
            fig2 = px.pie(gl, names="Region", values="Loss_Amount",
                          color_discrete_sequence=PAL, hole=0.42)
            fig2.update_traces(textfont=dict(color="#fff"), textinfo="percent+label",
                               marker=dict(line=dict(color="#04080f",width=2)))
            dark(fig2,"GEOGRAPHICAL LOSS BREAKDOWN (₹)")
            st.plotly_chart(fig2, use_container_width=True)

        l2, r2 = st.columns(2)
        with l2:
            lf = dff.groupby("Fraud_Type")["Loss_Amount"].sum().reset_index().sort_values("Loss_Amount")
            lf.columns = ["Fraud_Type","Loss"]
            fig3 = px.bar(lf, x="Loss", y="Fraud_Type", orientation="h",
                          color="Loss", color_continuous_scale=["#001830","#00c8ff","#ef4444"],
                          text=lf["Loss"].apply(lambda v: f"₹{v/100000:.1f}L"))
            fig3.update_traces(textposition="outside", textfont=dict(color="#c8d8e8"))
            fig3.update_xaxes(gridcolor="#0a1f35"); fig3.update_yaxes(gridcolor="rgba(0,0,0,0)")
            fig3.update_layout(coloraxis_showscale=False)
            dark(fig3,"TOTAL LOSS BY FRAUD TYPE")
            st.plotly_chart(fig3, use_container_width=True)
        with r2:
            sc = dff["Status"].value_counts().reset_index()
            sc.columns = ["Status","Count"]
            fig4 = px.bar(sc, x="Status", y="Count", color="Status", text="Count",
                          color_discrete_map={"Resolved":"#22c55e","Under Investigation":"#f59e0b","Closed":"#4a6080"})
            fig4.update_traces(textposition="outside", textfont=dict(color="#c8d8e8"))
            fig4.update_xaxes(showgrid=False); fig4.update_yaxes(gridcolor="#0a1f35")
            fig4.update_layout(showlegend=False)
            dark(fig4,"CASE STATUS BREAKDOWN")
            st.plotly_chart(fig4, use_container_width=True)

    with tab2:
        ra = dff.groupby("Region").agg(Cases=("Crime_ID","count"),Loss=("Loss_Amount","sum")).reset_index()
        fig5 = px.bar(ra, x="Region", y="Cases", color="Loss", text="Cases",
                      color_continuous_scale=["#001830","#00c8ff","#ef4444"])
        fig5.update_traces(textposition="outside", textfont=dict(color="#c8d8e8"))
        fig5.update_xaxes(showgrid=False, tickangle=-20); fig5.update_yaxes(gridcolor="#0a1f35")
        dark(fig5,"CASES PER DISTRICT")
        st.plotly_chart(fig5, use_container_width=True)

        fig6 = px.treemap(ra, path=["Region"], values="Cases", color="Loss",
                          color_continuous_scale=["#001020","#003060","#00c8ff","#f59e0b","#ef4444"])
        fig6.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#c8d8e8"),
                           margin=dict(l=10,r=10,t=45,b=10),
                           title=dict(text="DISTRICT HEATMAP",font=dict(size=12,color="#3a7fa8"),x=0))
        st.plotly_chart(fig6, use_container_width=True)

    with tab3:
        dff2 = dff.copy()
        dff2["MonthSort"] = pd.to_datetime(dff2["Incident_Date"]).dt.to_period("M").apply(lambda p: p.start_time)
        monthly = dff2.groupby(["MonthSort","Fraud_Type"]).agg(Cases=("Crime_ID","count")).reset_index().sort_values("MonthSort")
        fig7 = px.line(monthly, x="MonthSort", y="Cases", color="Fraud_Type",
                       markers=True, color_discrete_sequence=PAL)
        fig7.update_xaxes(gridcolor="#0a1f35"); fig7.update_yaxes(gridcolor="#0a1f35")
        dark(fig7,"MONTHLY FRAUD CASE TREND")
        st.plotly_chart(fig7, use_container_width=True)

        ml = dff2.groupby("MonthSort")["Loss_Amount"].sum().reset_index().sort_values("MonthSort")
        fig8 = px.area(ml, x="MonthSort", y="Loss_Amount", color_discrete_sequence=["#00c8ff"])
        fig8.update_traces(fillcolor="rgba(0,200,255,0.08)", line=dict(width=2.5))
        fig8.update_xaxes(gridcolor="#0a1f35"); fig8.update_yaxes(gridcolor="#0a1f35")
        dark(fig8,"MONTHLY TOTAL FINANCIAL LOSS (₹)")
        st.plotly_chart(fig8, use_container_width=True)

    with tab4:
        st.markdown("<p style='color:#1e5070;font-size:0.72rem;letter-spacing:2px;'>◈ LIVE SEARCHABLE DATABASE</p>", unsafe_allow_html=True)
        search = st.text_input("🔍 Search karo", placeholder="e.g. Patna  ya  UPI Phishing")
        show = dff.copy()
        if search.strip():
            mask = show.apply(lambda col: col.astype(str).str.contains(search, case=False, na=False)).any(axis=1)
            show = show[mask]
        st.markdown(f"<p style='color:#1e5070;font-size:0.7rem;'>{len(show)} records</p>", unsafe_allow_html=True)
        st.dataframe(show, use_container_width=True, hide_index=True)
        buf = io.StringIO()
        show.to_csv(buf, index=False)
        st.download_button("⬇️ Download Data (.csv)", data=buf.getvalue().encode(),
                           file_name="cyber_data.csv", mime="text/csv")

    st.markdown(f"""
    <div style='text-align:center;font-size:0.62rem;color:#0d2a42;padding:16px 0;margin-top:20px;'>
    CYBERSHIELD BIHAR · BCA FINAL YEAR PROJECT · AKU 2024-25 · PYTHON + STREAMLIT + PANDAS + PLOTLY
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  ROUTER
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "login":
    show_login()
elif st.session_state.page == "admin" and st.session_state.logged_in:
    show_admin()
else:
    st.session_state.page = "public"
    show_public()

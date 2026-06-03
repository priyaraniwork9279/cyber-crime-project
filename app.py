import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import io

st.set_page_config(page_title="Cyber Crime Analysis | Bihar", page_icon="🛡️", layout="wide")

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
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("cyber_data.csv", parse_dates=["Incident_Date"])
    except FileNotFoundError:
        st.error("cyber_data.csv file nahi mili! Dobara upload karo.")
        st.stop()
    df["Month"] = df["Incident_Date"].dt.strftime("%b %Y")
    df["MonthSort"] = df["Incident_Date"].dt.to_period("M").apply(lambda p: p.start_time)
    return df

df_all = load_data()

with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:10px 0 16px;'>
        <div style='font-size:1.3rem;color:#00c8ff;letter-spacing:2px;font-weight:900;'>🛡️ CYBERSHIELD</div>
        <div style='font-size:0.65rem;color:#1e4060;letter-spacing:2px;margin-top:3px;'>BIHAR CRIME ANALYSIS</div>
    </div>
    <style>
    @keyframes pulse { 0%{box-shadow:0 0 8px rgba(255,30,30,0.4)} 50%{box-shadow:0 0 25px rgba(255,30,30,0.8)} 100%{box-shadow:0 0 8px rgba(255,30,30,0.4)} }
    @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.5} }
    .sos { background:linear-gradient(135deg,#1a0505,#2a0808); border:1.5px solid #cc2020; border-radius:10px; padding:14px; text-align:center; animation:pulse 2s infinite; margin-bottom:16px; }
    .sos-num { font-size:2.4rem; color:#ff4040; letter-spacing:5px; font-weight:900; animation:blink 1.5s infinite; }
    </style>
    <div class='sos'>
        <div style='font-size:0.6rem;color:#993333;letter-spacing:2px;margin-bottom:4px;'>🚨 CYBER CRIME EMERGENCY</div>
        <div class='sos-num'>1930</div>
        <div style='font-size:0.65rem;color:#cc6060;letter-spacing:1.5px;margin-top:4px;'>NATIONAL HELPLINE · 24/7 FREE</div>
    </div>
    """, unsafe_allow_html=True)

    regions = ["All Districts"] + sorted(df_all["Region"].unique().tolist())
    sel_region = st.selectbox("📍 District Select Karo", regions)

    fraud_types = ["All Types"] + sorted(df_all["Fraud_Type"].unique().tolist())
    sel_fraud = st.selectbox("⚠️ Fraud Type", fraud_types)

    statuses = ["All Status"] + sorted(df_all["Status"].unique().tolist())
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

df = df_all.copy()
if sel_region != "All Districts": df = df[df["Region"] == sel_region]
if sel_fraud != "All Types": df = df[df["Fraud_Type"] == sel_fraud]
if sel_status != "All Status": df = df[df["Status"] == sel_status]

st.markdown("""
<div style='background:linear-gradient(135deg,#050d1a,#070f20);border:1px solid #0a1f35;
border-radius:12px;padding:28px 36px;margin-bottom:24px;border-top:2px solid #00c8ff;'>
<div style='font-size:0.7rem;color:#1e5070;letter-spacing:3px;margin-bottom:8px;'>
◈ AKU · BCA FINAL YEAR PROJECT · 2024-25</div>
<div style='font-size:1.8rem;font-weight:900;color:#ffffff;margin-bottom:8px;'>
🛡️ Cyber-Crime Pattern Analysis &<br><span style='color:#00c8ff;'>Public Awareness System</span></div>
<div style='font-size:0.88rem;color:#4a7090;line-height:1.7;max-width:750px;'>
Bihar ke districts mein ho rahe digital frauds ka interactive analysis dashboard.
UPI Phishing, OTP Fraud, Investment Scams — sab ka data ek jagah.
Sidebar se apna district select karo aur live data dekho.
</div>
</div>
""", unsafe_allow_html=True)

n = len(df)
total_loss = df["Loss_Amount"].sum()
upi_n = len(df[df["Fraud_Type"] == "UPI Phishing"])
upi_rate = round((upi_n / max(n,1)) * 100, 1)
avg_loss = int(df["Loss_Amount"].mean()) if n else 0
resolved = len(df[df["Status"] == "Resolved"])

c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("🗂️ Total Cases", f"{n}")
c2.metric("💸 Total Loss", f"₹{total_loss/100000:.1f}L")
c3.metric("📶 UPI Phishing", f"{upi_rate}%")
c4.metric("💰 Avg Loss", f"₹{avg_loss:,}")
c5.metric("✅ Resolved", f"{resolved}")

st.markdown("<br>", unsafe_allow_html=True)

PAL = ["#00c8ff","#f59e0b","#ef4444","#22c55e","#a78bfa","#fb923c"]

tab1, tab2, tab3, tab4 = st.tabs(["📊 CHARTS", "🗺️ HOTSPOTS", "📈 TRENDS", "🗄️ DATABASE"])

def dark(fig, title):
    fig.update_layout(
        title=dict(text=title, font=dict(size=12, color="#3a7fa8"), x=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#6a9ab8"), margin=dict(l=10,r=10,t=45,b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    return fig

with tab1:
    l, r = st.columns(2)
    with l:
        fc = df["Fraud_Type"].value_counts().reset_index()
        fc.columns = ["Fraud_Type","Cases"]
        fig = px.bar(fc, x="Fraud_Type", y="Cases", color="Fraud_Type",
                     color_discrete_sequence=PAL, text="Cases")
        fig.update_traces(textposition="outside", textfont=dict(color="#c8d8e8"))
        fig.update_xaxes(showgrid=False, linecolor="#0a1f35")
        fig.update_yaxes(gridcolor="#0a1f35", zerolinecolor="#0a1f35")
        fig.update_layout(showlegend=False)
        dark(fig, "FRAUD CATEGORY — CASE COUNT")
        st.plotly_chart(fig, use_container_width=True)
    with r:
        gl = df.groupby("Region")["Loss_Amount"].sum().reset_index()
        gl.columns = ["Region","Total_Loss"]
        fig2 = px.pie(gl, names="Region", values="Total_Loss",
                      color_discrete_sequence=PAL, hole=0.42)
        fig2.update_traces(textfont=dict(color="#ffffff"), textinfo="percent+label",
                           marker=dict(line=dict(color="#04080f", width=2)))
        dark(fig2, "GEOGRAPHICAL LOSS BREAKDOWN (₹)")
        st.plotly_chart(fig2, use_container_width=True)

    l2, r2 = st.columns(2)
    with l2:
        lf = df.groupby("Fraud_Type")["Loss_Amount"].sum().reset_index().sort_values("Loss_Amount")
        lf.columns = ["Fraud_Type","Loss"]
        fig3 = px.bar(lf, x="Loss", y="Fraud_Type", orientation="h",
                      color="Loss", color_continuous_scale=["#001830","#00c8ff","#ef4444"],
                      text=lf["Loss"].apply(lambda v: f"₹{v/100000:.1f}L"))
        fig3.update_traces(textposition="outside", textfont=dict(color="#c8d8e8"))
        fig3.update_xaxes(gridcolor="#0a1f35")
        fig3.update_yaxes(gridcolor="rgba(0,0,0,0)")
        fig3.update_layout(coloraxis_showscale=False)
        dark(fig3, "TOTAL LOSS BY FRAUD TYPE (₹)")
        st.plotly_chart(fig3, use_container_width=True)
    with r2:
        sc = df["Status"].value_counts().reset_index()
        sc.columns = ["Status","Count"]
        fig4 = px.bar(sc, x="Status", y="Count", color="Status", text="Count",
                      color_discrete_map={"Resolved":"#22c55e","Under Investigation":"#f59e0b","Closed":"#4a6080"})
        fig4.update_traces(textposition="outside", textfont=dict(color="#c8d8e8"))
        fig4.update_xaxes(showgrid=False)
        fig4.update_yaxes(gridcolor="#0a1f35")
        fig4.update_layout(showlegend=False)
        dark(fig4, "CASE STATUS BREAKDOWN")
        st.plotly_chart(fig4, use_container_width=True)

with tab2:
    ra = df.groupby("Region").agg(Cases=("Crime_ID","count"), Loss=("Loss_Amount","sum")).reset_index()
    fig5 = px.bar(ra, x="Region", y="Cases", color="Loss", text="Cases",
                  color_continuous_scale=["#001830","#00c8ff","#ef4444"])
    fig5.update_traces(textposition="outside", textfont=dict(color="#c8d8e8"))
    fig5.update_xaxes(showgrid=False, tickangle=-20)
    fig5.update_yaxes(gridcolor="#0a1f35")
    dark(fig5, "CASES PER DISTRICT (colour = financial loss)")
    st.plotly_chart(fig5, use_container_width=True)

    fig6 = px.treemap(ra, path=["Region"], values="Cases", color="Loss",
                      color_continuous_scale=["#001020","#003060","#00c8ff","#f59e0b","#ef4444"])
    fig6.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#c8d8e8"),
                       margin=dict(l=10,r=10,t=45,b=10),
                       title=dict(text="DISTRICT HEATMAP", font=dict(size=12,color="#3a7fa8"),x=0))
    st.plotly_chart(fig6, use_container_width=True)

with tab3:
    monthly = df.groupby(["MonthSort","Fraud_Type"]).agg(Cases=("Crime_ID","count")).reset_index().sort_values("MonthSort")
    fig7 = px.line(monthly, x="MonthSort", y="Cases", color="Fraud_Type",
                   markers=True, color_discrete_sequence=PAL)
    fig7.update_xaxes(gridcolor="#0a1f35")
    fig7.update_yaxes(gridcolor="#0a1f35")
    dark(fig7, "MONTHLY FRAUD CASE TREND")
    st.plotly_chart(fig7, use_container_width=True)

    ml = df.groupby("MonthSort")["Loss_Amount"].sum().reset_index().sort_values("MonthSort")
    fig8 = px.area(ml, x="MonthSort", y="Loss_Amount", color_discrete_sequence=["#00c8ff"])
    fig8.update_traces(fillcolor="rgba(0,200,255,0.08)", line=dict(width=2.5))
    fig8.update_xaxes(gridcolor="#0a1f35")
    fig8.update_yaxes(gridcolor="#0a1f35")
    dark(fig8, "MONTHLY TOTAL FINANCIAL LOSS (₹)")
    st.plotly_chart(fig8, use_container_width=True)

with tab4:
    st.markdown("<p style='color:#1e5070;font-size:0.72rem;letter-spacing:2px;'>◈ LIVE SEARCHABLE DATABASE</p>", unsafe_allow_html=True)
    search = st.text_input("🔍 Search karo (District, Fraud Type, Status...)", placeholder="e.g. Patna  ya  UPI Phishing")
    show = df.drop(columns=["Month","MonthSort"], errors="ignore").copy()
    if search.strip():
        mask = show.apply(lambda col: col.astype(str).str.contains(search, case=False, na=False)).any(axis=1)
        show = show[mask]
    st.markdown(f"<p style='color:#1e5070;font-size:0.7rem;'>{len(show)} records</p>", unsafe_allow_html=True)
    st.dataframe(show, use_container_width=True, hide_index=True)

    buf = io.StringIO()
    show.to_csv(buf, index=False)
    st.download_button("⬇️ Download Data (.csv)", data=buf.getvalue().encode(),
                       file_name="cyber_data_filtered.csv", mime="text/csv")

st.markdown(f"""
<div style='text-align:center;font-size:0.62rem;color:#0d2a42;padding:16px 0;margin-top:20px;'>
CYBERSHIELD BIHAR · BCA FINAL YEAR PROJECT · AKU 2024-25 · PYTHON + STREAMLIT + PANDAS + PLOTLY
</div>
""", unsafe_allow_html=True)

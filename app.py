import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
import io

st.set_page_config(page_title="Cyber Crime Analysis | Bihar", page_icon="🛡️", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "public"

ROWS = [
    ["CYB001","2024-01-08","UPI Phishing",47500,"Patna","Bihar",34,"Resolved"],
    ["CYB002","2024-01-15","OTP Fraud",21000,"Gaya","Bihar",52,"Under Investigation"],
    ["CYB003","2024-01-22","UPI Phishing",38000,"Muzaffarpur","Bihar",29,"Resolved"],
    ["CYB004","2024-02-01","Investment Scam",520000,"Patna","Bihar",55,"Under Investigation"],
    ["CYB005","2024-02-07","UPI Phishing",62000,"Darbhanga","Bihar",41,"Resolved"],
    ["CYB006","2024-02-13","UPI Phishing",29000,"Bhagalpur","Bihar",33,"Resolved"],
    ["CYB007","2024-02-19","Social Media Fraud",15500,"Gaya","Bihar",24,"Under Investigation"],
    ["CYB008","2024-02-26","UPI Phishing",55000,"Patna","Bihar",38,"Resolved"],
    ["CYB009","2024-03-04","OTP Fraud",18000,"Ara","Bihar",46,"Closed"],
    ["CYB010","2024-03-11","UPI Phishing",43000,"Nalanda","Bihar",31,"Under Investigation"],
    ["CYB011","2024-03-18","UPI Phishing",36000,"Siwan","Bihar",27,"Resolved"],
    ["CYB012","2024-03-25","Investment Scam",890000,"Muzaffarpur","Bihar",61,"Under Investigation"],
    ["CYB013","2024-04-01","UPI Phishing",51000,"Begusarai","Bihar",35,"Resolved"],
    ["CYB014","2024-04-08","Email Phishing",13000,"Patna","Bihar",48,"Closed"],
    ["CYB015","2024-04-15","UPI Phishing",68000,"Hajipur","Bihar",30,"Under Investigation"],
    ["CYB016","2024-04-22","UPI Phishing",44000,"Samastipur","Bihar",37,"Resolved"],
    ["CYB017","2024-04-29","Investment Scam",670000,"Patna","Bihar",58,"Under Investigation"],
    ["CYB018","2024-05-06","UPI Phishing",39000,"Gaya","Bihar",26,"Resolved"],
    ["CYB019","2024-05-13","Social Media Fraud",22000,"Darbhanga","Bihar",32,"Closed"],
    ["CYB020","2024-05-20","UPI Phishing",57000,"Patna","Bihar",43,"Resolved"],
    ["CYB021","2024-05-27","OTP Fraud",16500,"Bhagalpur","Bihar",50,"Under Investigation"],
    ["CYB022","2024-06-03","UPI Phishing",71000,"Muzaffarpur","Bihar",28,"Resolved"],
    ["CYB023","2024-06-10","UPI Phishing",33000,"Ara","Bihar",36,"Closed"],
    ["CYB024","2024-06-17","Investment Scam",1100000,"Patna","Bihar",64,"Under Investigation"],
    ["CYB025","2024-06-24","UPI Phishing",49000,"Nalanda","Bihar",39,"Resolved"],
]
COLS = ["Crime_ID","Incident_Date","Fraud_Type","Loss_Amount","Region","State","Victim_Age","Status"]

def get_df():
    if "data" not in st.session_state:
        df = pd.DataFrame(ROWS, columns=COLS)
        df["Incident_Date"] = pd.to_datetime(df["Incident_Date"])
        df["Loss_Amount"] = df["Loss_Amount"].astype(int)
        df["Victim_Age"] = df["Victim_Age"].astype(int)
        st.session_state.data = df
    return st.session_state.data

def save_df(df):
    st.session_state.data = df.copy()

def next_id():
    df = get_df()
    nums = df["Crime_ID"].str.replace("CYB","").astype(int)
    return f"CYB{str(nums.max()+1).zfill(3)}"

PAL = ["#00c8ff","#f59e0b","#ef4444","#22c55e","#a78bfa","#fb923c"]

def dark(fig, title):
    fig.update_layout(
        title=dict(text=title, font=dict(size=12, color="#3a7fa8"), x=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#6a9ab8"),
        margin=dict(l=10,r=10,t=45,b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    return fig

st.markdown("""
<style>
html, body, [class*="css"] { background-color: #04080f; color: #c8d8e8; }
[data-testid="stSidebar"] { background: #070d1a; }
[data-testid="stSidebar"] * { color: #a0b8cc !important; }
[data-testid="stAppViewContainer"] > .main { background: #04080f; }
[data-testid="stMetric"] { background: #080f1e; border: 1px solid #0d2a42; border-top: 2px solid #00b4ff; border-radius: 10px; padding: 16px !important; }
[data-testid="stMetricLabel"] { color: #3a7fa8 !important; font-size: 0.72rem !important; }
[data-testid="stMetricValue"] { color: #e8f4ff !important; font-size: 1.5rem !important; }
.stButton > button { background: #003d6b !important; color: #a8d8ff !important; border: 1px solid #006dc7 !important; border-radius: 6px !important; }
@keyframes pulse{0%{box-shadow:0 0 8px rgba(255,30,30,0.4)}50%{box-shadow:0 0 25px rgba(255,30,30,0.8)}100%{box-shadow:0 0 8px rgba(255,30,30,0.4)}}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0.5}}
.sos{background:linear-gradient(135deg,#1a0505,#2a0808);border:1.5px solid #cc2020;border-radius:10px;padding:14px;text-align:center;animation:pulse 2s infinite;margin-bottom:16px;}
.sos-num{font-size:2.4rem;color:#ff4040;letter-spacing:5px;font-weight:900;animation:blink 1.5s infinite;}
</style>
""", unsafe_allow_html=True)

def show_login():
    with st.sidebar:
        st.markdown("<div style='text-align:center;padding:20px 0;font-size:1.2rem;color:#00c8ff;font-weight:900;'>🛡️ CYBERSHIELD</div>", unsafe_allow_html=True)
        if st.button("🌐 Public Site", use_container_width=True):
            st.session_state.page = "public"
            st.rerun()
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1,c2,c3 = st.columns([1,1.2,1])
    with c2:
        st.markdown("<div style='background:#080f1e;border:1px solid #0d2a42;border-top:2px solid #00c8ff;border-radius:14px;padding:30px;text-align:center;'><div style='font-size:2rem;'>🛡️</div><div style='font-size:1.1rem;font-weight:900;color:#fff;margin:8px 0 4px;'>ADMIN LOGIN</div><div style='font-size:0.65rem;color:#1e5070;letter-spacing:2px;'>CYBERSHIELD CONTROL PANEL</div></div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        u = st.text_input("👤 Username", placeholder="admin")
        p = st.text_input("🔒 Password", type="password", placeholder="••••••••")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 LOGIN", use_container_width=True):
            if u == "admin" and p == "cyber123":
                st.session_state.logged_in = True
                st.session_state.page = "admin"
                st.rerun()
            else:
                st.error("❌ Galat username ya password!")
        st.markdown("<div style='text-align:center;margin-top:12px;font-size:0.72rem;color:#1e4060;'>Username: <b style='color:#3a7fa8;'>admin</b> | Password: <b style='color:#3a7fa8;'>cyber123</b></div>", unsafe_allow_html=True)

def show_admin():
    df = get_df()
    with st.sidebar:
        st.markdown("<div style='text-align:center;padding:8px 0 16px;'><div style='font-size:1.1rem;color:#00c8ff;font-weight:900;'>🛡️ ADMIN PANEL</div></div>", unsafe_allow_html=True)
        menu = st.radio("Menu", ["➕ Case Add","✏️ Case Edit","🗑️ Case Delete","📊 Dashboard"], label_visibility="collapsed")
        st.markdown("---")
        st.markdown(f"<div style='font-size:0.7rem;color:#1e5070;'>📦 Records: <b style='color:#00c8ff;'>{len(df)}</b></div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.page = "public"
            st.rerun()
        if st.button("🌐 Public Site", use_container_width=True):
            st.session_state.page = "public"
            st.rerun()

    if "➕" in menu:
        st.markdown("<h2 style='color:#fff;'>➕ Naya Case Add Karo</h2>", unsafe_allow_html=True)
        nid = next_id()
        st.info(f"🆔 Case ID: **{nid}** (automatic)")
        c1,c2 = st.columns(2)
        with c1:
            d  = st.date_input("📅 Tarikh", value=date.today())
            ft = st.selectbox("⚠️ Fraud Type", ["UPI Phishing","OTP Fraud","Investment Scam","Social Media Fraud","Email Phishing","Other"])
            am = st.number_input("💸 Loss (₹)", min_value=0, step=500, value=10000)
        with c2:
            rg = st.selectbox("📍 District", ["Patna","Gaya","Muzaffarpur","Darbhanga","Bhagalpur","Ara","Nalanda","Siwan","Begusarai","Hajipur","Samastipur","Other"])
            st8 = st.text_input("🏛️ State", value="Bihar")
            ag = st.number_input("👤 Age", min_value=1, max_value=100, value=30)
            ss = st.selectbox("📋 Status", ["Under Investigation","Resolved","Closed"])
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✅ SAVE KARO", use_container_width=True):
            nr = pd.DataFrame([[nid,pd.to_datetime(d),ft,am,rg,st8,ag,ss]], columns=COLS)
            save_df(pd.concat([get_df(), nr], ignore_index=True))
            st.success(f"✅ {nid} add ho gaya!")
            st.balloons()

    elif "✏️" in menu:
        st.markdown("<h2 style='color:#fff;'>✏️ Case Edit Karo</h2>", unsafe_allow_html=True)
        df = get_df()
        sel = st.selectbox("Case ID", df["Crime_ID"].tolist())
        row = df[df["Crime_ID"]==sel].iloc[0]
        st.markdown(f"<div style='background:#080f1e;border-left:3px solid #00c8ff;border-radius:8px;padding:12px;margin-bottom:12px;color:#6a9ab8;'>Editing: <b style='color:#00c8ff;'>{sel}</b> — {row['Fraud_Type']} — {row['Region']} — ₹{int(row['Loss_Amount']):,}</div>", unsafe_allow_html=True)
        c1,c2 = st.columns(2)
        FT = ["UPI Phishing","OTP Fraud","Investment Scam","Social Media Fraud","Email Phishing","Other"]
        ST = ["Under Investigation","Resolved","Closed"]
        with c1:
            nd  = st.date_input("📅 Tarikh", value=pd.to_datetime(row["Incident_Date"]).date())
            nft = st.selectbox("⚠️ Fraud Type", FT, index=FT.index(row["Fraud_Type"]) if row["Fraud_Type"] in FT else 0)
            na  = st.number_input("💸 Loss (₹)", min_value=0, step=500, value=int(row["Loss_Amount"]))
        with c2:
            nr  = st.text_input("📍 District", value=str(row["Region"]))
            ns  = st.text_input("🏛️ State", value=str(row["State"]))
            nag = st.number_input("👤 Age", min_value=1, max_value=100, value=int(row["Victim_Age"]))
            nst = st.selectbox("📋 Status", ST, index=ST.index(row["Status"]) if row["Status"] in ST else 0)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾 UPDATE KARO", use_container_width=True):
            df = get_df()
            i = df[df["Crime_ID"]==sel].index[0]
            df.at[i,"Incident_Date"]=pd.to_datetime(nd)
            df.at[i,"Fraud_Type"]=nft
            df.at[i,"Loss_Amount"]=na
            df.at[i,"Region"]=nr
            df.at[i,"State"]=ns
            df.at[i,"Victim_Age"]=nag
            df.at[i,"Status"]=nst
            save_df(df)
            st.success(f"✅ {sel} update ho gaya!")

    elif "🗑️" in menu:
        st.markdown("<h2 style='color:#fff;'>🗑️ Case Delete Karo</h2>", unsafe_allow_html=True)
        df = get_df()
        st.warning("⚠️ Delete karne ke baad wapas nahi aayega!")
        sel = st.selectbox("Case ID", df["Crime_ID"].tolist())
        row = df[df["Crime_ID"]==sel].iloc[0]
        st.markdown(f"<div style='background:#1a0505;border:1px solid #cc0000;border-radius:8px;padding:12px;margin:12px 0;'><b style='color:#ef4444;'>{sel}</b><br><span style='color:#6a9ab8;font-size:0.85rem;'>⚠️ {row['Fraud_Type']} | 📍 {row['Region']} | 💸 ₹{int(row['Loss_Amount']):,} | 📋 {row['Status']}</span></div>", unsafe_allow_html=True)
        if st.checkbox(f"Haan, {sel} delete karna chahta/chahti hun"):
            if st.button("🗑️ DELETE", use_container_width=True):
                save_df(df[df["Crime_ID"]!=sel].reset_index(drop=True))
                st.success(f"✅ {sel} delete ho gaya!")
                st.rerun()

    elif "📊" in menu:
        st.markdown("<h2 style='color:#fff;'>📊 Dashboard</h2>", unsafe_allow_html=True)
        df = get_df()
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("🗂️ Cases", len(df))
        c2.metric("💸 Loss", f"₹{df['Loss_Amount'].sum()/100000:.1f}L")
        c3.metric("📶 UPI%", f"{round(len(df[df['Fraud_Type']=='UPI Phishing'])/max(len(df),1)*100,1)}%")
        c4.metric("✅ Resolved", len(df[df['Status']=='Resolved']))
        l,r = st.columns(2)
        with l:
            fc = df["Fraud_Type"].value_counts().reset_index(); fc.columns=["Fraud_Type","Cases"]
            fig=px.bar(fc,x="Fraud_Type",y="Cases",color="Fraud_Type",color_discrete_sequence=PAL,text="Cases")
            fig.update_traces(textposition="outside",textfont=dict(color="#c8d8e8"))
            fig.update_xaxes(showgrid=False); fig.update_yaxes(gridcolor="#0a1f35"); fig.update_layout(showlegend=False)
            dark(fig,"FRAUD TYPES"); st.plotly_chart(fig,use_container_width=True)
        with r:
            gl=df.groupby("Region")["Loss_Amount"].sum().reset_index()
            fig2=px.pie(gl,names="Region",values="Loss_Amount",color_discrete_sequence=PAL,hole=0.42)
            fig2.update_traces(textfont=dict(color="#fff"),textinfo="percent+label")
            dark(fig2,"LOSS BY DISTRICT"); st.plotly_chart(fig2,use_container_width=True)
        st.dataframe(df,use_container_width=True,hide_index=True)
        buf=io.StringIO(); df.to_csv(buf,index=False)
        st.download_button("⬇️ Download CSV",data=buf.getvalue().encode(),file_name="cyber_data.csv",mime="text/csv")

def show_public():
    df = get_df()
    with st.sidebar:
        st.markdown("<div style='text-align:center;padding:10px 0 16px;'><div style='font-size:1.3rem;color:#00c8ff;font-weight:900;'>🛡️ CYBERSHIELD</div><div style='font-size:0.65rem;color:#1e4060;letter-spacing:2px;margin-top:3px;'>BIHAR CRIME ANALYSIS</div></div><div class='sos'><div style='font-size:0.6rem;color:#993333;letter-spacing:2px;margin-bottom:4px;'>🚨 CYBER CRIME EMERGENCY</div><div class='sos-num'>1930</div><div style='font-size:0.65rem;color:#cc6060;margin-top:4px;'>NATIONAL HELPLINE · 24/7 FREE</div></div>", unsafe_allow_html=True)
        sr = st.selectbox("📍 District", ["All Districts"]+sorted(df["Region"].unique().tolist()))
        sf = st.selectbox("⚠️ Fraud Type", ["All Types"]+sorted(df["Fraud_Type"].unique().tolist()))
        ss = st.selectbox("📋 Status", ["All Status"]+sorted(df["Status"].unique().tolist()))
        st.markdown("<div style='margin-top:14px;font-size:0.72rem;color:#2a5070;line-height:2;'><b style='color:#1e5070;font-size:0.65rem;'>◈ SAFETY TIPS</b><br>🔒 OTP kabhi share mat karo<br>📵 KYC SMS links ignore karo<br>💸 Guaranteed return = SCAM<br>🌐 cybercrime.gov.in</div>", unsafe_allow_html=True)
        st.markdown("---")
        if st.button("🔐 Admin Login", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()

    dff = df.copy()
    if sr!="All Districts": dff=dff[dff["Region"]==sr]
    if sf!="All Types":     dff=dff[dff["Fraud_Type"]==sf]
    if ss!="All Status":    dff=dff[dff["Status"]==ss]

    st.markdown("<div style='background:linear-gradient(135deg,#050d1a,#070f20);border:1px solid #0a1f35;border-radius:12px;padding:28px 36px;margin-bottom:24px;border-top:2px solid #00c8ff;'><div style='font-size:0.7rem;color:#1e5070;letter-spacing:3px;margin-bottom:8px;'>◈ AKU · BCA FINAL YEAR PROJECT · 2024-25</div><div style='font-size:1.8rem;font-weight:900;color:#ffffff;margin-bottom:8px;'>🛡️ Cyber-Crime Pattern Analysis &<br><span style='color:#00c8ff;'>Public Awareness System</span></div><div style='font-size:0.88rem;color:#4a7090;line-height:1.7;'>Bihar ke districts mein ho rahe digital frauds ka interactive dashboard. Sidebar se district select karo aur live data dekho.</div></div>", unsafe_allow_html=True)

    n=len(dff); tl=dff["Loss_Amount"].sum(); un=len(dff[dff["Fraud_Type"]=="UPI Phishing"])
    ur=round(un/max(n,1)*100,1); al=int(dff["Loss_Amount"].mean()) if n else 0; re=len(dff[dff["Status"]=="Resolved"])
    c1,c2,c3,c4,c5=st.columns(5)
    c1.metric("🗂️ Cases",n); c2.metric("💸 Loss",f"₹{tl/100000:.1f}L"); c3.metric("📶 UPI%",f"{ur}%"); c4.metric("💰 Avg",f"₹{al:,}"); c5.metric("✅ Resolved",re)
    st.markdown("<br>",unsafe_allow_html=True)

    t1,t2,t3,t4=st.tabs(["📊 CHARTS","🗺️ HOTSPOTS","📈 TRENDS","🗄️ DATABASE"])
    with t1:
        l,r=st.columns(2)
        with l:
            fc=dff["Fraud_Type"].value_counts().reset_index(); fc.columns=["Fraud_Type","Cases"]
            fig=px.bar(fc,x="Fraud_Type",y="Cases",color="Fraud_Type",color_discrete_sequence=PAL,text="Cases")
            fig.update_traces(textposition="outside",textfont=dict(color="#c8d8e8")); fig.update_xaxes(showgrid=False); fig.update_yaxes(gridcolor="#0a1f35"); fig.update_layout(showlegend=False)
            dark(fig,"FRAUD CATEGORY"); st.plotly_chart(fig,use_container_width=True)
        with r:
            gl=dff.groupby("Region")["Loss_Amount"].sum().reset_index()
            fig2=px.pie(gl,names="Region",values="Loss_Amount",color_discrete_sequence=PAL,hole=0.42)
            fig2.update_traces(textfont=dict(color="#fff"),textinfo="percent+label",marker=dict(line=dict(color="#04080f",width=2)))
            dark(fig2,"LOSS BY DISTRICT"); st.plotly_chart(fig2,use_container_width=True)
        l2,r2=st.columns(2)
        with l2:
            lf=dff.groupby("Fraud_Type")["Loss_Amount"].sum().reset_index().sort_values("Loss_Amount"); lf.columns=["Fraud_Type","Loss"]
            fig3=px.bar(lf,x="Loss",y="Fraud_Type",orientation="h",color="Loss",color_continuous_scale=["#001830","#00c8ff","#ef4444"],text=lf["Loss"].apply(lambda v:f"₹{v/100000:.1f}L"))
            fig3.update_traces(textposition="outside",textfont=dict(color="#c8d8e8")); fig3.update_xaxes(gridcolor="#0a1f35"); fig3.update_yaxes(gridcolor="rgba(0,0,0,0)"); fig3.update_layout(coloraxis_showscale=False)
            dark(fig3,"LOSS BY FRAUD TYPE"); st.plotly_chart(fig3,use_container_width=True)
        with r2:
            sc=dff["Status"].value_counts().reset_index(); sc.columns=["Status","Count"]
            fig4=px.bar(sc,x="Status",y="Count",color="Status",text="Count",color_discrete_map={"Resolved":"#22c55e","Under Investigation":"#f59e0b","Closed":"#4a6080"})
            fig4.update_traces(textposition="outside",textfont=dict(color="#c8d8e8")); fig4.update_xaxes(showgrid=False); fig4.update_yaxes(gridcolor="#0a1f35"); fig4.update_layout(showlegend=False)
            dark(fig4,"CASE STATUS"); st.plotly_chart(fig4,use_container_width=True)
    with t2:
        ra=dff.groupby("Region").agg(Cases=("Crime_ID","count"),Loss=("Loss_Amount","sum")).reset_index()
        fig5=px.bar(ra,x="Region",y="Cases",color="Loss",text="Cases",color_continuous_scale=["#001830","#00c8ff","#ef4444"])
        fig5.update_traces(textposition="outside",textfont=dict(color="#c8d8e8")); fig5.update_xaxes(showgrid=False,tickangle=-20); fig5.update_yaxes(gridcolor="#0a1f35")
        dark(fig5,"CASES PER DISTRICT"); st.plotly_chart(fig5,use_container_width=True)
        fig6=px.treemap(ra,path=["Region"],values="Cases",color="Loss",color_continuous_scale=["#001020","#003060","#00c8ff","#f59e0b","#ef4444"])
        fig6.update_layout(paper_bgcolor="rgba(0,0,0,0)",font=dict(color="#c8d8e8"),margin=dict(l=10,r=10,t=45,b=10),title=dict(text="DISTRICT HEATMAP",font=dict(size=12,color="#3a7fa8"),x=0))
        st.plotly_chart(fig6,use_container_width=True)
    with t3:
        d2=dff.copy(); d2["MonthSort"]=pd.to_datetime(d2["Incident_Date"]).dt.to_period("M").apply(lambda p:p.start_time)
        mo=d2.groupby(["MonthSort","Fraud_Type"]).agg(Cases=("Crime_ID","count")).reset_index().sort_values("MonthSort")
        fig7=px.line(mo,x="MonthSort",y="Cases",color="Fraud_Type",markers=True,color_discrete_sequence=PAL)
        fig7.update_xaxes(gridcolor="#0a1f35"); fig7.update_yaxes(gridcolor="#0a1f35")
        dark(fig7,"MONTHLY TREND"); st.plotly_chart(fig7,use_container_width=True)
        ml=d2.groupby("MonthSort")["Loss_Amount"].sum().reset_index().sort_values("MonthSort")
        fig8=px.area(ml,x="MonthSort",y="Loss_Amount",color_discrete_sequence=["#00c8ff"])
        fig8.update_traces(fillcolor="rgba(0,200,255,0.08)",line=dict(width=2.5)); fig8.update_xaxes(gridcolor="#0a1f35"); fig8.update_yaxes(gridcolor="#0a1f35")
        dark(fig8,"MONTHLY LOSS"); st.plotly_chart(fig8,use_container_width=True)
    with t4:
        search=st.text_input("🔍 Search karo",placeholder="e.g. Patna ya UPI Phishing")
        show=dff.copy()
        if search.strip():
            mask=show.apply(lambda col:col.astype(str).str.contains(search,case=False,na=False)).any(axis=1); show=show[mask]
        st.markdown(f"<p style='color:#1e5070;font-size:0.7rem;'>{len(show)} records</p>",unsafe_allow_html=True)
        st.dataframe(show,use_container_width=True,hide_index=True)
        buf=io.StringIO(); show.to_csv(buf,index=False)
        st.download_button("⬇️ Download CSV",data=buf.getvalue().encode(),file_name="cyber_data.csv",mime="text/csv")

    st.markdown("<div style='text-align:center;font-size:0.62rem;color:#0d2a42;padding:16px 0;margin-top:20px;'>CYBERSHIELD BIHAR · BCA FINAL YEAR PROJECT · AKU 2024-25</div>",unsafe_allow_html=True)

if st.session_state.page == "login":
    show_login()
elif st.session_state.page == "admin" and st.session_state.logged_in:
    show_admin()
else:
    show_public()

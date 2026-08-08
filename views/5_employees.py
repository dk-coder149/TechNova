import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px



# -----------------------------------------------------------------
# DATA LOADING (WITH FALLBACK)
# -----------------------------------------------------------------
@st.cache_data
def get_employee_data():
    try:
        from queries import load_employee_analytics
        return load_employee_analytics()
    except Exception:
        np.random.seed(104)
        names = ["Amit Sharma", "Priya Singh", "Rohan Mehta", "Neha Gupta", "Vikram Patel", "Suresh Kumar"]
        regions = ["North", "South", "East", "West", "Central", "North"]
        
        df = pd.DataFrame({
            "employee_id": [f"EMP-{100+i}" for i in range(len(names))],
            "employee_name": names,
            "region": regions,
            "sales_target": np.random.uniform(500000, 1000000, size=len(names)).round(2),
            "sales_achieved": np.random.uniform(400000, 1200000, size=len(names)).round(2),
            "deals_closed": np.random.randint(15, 60, size=len(names))
        })
        df["achievement_rate"] = ((df["sales_achieved"] / df["sales_target"]) * 100).round(2)
        return df

df_emp = get_employee_data()

# -----------------------------------------------------------------
# HEADER & KPIS
# -----------------------------------------------------------------
st.title("👨‍💼 Sales Representative Performance")
st.markdown("Monitor team productivity, individual achievements, and regional sales distribution.")

total_team = len(df_emp)
total_team_sales = df_emp["sales_achieved"].sum()
avg_achievement = df_emp["achievement_rate"].mean()
top_rep = df_emp.sort_values("sales_achieved", ascending=False).iloc[0]["employee_name"]

k1, k2, k3, k4 = st.columns(4)
k1.metric("Active Sales Reps", f"{total_team}")
k2.metric("Total Team Sales", f"₹{total_team_sales/1e5:.2f} L")
k3.metric("Avg Target Achieved", f"{avg_achievement:.1f}%")
k4.metric("Top Performer", top_rep)

st.markdown("---")

# -----------------------------------------------------------------
# CHARTS
# -----------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🎯 Sales Target vs Achievement")
    fig_emp = px.bar(df_emp, x="employee_name", y=["sales_target", "sales_achieved"], barmode="group", labels={"value": "Amount (₹)", "employee_name": "Sales Rep"})
    st.plotly_chart(fig_emp, use_container_width=True)

with col2:
    st.subheader("🗺️ Region-wise Team Contribution")
    region_emp = df_emp.groupby("region")["sales_achieved"].sum().reset_index()
    fig_reg = px.pie(region_emp, names="region", values="sales_achieved", hole=0.4)
    st.plotly_chart(fig_reg, use_container_width=True)

st.subheader("📋 Leaderboard & Performance Scorecard")
st.dataframe(df_emp.sort_values("sales_achieved", ascending=False), use_container_width=True, hide_index=True)



#########################################


@st.cache_data(ttl=3600)
def get_employee_data():
    try:
        from queries import load_employee_analytics
        df = load_employee_analytics()
        if df.empty: raise ValueError
    except Exception:
        np.random.seed(42)
        names = ["Aarav Sharma", "Priya Verma", "Rohan Mehta", "Neha Gupta", "Vikram Singh", "Ananya Reddy"]
        depts = ["North Region", "South Region", "West Region", "East Region"]
        n = len(names)
        
        targets = np.random.uniform(500000, 1500000, size=n).round(0)
        achieved = targets * np.random.uniform(0.7, 1.4, size=n)
        
        df = pd.DataFrame({
            "employee_id": [f"EMP-{101+i}" for i in range(n)],
            "employee_name": names,
            "department": np.random.choice(depts, size=n),
            "sales_target": targets,
            "sales_achieved": achieved.round(2),
            "deals_closed": np.random.randint(10, 60, size=n)
        })
        
    df["achievement_rate"] = ((df["sales_achieved"] / df["sales_target"]) * 100).round(2)
    # Incentives Rule: 5% bonus if target achieved >= 100%
    df["incentive"] = np.where(df["achievement_rate"] >= 100, df["sales_achieved"] * 0.05, 0.0).round(2)
    return df

df_emp = get_employee_data()

# Ranking Sort
df_emp = df_emp.sort_values(by="achievement_rate", ascending=False).reset_index(drop=True)
df_emp["rank"] = df_emp.index + 1

# Metrics
e1, e2, e3, e4 = st.columns(4)
e1.metric("Top Sales Rep", df_emp.iloc[0]["employee_name"])
e2.metric("Total Team Achieved", f"₹{df_emp['sales_achieved'].sum():,.2f}")
e3.metric("Avg Target Completion", f"{df_emp['achievement_rate'].mean():.1f}%")
e4.metric("Total Payout Incentives", f"₹{df_emp['incentive'].sum():,.2f}")

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["🏆 Performance Ranking & Sales", "💰 Incentive Calculator", "🏢 Department Performance"])

with tab1:
    st.subheader("Sales Representative Leaderboard")
    fig_rank = px.bar(df_emp, x="achievement_rate", y="employee_name", orientation="h", color="achievement_rate",
                      labels={"achievement_rate": "Target Achievement (%)"}, title="Target Achievement Rate (%)")
    fig_rank.add_vline(x=100, line_dash="dash", line_color="red", annotation_text="Target Line")
    fig_rank.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_rank, use_container_width=True)

with tab2:
    st.subheader("Calculated Commission & Incentives")
    st.dataframe(df_emp[["rank", "employee_name", "sales_target", "sales_achieved", "achievement_rate", "incentive"]], use_container_width=True)

with tab3:
    st.subheader("Department / Regional Sales Breakdown")
    dept_df = df_emp.groupby("department")[["sales_target", "sales_achieved"]].sum().reset_index()
    fig_dept = px.bar(dept_df, x="department", y=["sales_target", "sales_achieved"], barmode="group",
                      title="Target vs Achieved by Department")
    st.plotly_chart(fig_dept, use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="L'Oréal Financial Intelligence",
    page_icon="📊",
    layout="wide"
)

# Historical figures in EUR millions
data = {
    "Year": [2022, 2023, 2024],
    "Sales": [38260.6, 41182.5, 43486.8],
    "Net_Profit": [5712.6, 6190.5, 6416.5],
    "Profit_Attributable": [5706.6, 6184.0, 6408.7],
    "Total_Assets": [46844.2, 51855.1, 56353.4],
    "Shareholders_Equity": [27178.5, 29074.3, 33133.3]
}

df = pd.DataFrame(data)
df["Profit_Margin"] = df["Net_Profit"] / df["Sales"] * 100
df["Sales_Growth"] = df["Sales"].pct_change() * 100
df["Average_Assets"] = (
    df["Total_Assets"] + df["Total_Assets"].shift(1)
) / 2
df["Average_Equity"] = (
    df["Shareholders_Equity"]
    + df["Shareholders_Equity"].shift(1)
) / 2
df["ROA"] = df["Net_Profit"] / df["Average_Assets"] * 100
df["ROE"] = (
    df["Profit_Attributable"] / df["Average_Equity"] * 100
)

st.title("L'ORÉAL | Financial Intelligence")
st.caption("Interactive Financial Performance Dashboard | 2022–2024")

st.sidebar.header("Dashboard Controls")
selected_years = st.sidebar.multiselect(
    "Select financial years",
    options=df["Year"].tolist(),
    default=df["Year"].tolist()
)

filtered = df[df["Year"].isin(selected_years)].copy()

if filtered.empty:
    st.warning("Please select at least one year.")
    st.stop()

latest = filtered.sort_values("Year").iloc[-1]

st.subheader(f"Financial Snapshot — {int(latest['Year'])}")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Revenue", f"€{latest['Sales']/1000:.2f}B")
c2.metric("Net Profit", f"€{latest['Net_Profit']/1000:.2f}B")
c3.metric("Profit Margin", f"{latest['Profit_Margin']:.2f}%")
c4.metric(
    "Return on Equity",
    f"{latest['ROE']:.2f}%" if pd.notna(latest["ROE"]) else "N/A"
)

left, right = st.columns(2)

with left:
    st.subheader("Revenue Trend")
    fig = px.bar(
        filtered, x="Year", y="Sales",
        color_discrete_sequence=["#38BDF8"],
        labels={"Sales": "Revenue (€ millions)"}
    )
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Net Profit Trend")
    fig = px.line(
        filtered, x="Year", y="Net_Profit",
        markers=True,
        labels={"Net_Profit": "Net Profit (€ millions)"}
    )
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

left2, right2 = st.columns(2)

with left2:
    st.subheader("Net Profit Margin")
    fig = px.line(
        filtered, x="Year", y="Profit_Margin",
        markers=True,
        labels={"Profit_Margin": "Margin (%)"}
    )
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

with right2:
    st.subheader("Return on Assets vs Equity")
    ratios = filtered.melt(
        id_vars="Year",
        value_vars=["ROA", "ROE"],
        var_name="Ratio",
        value_name="Percentage"
    )
    fig = px.line(
        ratios, x="Year", y="Percentage",
        color="Ratio", markers=True
    )
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Financial Data")
st.dataframe(filtered, use_container_width=True)

st.download_button(
    "Download Financial Data (CSV)",
    filtered.to_csv(index=False).encode("utf-8"),
    file_name="loreal_financial_data.csv",
    mime="text/csv"
)

st.caption(
    "Source: L'Oréal 2024 Universal Registration Document. "
    "ROA and ROE use average balance-sheet values; "
    "2022 returns are unavailable without 2021 balances."
)

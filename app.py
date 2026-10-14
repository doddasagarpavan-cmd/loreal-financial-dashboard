import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="L'Oréal | Financial Intelligence", page_icon="📈", layout="wide")

BG = '#0B1220'
PANEL = '#172338'
CYAN = '#38BDF8'
GREEN = '#34D399'
GOLD = '#FBBF24'
PURPLE = '#A78BFA'

st.markdown('''<style>
.stApp {background-color:#0B1220;color:#F8FAFC;}
[data-testid="stSidebar"] {background-color:#121D30;}
[data-testid="stMetric"] {background-color:#172338;border:1px solid #263850;border-radius:14px;padding:18px;}
[data-testid="stMetricLabel"] {color:#9CAFC7;}
h1,h2,h3 {letter-spacing:-.02em;}
.block-container {padding-top:2rem;}
</style>''', unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.DataFrame({
        'Year':[2022,2023,2024],
        'Sales':[38260.6,41182.5,43486.8],
        'Net_Profit':[5712.6,6190.5,6416.5],
        'Profit_Attributable':[5706.6,6184.0,6408.7],
        'Total_Assets':[46844.2,51855.1,56353.4],
        'Shareholders_Equity':[27178.5,29074.3,33133.3],
    })
    df['Profit_Margin'] = df['Net_Profit']/df['Sales']*100
    df['Sales_Growth'] = df['Sales'].pct_change()*100
    df['Profit_Growth'] = df['Net_Profit'].pct_change()*100
    df['Average_Assets'] = (df['Total_Assets']+df['Total_Assets'].shift(1))/2
    df['Average_Equity'] = (df['Shareholders_Equity']+df['Shareholders_Equity'].shift(1))/2
    df['ROA'] = df['Net_Profit']/df['Average_Assets']*100
    df['ROE'] = df['Profit_Attributable']/df['Average_Equity']*100
    return df

df = load_data()

st.sidebar.title('📈 FINANCIAL INTELLIGENCE')
st.sidebar.caption('L’Oréal | Historical analysis')
page = st.sidebar.radio('Navigation', ['Overview','Financial Trends','Returns & Ratios','Data & Sources'])
selected_years = st.sidebar.multiselect('Financial years', df['Year'].tolist(), default=df['Year'].tolist())
st.sidebar.caption('Data: EUR millions · 2022–2024')

if not selected_years:
    st.warning('Select at least one financial year in the sidebar.')
    st.stop()

filtered = df[df['Year'].isin(selected_years)].sort_values('Year')
latest = filtered.iloc[-1]
# Compare against the actual preceding year, even if filtered out of the chart.
previous = df[df['Year'] == latest['Year']-1]
previous = previous.iloc[0] if not previous.empty else None

def delta(current, prior, percent=False):
    if prior is None or pd.isna(current) or pd.isna(prior):
        return None
    return f'{current-prior:+.2f} pp' if percent else f'{(current/prior-1)*100:+.2f}% YoY' if prior else None

def style_chart(fig, percent=False):
    fig.update_layout(template='plotly_dark', paper_bgcolor=PANEL, plot_bgcolor=PANEL,
                      font_color='#E5EDF8', margin=dict(l=25,r=20,t=35,b=30),
                      hovermode='x unified', legend_title_text='')
    fig.update_xaxes(type='category', showgrid=False)
    fig.update_yaxes(gridcolor='#304159', zeroline=False, ticksuffix='%' if percent else '')
    return fig

st.title('L’ORÉAL  |  FINANCIAL INTELLIGENCE')
st.caption('Interactive historical financial analysis · 2022–2024 · Figures in EUR millions unless stated')

if page == 'Overview':
    st.subheader(f'Executive snapshot · {int(latest["Year"])}')
    c1,c2,c3,c4 = st.columns(4)
    c1.metric('Revenue',f'€{latest["Sales"]/1000:.2f}B',delta(latest['Sales'], previous['Sales'] if previous is not None else None))
    c2.metric('Net profit',f'€{latest["Net_Profit"]/1000:.2f}B',delta(latest['Net_Profit'], previous['Net_Profit'] if previous is not None else None))
    c3.metric('Net margin',f'{latest["Profit_Margin"]:.2f}%',delta(latest['Profit_Margin'], previous['Profit_Margin'] if previous is not None else None, True))
    c4.metric('ROE',f'{latest["ROE"]:.2f}%' if pd.notna(latest['ROE']) else 'N/A',delta(latest['ROE'],previous['ROE'] if previous is not None else None,True))
    left,right = st.columns(2)
    with left:
        st.subheader('Revenue evolution')
        fig = px.bar(filtered,x='Year',y='Sales',color_discrete_sequence=[CYAN],text='Sales')
        fig.update_traces(texttemplate='€%{text:,.0f}M',textposition='outside')
        st.plotly_chart(style_chart(fig),use_container_width=True)
    with right:
        st.subheader('Profitability evolution')
        fig = px.line(filtered,x='Year',y='Net_Profit',markers=True,color_discrete_sequence=[GREEN])
        fig.update_traces(line_width=3)
        st.plotly_chart(style_chart(fig),use_container_width=True)
    st.subheader('Analyst observations')
    if previous is not None:
        st.write(f"**Revenue:** {delta(latest['Sales'],previous['Sales'])} compared with {int(previous['Year'])}.")
        st.write(f"**Net profit:** {delta(latest['Net_Profit'],previous['Net_Profit'])} compared with {int(previous['Year'])}.")
        st.write(f"**Net margin:** {latest['Profit_Margin']:.2f}% ({delta(latest['Profit_Margin'],previous['Profit_Margin'],True)} versus prior year).")
    else:
        st.info('2022 is the first year in this dataset; prior-year growth is unavailable.')
    st.caption('Observations are descriptive, not explanations of causation.')
    st.divider()
    st.subheader("Executive Financial Analysis")

    st.info(
        "L'Oréal recorded revenue and net profit growth "
        "between 2022 and 2024. However, profitability "
        "ratios weakened in 2024, indicating that "
        "financial performance should be assessed "
        "beyond headline revenue growth."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Revenue & Profitability")
        st.write(
            "In 2024, revenue increased by approximately "
            "5.60%, while net profit grew by 3.65%. "
            "Because profit grew more slowly than sales, "
            "the net profit margin declined."
        )

    with col2:
        st.markdown("#### Shareholder Returns")
        st.write(
            "Return on Equity declined from approximately "
            "21.99% in 2023 to 20.60% in 2024. "
            "This suggests that average shareholders' "
            "equity grew faster than profit attributable "
            "to shareholders."
        )

    st.markdown("#### Questions for Further Investigation")

    st.markdown("""
    - Which operating expenses contributed to changes
      in profitability?
    - Did acquisitions or investments contribute to
      growth in total assets?
    - How did changes in shareholders' equity affect ROE?
    - Can L'Oréal sustain revenue growth while
      improving its profitability ratios?
    """)

    st.caption(
        "Analysis based on historical consolidated "
        "financial figures. Potential drivers require "
        "verification against the annual report."
    )
    st.divider()
    st.subheader("Financial Health Analysis")

    asset_growth = (
        df.loc[df["Year"] == 2024, "Total_Assets"].iloc[0]
        / df.loc[df["Year"] == 2023, "Total_Assets"].iloc[0]
        - 1
    ) * 100

    equity_growth = (
        df.loc[df["Year"] == 2024, "Shareholders_Equity"].iloc[0]
        / df.loc[df["Year"] == 2023, "Shareholders_Equity"].iloc[0]
        - 1
    ) * 100

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Assets (2024)",
            "€56.35B",
            f"+{asset_growth:.2f}% vs 2023"
        )

    with col2:
        st.metric(
            "Shareholders' Equity (2024)",
            "€33.13B",
            f"+{equity_growth:.2f}% vs 2023"
        )

    st.markdown("#### Financial Interpretation")

    st.write(
        f"L'Oréal's total assets increased by {asset_growth:.2f}% "
        f"in 2024, while shareholders' equity increased by "
        f"{equity_growth:.2f}%. Despite these increases, "
        "ROA and ROE declined, indicating that earnings "
        "grew more slowly than the average asset and "
        "equity bases."
    )

    st.info(
        "Analyst insight: Asset and equity growth should "
        "be evaluated alongside profitability and capital "
        "efficiency. Higher assets do not automatically "
        "mean stronger financial returns."
    )



elif page == 'Financial Trends':
    st.subheader('Financial performance trends')
    metric = st.selectbox('Choose a financial metric',['Sales','Net_Profit','Total_Assets','Shareholders_Equity'])
    fig = px.line(filtered,x='Year',y=metric,markers=True,color_discrete_sequence=[CYAN])
    fig.update_traces(line_width=4,marker_size=10)
    st.plotly_chart(style_chart(fig),use_container_width=True)
    st.subheader('Annual growth rates')
    growth = filtered.melt(id_vars='Year',value_vars=['Sales_Growth','Profit_Growth'],var_name='Metric',value_name='Growth (%)')
    fig = px.bar(growth,x='Year',y='Growth (%)',color='Metric',barmode='group',color_discrete_sequence=[CYAN,GREEN])
    st.plotly_chart(style_chart(fig,True),use_container_width=True)
    st.caption('Growth rates use the complete underlying dataset, even when a year is hidden by the filter.')

elif page == 'Returns & Ratios':
    st.subheader('Profitability and capital efficiency')
    a,b = st.columns(2)
    with a:
        fig = px.line(filtered,x='Year',y='Profit_Margin',markers=True,color_discrete_sequence=[GOLD])
        st.plotly_chart(style_chart(fig,True),use_container_width=True)
    with b:
        ratios = filtered.melt(id_vars='Year',value_vars=['ROA','ROE'],var_name='Ratio',value_name='Value (%)')
        fig = px.line(ratios,x='Year',y='Value (%)',color='Ratio',markers=True,color_discrete_map={'ROA':CYAN,'ROE':PURPLE})
        st.plotly_chart(style_chart(fig,True),use_container_width=True)
    st.info('2022 ROA and ROE are unavailable because 2021 balance-sheet figures have not been entered.')
    st.markdown('**Method:** ROA = consolidated net profit / average total assets. ROE = profit attributable to owners / average equity attributable to owners. Ratios use year-end balances averaged across consecutive years.')

else:
    st.subheader('Financial data and methodology')
    st.dataframe(filtered.style.format(precision=2,na_rep='N/A'),use_container_width=True)
    st.download_button('⬇ Download filtered data (CSV)',filtered.to_csv(index=False).encode('utf-8'),file_name='loreal_financial_data.csv',mime='text/csv')
    st.markdown('**Primary source:** [L’Oréal 2024 Universal Registration Document](https://www.loreal-finance.com/site/URD24/app/en/uploads/2074/Document/loreal-urd-2024-en.82fc3.pdf)')
    st.warning('Figures were manually transcribed for this educational project. Cross-check them against the original consolidated financial statements before external publication or investment use.')
    st.caption('Net profit and profit attributable to owners are distinct measures. 2022 ROA and ROE need 2021 opening balances.')

st.divider()
st.caption('Independent educational portfolio project · Not investment advice · L’Oréal is not affiliated with this dashboard.')

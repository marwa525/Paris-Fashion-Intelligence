import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from data import fetch_brand_data

st.set_page_config(
    page_title="Paris Fashion Intelligence",
    page_icon="🗼",
    layout="wide"
)

st.markdown("""
<style>
    .block-container{padding:2rem 3rem}
</style>
""", unsafe_allow_html=True)

st.markdown("## 🗼 paris.ai — fashion intelligence")
st.markdown("NLP sentiment analysis · Live data · 5 luxury houses")
st.markdown("---")

# ─────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────

st.sidebar.title("⚙️ Settings")
st.sidebar.markdown("---")

api_key = st.sidebar.text_input(
    "NewsAPI Key",
    type="password",
    help="Get free key at newsapi.org"
)

brands_input = st.sidebar.multiselect(
    "Select brands to analyze",
    options=[
        'Louis Vuitton',
        'Hermes',
        'Chanel',
        'Dior',
        'Balenciaga',
        'Gucci',
        'Prada',
        'Valentino',
        'Givenchy',
        'Saint Laurent'
    ],
    default=[
        'Louis Vuitton',
        'Hermes',
        'Chanel',
        'Dior',
        'Balenciaga'
    ]
)

time_period = st.sidebar.selectbox(
    "Time period",
    options=[
        'Last 7 days',
        'Last 14 days',
        'Last 30 days'
    ],
    index=2
)

refresh = st.sidebar.button(
    "🔄 Fetch Fresh Data",
    use_container_width=True
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Built by Marwa Zulfiqar**\n\n"
    "Data Engineer | paris.ai\n\n"
    "Paris, France 🗼"
)

# ─────────────────────────────────────
# COLOR FUNCTION
# ─────────────────────────────────────

def get_color(score):
    if score >= 10:
        return '#378ADD'
    elif score >= 7:
        return '#85B7EB'
    elif score >= 4:
        return '#B5D4F4'
    else:
        return '#EF9F27'

# ─────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────

default_data = {
    'brand': [
        'Dior', 'Louis Vuitton',
        'Chanel', 'Balenciaga', 'Hermes'
    ],
    'total_articles': [99, 94, 94, 98, 100],
    'positive': [14, 14, 11, 12, 5],
    'negative': [2, 4, 3, 4, 4],
    'neutral': [83, 76, 80, 82, 91],
    'sentiment_score': [
        12.1, 10.6, 8.5, 8.2, 1.0
    ]
}

if not api_key:
    st.info(
        "💡 Enter your NewsAPI key in "
        "the sidebar to load live data. "
        "Showing last analysis results."
    )
    df = pd.DataFrame(default_data)

else:
    cache_key = f"{brands_input}_{time_period}"

    if (
        refresh or
        'df' not in st.session_state or
        st.session_state.get(
            'cache_key'
        ) != cache_key
    ):
        with st.spinner(
            f"Analyzing {len(brands_input)} "
            f"brands... takes ~30 seconds"
        ):
            df = fetch_brand_data(
                api_key,
                brands=brands_input,
                time_period=time_period
            )
            st.session_state['df'] = df
            st.session_state[
                'cache_key'
            ] = cache_key
            st.success("✅ Live data loaded!")
    else:
        df = st.session_state['df']

# ─────────────────────────────────────
# METRICS
# ─────────────────────────────────────

total_articles = int(
    df['total_articles'].sum()
)
top_brand = df.iloc[0]['brand']
top_score = df.iloc[0]['sentiment_score']
avg_score = round(
    df['sentiment_score'].mean(), 1
)
gap = round(
    df['sentiment_score'].max() -
    df['sentiment_score'].min(), 1
)

col1, col2, col3, col4 = st.columns(4)
col1.metric(
    "Articles analyzed",
    total_articles
)
col2.metric(
    "Sentiment leader",
    top_brand,
    f"{top_score}%"
)
col3.metric(
    "Average sentiment",
    f"{avg_score}%"
)
col4.metric(
    "Sentiment gap",
    f"{gap} pts"
)

st.markdown("---")

# ─────────────────────────────────────
# CHART 1 — SENTIMENT RANKING
# ─────────────────────────────────────

left, right = st.columns(2)

with left:
    st.subheader("Sentiment score ranking")

    colors = [
        get_color(s)
        for s in df['sentiment_score']
    ]

    fig1 = go.Figure(go.Bar(
        x=df['sentiment_score'],
        y=df['brand'],
        orientation='h',
        marker_color=colors,
        text=[
            f"{s}%"
            for s in df['sentiment_score']
        ],
        textposition='outside'
    ))

    fig1.update_layout(
        height=300,
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        margin=dict(l=10, r=50, t=10, b=10),
        xaxis=dict(
            title="Sentiment %",
            gridcolor='#f0f0f0',
            range=[
                0,
                df['sentiment_score'].max() + 4
            ]
        ),
        yaxis=dict(
            autorange='reversed'
        )
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

# ─────────────────────────────────────
# CHART 2 — ARTICLE BREAKDOWN
# ─────────────────────────────────────

with right:
    st.subheader("Article breakdown")

    fig2 = go.Figure()

    fig2.add_trace(go.Bar(
        name='Positive',
        x=df['brand'],
        y=df['positive'],
        marker_color='#639922',
        text=df['positive'],
        textposition='auto'
    ))

    fig2.add_trace(go.Bar(
        name='Neutral',
        x=df['brand'],
        y=df['neutral'],
        marker_color='#B4B2A9',
        text=df['neutral'],
        textposition='auto'
    ))

    fig2.add_trace(go.Bar(
        name='Negative',
        x=df['brand'],
        y=df['negative'],
        marker_color='#E24B4A',
        text=df['negative'],
        textposition='auto'
    ))

    fig2.update_layout(
        height=300,
        barmode='group',
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(
            orientation='h',
            y=1.15
        ),
        yaxis=dict(
            gridcolor='#f0f0f0'
        )
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ─────────────────────────────────────
# CHART 3 — SCATTER PLOT
# ─────────────────────────────────────

st.markdown("---")
st.subheader("Volume vs sentiment")

fig3 = go.Figure()

for i, row in df.iterrows():
    fig3.add_trace(go.Scatter(
        x=[row['total_articles']],
        y=[row['sentiment_score']],
        mode='markers+text',
        name=row['brand'],
        text=[row['brand']],
        textposition='top center',
        marker=dict(
            size=18,
            color=get_color(
                row['sentiment_score']
            )
        )
    ))

fig3.update_layout(
    height=380,
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=10, r=10, t=30, b=10),
    xaxis=dict(
        title="Article volume",
        gridcolor='#f0f0f0'
    ),
    yaxis=dict(
        title="Sentiment score %",
        gridcolor='#f0f0f0'
    )
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ─────────────────────────────────────
# KEY INSIGHTS
# ─────────────────────────────────────

st.markdown("---")
st.subheader("Key insights")

winner = df.iloc[0]
loser = df.iloc[-1]
most_articles = df.loc[
    df['total_articles'].idxmax()
]

c1, c2, c3 = st.columns(3)

with c1:
    st.success(
        f"**Sentiment leader**\n\n"
        f"**{winner['brand']}** leads at "
        f"{winner['sentiment_score']}% with "
        f"{winner['positive']} positive and "
        f"only {winner['negative']} negative "
        f"articles."
    )

with c2:
    st.info(
        f"**Most covered brand**\n\n"
        f"**{most_articles['brand']}** has "
        f"the highest article volume at "
        f"{most_articles['total_articles']} "
        f"articles with "
        f"{most_articles['sentiment_score']}% "
        f"sentiment."
    )

with c3:
    st.warning(
        f"**Needs attention**\n\n"
        f"**{loser['brand']}** has the "
        f"lowest sentiment at "
        f"{loser['sentiment_score']}% with "
        f"{loser['negative']} negative "
        f"articles out of "
        f"{loser['total_articles']} total."
    )

# ─────────────────────────────────────
# RAW DATA TABLE
# ─────────────────────────────────────

st.markdown("---")
st.subheader("Raw data")

st.dataframe(
    df.rename(columns={
        'brand': 'Brand',
        'total_articles': 'Total Articles',
        'positive': 'Positive',
        'negative': 'Negative',
        'neutral': 'Neutral',
        'sentiment_score': 'Sentiment %'
    }),
    use_container_width=True,
    hide_index=True
)

csv = df.to_csv(index=False)
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='paris_fashion_sentiment.csv',
    mime='text/csv'
)

# ─────────────────────────────────────
# FOOTER
# ─────────────────────────────────────

st.markdown("---")
st.markdown(
    "Built with Python · NewsAPI · "
    "NLP · Plotly · "
    "by Marwa Zulfiqar 🗼"
)
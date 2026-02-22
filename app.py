import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# LOAD DATA
df = pd.read_csv("data/bwf_ms_matches.csv")
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["year"] = df["date"].dt.year

# TITLE
st.title("BWF Men's Singles Badminton Dashboard")

st.markdown("""
### Analytical Objective
This dashboard examines men's singles badminton tournaments to identify trends in match activity over time, evaluate match competitiveness, and understand how events are distributed across different countries.
""")

# SIDEBAR FILTERS
st.sidebar.header("Filters")

year_range = st.sidebar.slider(
    "Select Year Range",
    int(df["year"].min()),
    int(df["year"].max()),
    (int(df["year"].min()), int(df["year"].max()))
)

tournament_type = st.sidebar.multiselect(
    "Tournament Type",
    df["tournament_type"].dropna().unique(),
    default=df["tournament_type"].dropna().unique()
)

filtered = df[
    (df["year"].between(year_range[0], year_range[1])) &
    (df["tournament_type"].isin(tournament_type))
]

# METRICS
col1, col2, col3 = st.columns(3)
col1.metric("Total Matches", len(filtered))
col2.metric("Tournaments", filtered["tournament"].nunique())
col3.metric("Countries Hosting", filtered["country"].nunique())

# TABS
tab1, tab2 = st.tabs(["Tournament Trends", "Match Analysis"])

# TAB 1
with tab1:
    st.header("Tournament Activity")

    matches_per_year = filtered.groupby("year").size().reset_index(name="matches")
    st.plotly_chart(px.line(matches_per_year, x="year", y="matches",
                            title="Matches per Year"), use_container_width=True)
    st.markdown("""
    ### Interpretation
    This chart shows how tournament activity changes over time. Variations in match numbers reflect changes in scheduling, competition frequency, or external factors affecting badminton events.
    """)
    matches_by_type = filtered["tournament_type"].value_counts().reset_index()
    matches_by_type.columns = ["tournament_type", "matches"]

    st.plotly_chart(px.bar(matches_by_type,
                           x="tournament_type",
                           y="matches",
                           title="Matches by Tournament Type"),
                    use_container_width=True)

    st.markdown("""
### Interpretation
This chart compares match counts across tournament levels. It shows which types of competitions contribute most to overall match activity.
""")

# TAB 2
with tab2:
    st.header("Match Characteristics")

    st.plotly_chart(px.scatter(filtered,
                               x="team_one_total_points",
                               y="team_two_total_points",
                               color="nb_sets",
                               title="Points Scored by Each Team"),
                    use_container_width=True)
    st.markdown("""
    ### Interpretation
    This chart shows how closely matched competitors are. Similar point totals indicate competitive matches, while large differences suggest dominant performances.
    """)

    heat = filtered.pivot_table(index="country",
                                columns="year",
                                values="tournament",
                                aggfunc="count",
                                fill_value=0)

    st.plotly_chart(px.imshow(heat,
                              text_auto=True,
                              title="Matches Hosted by Country and Year"),
                    use_container_width=True)

    st.markdown("""
### Interpretation
This chart shows where tournaments are hosted and how hosting patterns change over time. Higher match counts highlight countries that are major centers for badminton events.
""")


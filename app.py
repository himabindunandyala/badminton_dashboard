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
This dashboard analyzes men's singles badminton tournaments to understand how match activity changes over time, how competitive matches are based on scoring patterns, and which countries host the most events. The goal is to understand how global badminton competitions are structured and how they vary across seasons and locations.
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

st.sidebar.subheader("Player Filter")

all_players = pd.concat([
    df["team_one_players"],
    df["team_two_players"]
]).dropna().unique()

selected_player = st.sidebar.selectbox(
    "Select Player",
    sorted(all_players)
)

filtered = df[
    (df["year"].between(year_range[0], year_range[1])) &
    (df["tournament_type"].isin(tournament_type))
]

player_matches = filtered[
    (filtered["team_one_players"] == selected_player) |
    (filtered["team_two_players"] == selected_player)
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
    From the yearly trend, match activity does not stay the same every year. Some years have noticeably more matches, while others show drops, which may reflect changes in tournament scheduling or external factors affecting competitions. This shows that badminton activity is influenced by how the international tournament calendar is organized. 
    """)
    matches_by_type = filtered["tournament_type"].value_counts().reset_index()
    matches_by_type.columns = ["tournament_type", "matches"]

    st.plotly_chart(px.bar(matches_by_type,
                           x="tournament_type",
                           y="matches",
                           title="Matches by Tournament Type"),
                    use_container_width=True)

    st.markdown("""
Looking at tournament types, some categories clearly host more matches than others. This suggests that certain competition levels play a bigger role in the sport and provide more opportunities for players to compete. Overall, these patterns help explain how badminton tournaments are structured and how competition activity changes over time.
""")

    st.subheader("Tournament Type Share")

    type_counts = filtered["tournament_type"].value_counts().reset_index()
    type_counts.columns = ["tournament_type", "matches"]

    fig_pie = px.pie(type_counts,
                 names="tournament_type",
                 values="matches",
                 title="Share of Matches by Tournament Type",
                 hole=0.3)   

    st.plotly_chart(fig_pie, use_container_width=True)

# TAB 2
with tab2:
  st.header("Match Characteristics")

  st.subheader("Selected Player Analysis")

  st.write("Player:", selected_player)
  st.write("Matches played:", len(player_matches))
  st.dataframe(player_matches[[
      "tournament",
      "country",
      "date",
      "winner",
      "nb_sets"
]])

  st.plotly_chart(px.scatter(filtered,
                       x="team_one_total_points",
                       y="team_two_total_points",
                       color="nb_sets",
                       title="Points Scored by Each Team"),
            use_container_width=True)
  st.markdown("""
The points comparison shows that many matches are fairly close, which suggests that players are often evenly matched and competition is strong. However, some matches show large differences in points, which indicates dominant performances where one side clearly outplayed the other.
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
The country heatmap shows that tournaments are not evenly spread around the world. Some countries host many more matches than others, which suggests they play a major role in organizing international badminton events. Changes across years also show that hosting patterns can shift over time. Together, this helps explain both match competitiveness and the global distribution of tournaments.
""")

  st.subheader("Score Distribution by Match Length")

  filtered["total_points"] = (
    filtered["team_one_total_points"] +
    filtered["team_two_total_points"]
)

  fig_box = px.box(filtered,
                 x="nb_sets",
                 y="total_points",
                 color="nb_sets",
                 title="Distribution of Total Points by Number of Sets")

  st.plotly_chart(fig_box, use_container_width=True)

  










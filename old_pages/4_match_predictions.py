from typing import List
import pandas as pd
import streamlit as st

from old_pages.data_pull import read_match_scouting_data


if __name__ == "__main__":
    st.set_page_config(
        page_title="Match Analytics",
        layout="wide",
    )
    st.title("Match Predictions")

    match_data: pd.DataFrame = read_match_scouting_data()

    column1, column2, column3 = st.columns(3)

    event: str = ""
    red_alliance: List[str] = []
    blue_alliance: List[str] = []

    with column1:
        event = st.selectbox(
            label="Select the Event", options=match_data["event"].drop_duplicates().sort_values()
        )

    with column2:
        red_alliance = st.multiselect(
            label="Select the Red Alliance teams",
            options=match_data[match_data["event"] == event]["team_number"]
            .drop_duplicates()
            .sort_values(),
            max_selections=3,
        )
    with column3:
        blue_alliance = st.multiselect(
            label="Select the Blue Alliance teams",
            options=match_data[match_data["event"] == event]["team_number"]
            .drop_duplicates()
            .sort_values(),
            max_selections=3,
        )

    is_red_alliance_filled: bool = red_alliance and len(red_alliance) == 3
    is_blue_alliance_filled: bool = blue_alliance and len(blue_alliance) == 3

    if not event or not is_red_alliance_filled or not is_blue_alliance_filled:
        st.write(
            "Please select an event, three teams for the Red Alliance, and three teams for the Blue Alliance."
        )
    else:
        ########################################################################
        # Everything is assumed we have exactly three teams on each alliance
        # and an event selected. This block of code will not run otherwise.
        match_data = match_data[
            (match_data["event"] == event)
            & match_data["team_number"].isin(red_alliance + blue_alliance)
        ]

        red_alliance_matches: pd.DataFrame = match_data.copy()[
            match_data["team_number"].isin(red_alliance)
        ].sort_values(by=["team_number", "match_number"])

        blue_alliance_matches: pd.DataFrame = match_data.copy()[
            match_data["team_number"].isin(blue_alliance)
        ].sort_values(by=["team_number", "match_number"])

        stat_filters = [
            "match_number",
            "auto_high_cubes",
            "auto_high_cones",
            "auto_mid_cubes",
            "auto_mid_cones",
            "auto_hybrid_cubes",
            "auto_hybrid_cones",
            "teleop_high_cubes",
            "teleop_high_cones",
            "teleop_mid_cubes",
            "teleop_mid_cones",
            "teleop_hybrid_cubes",
            "teleop_hybrid_cones",
        ]

        renames = {
            "match_number": "Match Number",
            "auto_high_cubes": "A High Cubes",
            "auto_high_cones": "A High Cones",
            "auto_mid_cubes": "A Mid Cubes",
            "auto_mid_cones": "A Mid Cones",
            "auto_hybrid_cubes": "A Hybrid Cubes",
            "auto_hybrid_cones": "A Hybrid Cones",
            "teleop_high_cubes": "T High Cubes",
            "teleop_high_cones": "T High Cones",
            "teleop_mid_cubes": "T Mid Cubes",
            "teleop_mid_cones": "T Mid Cones",
            "teleop_hybrid_cubes": "T Hybrid Cubes",
            "teleop_hybrid_cones": "T Hybrid Cones",
        }

        score_mapping = {
            'A High Cubes': 6,
            'A High Cones': 6,       
            'T High Cubes': 5,
            'T High Cones': 5,
            'A Mid Cubes':4,
            'A Mid Cones':4,
            'T Mid Cubes':3,
            'T Mid Cones':3,
            'A Hybrid Cubes':3,
            'A Hybrid Cones':3,
            'T Hybrid Cubes':2,
            'T Hybrid Cones':2,
        }

        st.header("Red Alliance Stats", divider=True)
        for team_number in red_alliance_matches["team_number"].sort_values().unique():
            st.subheader("Analysis for Team: " + str(team_number))
            filtered_data: pd.DataFrame = red_alliance_matches[
                red_alliance_matches["team_number"] == team_number
            ]

            filtered_data = filtered_data[stat_filters].rename(columns=renames).set_index("Match Number")

            column1, column2 = st.columns(2)

            with column1:
                st.dataframe(filtered_data)
            with column2:
                st.bar_chart(data=filtered_data)

        st.header("Blue Alliance Stats", divider=True)
        for team_number in blue_alliance_matches["team_number"].sort_values().unique():
            st.subheader("Analysis for Team: " + str(team_number))
            filtered_data: pd.DataFrame = blue_alliance_matches[
                blue_alliance_matches["team_number"] == team_number
            ]

            filtered_data = filtered_data[stat_filters].rename(columns=renames).set_index("Match Number")

            for key, value in score_mapping.items():
                filtered_data[key] *= value

            column1, column2 = st.columns(2)

            with column1:
                st.dataframe(filtered_data)
            with column2:
                st.bar_chart(data=filtered_data)
        

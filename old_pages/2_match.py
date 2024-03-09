from typing import Dict, List, TypeVar
import numpy as np
import pandas as pd
import streamlit as st

from old_pages.data_pull import read_match_scouting_data

from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import ExcelExportMode


def filter_by_event(match_data: pd.DataFrame) -> pd.DataFrame:
    """
    Handle filtering match data by Event name
    """
    event_choice: str = st.selectbox(
        label="Select which event you want to analyze",
        options=match_data["event"].drop_duplicates(),
        index=None,
    )

    event_filtered_data: pd.DataFrame = match_data.copy()
    if event_choice:
        event_filtered_data = match_data[match_data["event"] == event_choice]

    st.session_state.event_filtered = bool(event_choice)

    return event_filtered_data


def filter_by_team_number(match_data: pd.DataFrame) -> pd.DataFrame:
    """
    Handle filtering match data by Team Number
    """
    team_number_choice: str = st.selectbox(
        label="Select which team number you want to analyze",
        options=match_data["team_number"].drop_duplicates().astype(int).sort_values().astype(str),
        index=None,
        # index=team_starting_index
    )

    team_filtered_data: pd.DataFrame = match_data.copy()
    if team_number_choice:
        team_filtered_data = team_filtered_data[
            team_filtered_data["team_number"] == team_number_choice
        ]

    st.session_state.team_filtered = bool(team_number_choice)

    return team_filtered_data


def filter_by_match_number(match_data: pd.DataFrame) -> pd.DataFrame:
    """
    Handle filtering match data by Match Number
    """
    match_selection: List[TypeVar] = st.multiselect(
        label="Select which matches you want to filter",
        options=match_data["match_number"].drop_duplicates().astype(int).sort_values().astype(str),
    )

    match_filtered_data: pd.DataFrame = match_data.copy()
    if match_selection:
        # st.query_params["match"] = match_selection
        match_filtered_data = match_filtered_data[
            match_filtered_data["match_number"].isin(match_selection)
        ]

    st.session_state.match_filtered = bool(match_selection)

    return match_filtered_data


if __name__ == "__main__":
    st.set_page_config(
        page_title="Match Analytics",
        layout="wide",
    )

    if "event_filtered" not in st.session_state:
        st.session_state.event_filtered = False

    if "team_filtered" not in st.session_state:
        st.session_state.team_filtered = False

    if "match_filtered" not in st.session_state:
        st.session_state.match_filtered = False

    st.title("Match Analysis")
    st.write(
        "This page helps with analyzing match scoring by breaking down by event, then by robot, then by matches."
    )

    match_data = read_match_scouting_data()
    match_data["event"] = match_data["event"].astype(str)
    match_data["team_number"] = match_data["team_number"].astype(str)
    match_data["match_number"] = match_data["match_number"].astype(str)
    match_data = match_data.sort_values(
        by=["event", "match_number", "team_number", "timestamp"]
    ).reset_index(drop=True)

    ############################################################################
    # We want to eventually have the Query Parameters help drive sharable links
    # This is kept here for reference. Writing state to Query Params seems to
    # reset the shadow DOM sometimes, but might be able to be saved to state
    # variables instead.
    #
    # event_name = st.query_params.get("event", None)
    # team_number_param = st.query_params.get("team", None)
    # match_number_param = st.query_params.get("match", "").split(",")
    # team_starting_index: int = None
    # if available_team_numbers.isin([team_number_param]).any():
    #     team_starting_index = try_parse_int(available_team_numbers[available_team_numbers == team_number_param].index[0])

    column1, column2, column3 = st.columns(3)

    # match_filtered_data: pd.DataFrame = match_data.copy()

    ############################################################################
    # Event Selection
    with column1:
        match_data = filter_by_event(match_data=match_data)

    ############################################################################
    # Handle Team Filtering
    with column2:
        match_data = filter_by_team_number(match_data=match_data)

    ############################################################################
    # Handle Match Filtering
    with column3:
        match_data = filter_by_match_number(match_data=match_data)

    ############################################################################
    # Handles showing the raw data for downloads.
    st.header(
        "Match Data",
        anchor="match-data",
        help="You can download the full data by right-clicking and tapping 'Export'",
    )
    data_grid = GridOptionsBuilder.from_dataframe(match_data)
    data_grid.configure_pagination(enabled=True, paginationPageSize=10)
    data_grid.configure_default_column(groupable="true", filterable="true")
    data_grid.configure_grid_options(alwaysShowHorizontalScroll=True)
    data_grid.configure_side_bar(filters_panel=True)

    AgGrid(
        match_data,
        gridOptions=data_grid.build(),
        excel_export_mode=ExcelExportMode.MANUAL,
        allow_unsafe_jscode=True,
        custom_css={
            "#gridToolBar": {
                "padding-bottom": "0px !important",
            }
        },
    )

    if not st.session_state.event_filtered or not st.session_state.team_filtered:
        st.write(
            "To get more granular information about matches, "
            "please filter data with both an event and a team number."
        )
    else:
        mapped_data = match_data.copy()
        mapped_data["match_number"] = mapped_data["match_number"].astype(int)
        mapped_data = mapped_data.sort_values(by="match_number")
        mapped_data = mapped_data.reset_index(drop=True)

        column1, column2 = st.columns(2)

        ############################################################################
        # Render graphs for Cubes and Cones in Autonomous
        with column1:
            st.header("Cones in Autonomous")
            st.bar_chart(
                data=mapped_data[
                    [
                        "match_number",
                        "auto_high_cones",
                        "auto_mid_cones",
                        "auto_hybrid_cones",
                    ]
                ],
                x="match_number",
            )
            st.header("Cubes in Autonomous")
            st.bar_chart(
                data=mapped_data[
                    [
                        "match_number",
                        "auto_high_cubes",
                        "auto_mid_cubes",
                        "auto_hybrid_cubes",
                    ]
                ],
                x="match_number",
            )

        ############################################################################
        # Render graphs for Cubes and Cones in TeleOperated
        with column2:
            st.header("Cones in TeleOperated")
            st.bar_chart(
                data=mapped_data[
                    [
                        "match_number",
                        "teleop_high_cones",
                        "teleop_mid_cones",
                        "teleop_hybrid_cones",
                    ]
                ],
                x="match_number",
            )
            st.header("Cubes in TeleOperated")
            st.bar_chart(
                data=mapped_data[
                    [
                        "match_number",
                        "teleop_high_cubes",
                        "teleop_mid_cubes",
                        "teleop_hybrid_cubes",
                    ]
                ],
                x="match_number",
            )

        ############################################################################
        # Calculate the number of points in Autonomous
        mapped_auto_data = mapped_data.copy().rename(
            columns={"match_number": "Match Number", "field_position": "Field Position"}
        )
        mapped_auto_data["High Cubes"] = (mapped_auto_data["auto_high_cubes"] * 6).fillna(0)
        mapped_auto_data["High Cones"] = (mapped_auto_data["auto_high_cones"] * 6).fillna(0)
        mapped_auto_data["Mid Cubes"] = (mapped_auto_data["auto_mid_cubes"] * 4).fillna(0)
        mapped_auto_data["Mid Cones"] = (mapped_auto_data["auto_mid_cones"] * 4).fillna(0)
        mapped_auto_data["Hybrid Cubes"] = (mapped_auto_data["auto_hybrid_cubes"] * 3).fillna(0)
        mapped_auto_data["Hybrid Cones"] = (mapped_auto_data["auto_hybrid_cones"] * 3).fillna(0)
        mapped_auto_data["Balance"] = (mapped_auto_data["auto_balance"] * 12).fillna(0)
        mapped_auto_data["Docked"] = (mapped_auto_data["auto_dock"] * 8).fillna(0)
        mapped_auto_data["Mobility"] = (mapped_auto_data["auto_mobility"] * 3).fillna(0)

        mapped_auto_data["Auto Total"] = (
            mapped_auto_data["High Cubes"]
            + mapped_auto_data["High Cones"]
            + mapped_auto_data["Mid Cubes"]
            + mapped_auto_data["Mid Cones"]
            + mapped_auto_data["Hybrid Cubes"]
            + mapped_auto_data["Hybrid Cones"]
            + mapped_auto_data["Balance"]
            + mapped_auto_data["Docked"]
            + mapped_auto_data["Mobility"]
        )

        st.header("Autonomous Scoring Breakdown")
        st.dataframe(
            data=mapped_auto_data[
                [
                    "Match Number",
                    "Field Position",
                    "High Cubes",
                    "High Cones",
                    "Mid Cubes",
                    "Mid Cones",
                    "Hybrid Cubes",
                    "Hybrid Cones",
                    "Balance",
                    "Docked",
                    "Mobility",
                    "Auto Total",
                ]
            ].set_index("Match Number"),
            use_container_width=True,
        )

        st.bar_chart(
            data=mapped_auto_data[
                [
                    "Match Number",
                    "High Cubes",
                    "High Cones",
                    "Mid Cubes",
                    "Mid Cones",
                    "Hybrid Cubes",
                    "Hybrid Cones",
                    "Balance",
                    "Docked",
                    "Mobility",
                ]
            ].set_index("Match Number"),
        )

        ########################################################################
        # Calculate the number of points in Teleop
        st.header("TeleOperated Scoring Breakdown")

        mapped_teleop_data = mapped_data.copy().rename(
            columns={
                "match_number": "Match Number",
                "end_balance": "End Balance?",
                "end_dock": "End Dock?",
                "end_park": "End Park?",
            }
        )
        mapped_teleop_data["High Cubes"] = (mapped_teleop_data["teleop_high_cubes"] * 5).fillna(0)
        mapped_teleop_data["High Cones"] = (mapped_teleop_data["teleop_high_cones"] * 5).fillna(0)
        mapped_teleop_data["Mid Cubes"] = (mapped_teleop_data["teleop_mid_cubes"] * 3).fillna(0)
        mapped_teleop_data["Mid Cones"] = (mapped_teleop_data["teleop_mid_cones"] * 3).fillna(0)
        mapped_teleop_data["Hybrid Cubes"] = (mapped_teleop_data["teleop_hybrid_cubes"] * 2).fillna(
            0
        )
        mapped_teleop_data["Hybrid Cones"] = (mapped_teleop_data["teleop_hybrid_cones"] * 2).fillna(
            0
        )

        mapped_teleop_data["Teleop Total"] = (
            mapped_teleop_data["High Cubes"]
            + mapped_teleop_data["High Cones"]
            + mapped_teleop_data["Mid Cubes"]
            + mapped_teleop_data["Mid Cones"]
            + mapped_teleop_data["Hybrid Cubes"]
            + mapped_teleop_data["Hybrid Cones"]
        )

        mapped_teleop_data["Did Shuttle?"] = np.where(
            mapped_teleop_data["teleop_shuttle"].fillna(value=False), "Yes", "No"
        )
        mapped_teleop_data["Did Defend?"] = np.where(
            mapped_teleop_data["teleop_defend"].fillna(value=False), "Yes", "No"
        )

        st.dataframe(
            data=mapped_teleop_data[
                [
                    "Match Number",
                    "High Cubes",
                    "High Cones",
                    "Mid Cubes",
                    "Mid Cones",
                    "Hybrid Cubes",
                    "Hybrid Cones",
                    "Did Shuttle?",
                    "Did Defend?",
                ]
            ].set_index("Match Number"),
            use_container_width=True,
        )

        ########################################################################
        # Calculate the number of points in End Game
        mapped_end_data = mapped_data.copy().rename(
            columns={
                "match_number": "Match Number",
                "end_balance": "End Balance?",
                "end_dock": "End Dock?",
                "end_park": "End Park?",
            }
        )

        mapped_end_data["End Balance?"] = mapped_teleop_data["End Balance?"].fillna(value=False)
        mapped_end_data["End Dock?"] = mapped_teleop_data["End Dock?"].fillna(value=False)
        mapped_end_data["End Park?"] = mapped_teleop_data["End Park?"].fillna(value=False)

        mapped_end_data["End Balance Score"] = mapped_end_data["End Balance?"].astype(int) * 10
        mapped_end_data["End Dock Score"] = mapped_end_data["End Dock?"].astype(int) * 6
        mapped_end_data["End Park Score"] = mapped_end_data["End Balance?"].astype(int) * 2

        mapped_end_data["End Game Total"] = (
            mapped_end_data["End Balance Score"]
            + mapped_end_data["End Dock Score"]
            + mapped_end_data["End Park Score"]
        )

        column1, column2 = st.columns(2)

        with column1:
            st.header("End Game State")
            st.dataframe(
                data=mapped_end_data[
                    [
                        "Match Number",
                        "End Balance?",
                        "End Dock?",
                        "End Park?",
                    ]
                ].set_index("Match Number"),
                use_container_width=True,
            )

        with column2:
            st.header("End Game Values")
            st.dataframe(
                data=mapped_end_data[
                    [
                        "Match Number",
                        "End Balance Score",
                        "End Dock Score",
                        "End Park Score",
                    ]
                ].set_index("Match Number"),
                use_container_width=True,
            )
        st.header("End Game Scoring")

        final_calculations = mapped_auto_data[["Match Number", "Auto Total"]].merge(
            mapped_teleop_data[["Match Number", "Teleop Total"]], how="left", on="Match Number"
        )[["Match Number", "Auto Total", "Teleop Total"]]

        final_calculations = final_calculations.merge(
            mapped_end_data[["Match Number", "End Game Total"]], how="left", on="Match Number"
        )

        final_calculations["Total Score"] = (
            final_calculations["Auto Total"]
            + final_calculations["Teleop Total"]
            + final_calculations["End Game Total"]
        )

        st.dataframe(
            data=final_calculations[
                ["Match Number", "Auto Total", "Teleop Total", "End Game Total", "Total Score"]
            ].set_index("Match Number"),
            use_container_width=True,
        )

        st.bar_chart(
            data=final_calculations[
                ["Match Number", "Auto Total", "Teleop Total", "End Game Total"]
            ].set_index("Match Number"),
            use_container_width=True,
        )

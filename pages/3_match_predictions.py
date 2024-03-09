import pandas as pd
import streamlit as st

from typing import List

match_data: pd.DataFrame = pd.DataFrame()

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

from typing import List, TypeVar
import streamlit as st
import pandas as pd


from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import ExcelExportMode

from query_data import query_all_match_scouting_data, query_all_pit_scouting_data

st.set_page_config(
    page_title="Match Analytics",
    layout="wide",
)
st.title("Match Analytics")

column1, column2, column3 = st.columns(3)

event: str = ""
team_number: int = 0
match_selection: List[TypeVar] = []

match_data: pd.DataFrame = query_all_match_scouting_data().sort_values(by=['team.number', 'match.number'])

bulk_pit_data = match_data.copy()
bulk_pit_data['team.number'] = bulk_pit_data['team.number'].astype(str)

with column1:
    event = st.selectbox(
        label="Select Event",
        options=["Anderson"])
with column2:
    team_number = st.selectbox(
        label="Select Team Number",
        options=match_data['team.number'].unique()
    )
with column3:
    match_selection = st.multiselect(
            label="Select which matches you want to filter",
            options=match_data['match.number'],
        )

if team_number:
    match_data = match_data[match_data['team.number'] == team_number]

if match_selection:
    match_data = match_data[match_data['match.number'].isin(match_selection)]


# Teleop
match_data['subwoofer.attempted.teleop'] = match_data['subwoofer.attempted.teleop'].fillna(0)
match_data['subwoofer.completed.teleop'] = match_data['subwoofer.completed.teleop'].fillna(0)

match_data['amp.attempted.teleop'] = match_data['amp.attempted.teleop'].fillna(0)
match_data['amp.completed.teleop'] = match_data['amp.completed.teleop'].fillna(0)

match_data['podium.attempted.teleop'] = match_data['podium.attempted.teleop'].fillna(0)
match_data['podium.completed.teleop'] = match_data['podium.completed.teleop'].fillna(0)

match_data['medium.attempted.teleop'] = match_data['medium.attempted.teleop'].fillna(0)
match_data['medium.completed.teleop'] = match_data['medium.completed.teleop'].fillna(0)

match_data['midfield.attempted.teleop'] = match_data['midfield.attempted.teleop'].fillna(0)
match_data['midfield.completed.teleop'] = match_data['midfield.completed.teleop'].fillna(0)

# Auto
match_data['subwoofer.attempted.auto'] = match_data['subwoofer.attempted.auto'].fillna(0)
match_data['subwoofer.completed.auto'] = match_data['subwoofer.completed.auto'].fillna(0)

match_data['amp.attempted.auto'] = match_data['amp.attempted.auto'].fillna(0)
match_data['amp.completed.auto'] = match_data['amp.completed.auto'].fillna(0)

match_data['podium.attempted.auto'] = match_data['podium.attempted.auto'].fillna(0)
match_data['podium.completed.auto'] = match_data['podium.completed.auto'].fillna(0)

# match_data['medium.attempted.auto'] = match_data['medium.attempted.auto'].fillna(0)
# match_data['medium.completed.auto'] = match_data['medium.completed.auto'].fillna(0)

match_data['midfield.attempted.auto'] = match_data['midfield.attempted.auto'].fillna(0)
match_data['midfield.completed.auto'] = match_data['midfield.completed.auto'].fillna(0)


# Teleop averages
match_data['subwoofer.teleop.average'] = (
    (match_data['subwoofer.completed.teleop'])
    / (match_data['subwoofer.completed.teleop'] + match_data['subwoofer.attempted.teleop'])
).fillna(0)

match_data['amp.teleop.average'] = (
    (match_data['amp.completed.teleop'])
    / (match_data['amp.completed.teleop'] + match_data['amp.attempted.teleop'])
).fillna(0)

match_data['podium.teleop.average'] = (
    (match_data['podium.completed.teleop'])
    / (match_data['podium.completed.teleop'] + match_data['podium.attempted.teleop'])
).fillna(0)

match_data['medium.teleop.average'] = (
    (match_data['medium.completed.teleop'])
    / (match_data['medium.completed.teleop'] + match_data['medium.attempted.teleop'])
).fillna(0)

match_data['midfield.teleop.average'] = (
    (match_data['midfield.completed.teleop'])
    / (match_data['midfield.completed.teleop'] + match_data['midfield.attempted.teleop'])
).fillna(0)


# Auto averages
match_data['subwoofer.auto.average'] = (
    (match_data['subwoofer.completed.auto'])
    / (match_data['subwoofer.completed.auto'] + match_data['subwoofer.attempted.auto'])
).fillna(0)

match_data['amp.auto.average'] = (
    (match_data['amp.completed.auto'])
    / (match_data['amp.completed.auto'] + match_data['amp.attempted.auto'])
).fillna(0)

match_data['podium.auto.average'] = (
    (match_data['podium.completed.auto'])
    / (match_data['podium.completed.auto'] + match_data['podium.attempted.auto'])
).fillna(0)

# match_data['medium.auto.average'] = (
#     (match_data['medium.completed.auto'])
#     / (match_data['medium.completed.auto'] + match_data['medium.attempted.auto'])
# ).fillna(0)

match_data['midfield.auto.average'] = (
    (match_data['midfield.completed.auto'])
    / (match_data['midfield.completed.auto'] + match_data['midfield.attempted.auto'])
).fillna(0)

match_data = match_data.reset_index(drop=True)

st.header("Unedited Column Names")

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

st.header("Cleaned columns")

column_names_original = match_data.columns
column_names_pretty = {}
for key in match_data.columns:
    column_names_pretty[key] = ' '.join([word.capitalize() for word in key.split('.')])

match_data_pretty = match_data.rename(columns=column_names_pretty)

with st.expander("Autonomous", expanded=True):    
    for column in [
                "Amp Auto Average",
                "Subwoofer Auto Average",
                "Podium Auto Average",
                "Midfield Auto Average",
            ]:
        st.header(column)
        st.bar_chart(data=match_data_pretty[["Match Number", column]], x="Match Number")


with st.expander("Teleop", expanded=True):    
    for column in [
                "Amp Teleop Average",
                "Subwoofer Teleop Average",
                "Podium Teleop Average",
                "Medium Teleop Average",
                "Midfield Teleop Average",
            ]:
        st.subheader(column)
        st.bar_chart(data=match_data_pretty[["Match Number", column]], x="Match Number")

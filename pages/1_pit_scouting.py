from typing import List, TypeVar
import streamlit as st
import pandas as pd

from query_data import get_events_available, query_all_pit_scouting_data, query_pit_scouting_data_by_event

from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import ExcelExportMode

st.set_page_config(
    page_title="Match Analytics",
    layout="wide",
)
st.title("Pit Scouting Analysis")

event: str = ""
team_number: int = 0

pit_data: pd.DataFrame = query_all_pit_scouting_data().sort_values(by=['team.number'])


column1, column2 = st.columns(2)

with column1:
    event = st.selectbox(
        label="Select Event",
        options=get_events_available(),
        format_func=lambda x: x.capitalize(),
        )
with column2:
    team_number = st.selectbox(
        label="Select Team Number",
        options=pit_data['team.number'],
        index=None
    )

if event:
    pit_data = pit_data[pit_data['event'] == event]

if team_number:
    pit_data = pit_data[pit_data['team.number'] == team_number]

bulk_pit_data = pit_data.copy()
bulk_pit_data['team.number'] = bulk_pit_data['team.number'].astype(str)

st.header(
    "Pit Data",
    anchor="pit-data",
    help="You can download the full data by right-clicking and tapping 'Export'",
)
data_grid = GridOptionsBuilder.from_dataframe(pit_data)
data_grid.configure_pagination(enabled=True, paginationPageSize=10)
data_grid.configure_default_column(groupable="true", filterable="true")
data_grid.configure_grid_options(alwaysShowHorizontalScroll=True)
data_grid.configure_side_bar(filters_panel=True)

AgGrid(
    pit_data,
    gridOptions=data_grid.build(),
    excel_export_mode=ExcelExportMode.MANUAL,
    allow_unsafe_jscode=True,
    custom_css={
        "#gridToolBar": {
            "padding-bottom": "0px !important",
        }
    },
)


if len(pit_data) == 1:
    entry = pit_data.iloc[0]


    st.header("Physical Characteristics")

    st.subheader("General Stats")
    column1, column2, column3, column4, column5, = st.columns(5)

    with column1:
        st.metric("Robot Weight (lbs)", entry['robot.weight'])
    
    with column2:
        st.metric("Robot Travel Height (in)", entry['robot.travel.height'])
    
    with column3:
        st.metric("Robot Max Height (in)", entry['robot.max.height'])
    
    with column4:
        st.metric("Robot Width (in)", entry['robot.dimensions.width'])
    
    with column5:
        st.metric("Robot Length (in)", entry['robot.dimensions.length'])

    st.subheader("Battery")
    st.write(f"The team specified that they're using `{entry['robot.battery']}` batteries.")


    st.header("Driving cabilities")
    st.write(f"Team {entry['team.number']} uses a `{entry['robot.drive.train']}` drive train.")
    st.write(f"They specified that they use the following motors in their drive train:")
    for motor in entry['robot.drive.motors'].strip('[]').split(', '):
        st.write(f"- {motor}")

    if entry['robot.drive.train'] == "Swerve":
        st.write("The team specified that they are using the following swerve modules")
        st.write(f"- {entry['robot.drive.module']}")

    st.header("Mechanism Capabilities")
    st.write(f"They specified that they use the following motors in their subsystems:")
    for motor in entry['robot.mechanism.motors'].strip('[]').split(', '):
        st.write(f"- {motor}")

    st.write("For loading notes, they specified that they load with the following methods:")
    for intake in entry['robot.intake.method'].strip('[]').split(', '):
        st.write(f"- {intake}")

    st.write("When asked how they plan to climb, they said the following:")
    st.write(f"- {entry['robot.climbing.mechanism']}")

    st.write("When asked if they can go under the stage, they said:")
    st.write(f"- {entry['robot.under.stage']}")
    
    st.header("Software capabilities")
    st.subheader("Vision")
    st.write("The team specified that they are using the following softwares for Vision.")    
    for software in entry['robot.vision.software'].strip('[]').split(', '):
        software = software or "None"
        st.write(f"- {software}")
    st.write("With the following cameras specified:")
    for camera in entry['robot.vision.cameras'].strip('[]').split(', '):
        camera = camera or "None"
        st.write(f"- {camera}")
    
    st.subheader("Autonomous Software")
    st.write("The team specified that they use the following software for autonomous")
    for software in entry['robot.auto.software'].strip('[]').split(', '):
        software = software or "None"
        st.write(f"- {software}")
        
    st.header("Closing Remarks")
    st.write("Other comments left from the Pit Scouter are as follows:")
    last_notes = entry['other.notes'].strip() or "None"
    st.write(f"- {last_notes}")
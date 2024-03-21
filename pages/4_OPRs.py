from typing import List
import streamlit as st
import pandas as pd
import os

from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import ExcelExportMode

from query_data import load_tba_opr_data, load_tba_opr_options

event_options: List[str] = load_tba_opr_options()
event: str = ""

event = st.selectbox(
    label="Select the Event", options=event_options, index=None
)

if event:
    data = load_tba_opr_data(event=event)
    st.header("TBA COPRs")

    data_grid = GridOptionsBuilder.from_dataframe(data)
    data_grid.configure_pagination(enabled=True, paginationPageSize=10)
    data_grid.configure_default_column(groupable="true", filterable="true")
    data_grid.configure_grid_options(alwaysShowHorizontalScroll=True)
    data_grid.configure_side_bar(filters_panel=True)

    AgGrid(data,
        gridOptions=data_grid.build(),
        excel_export_mode=ExcelExportMode.MANUAL,
        allow_unsafe_jscode=True,
        custom_css={
            "#gridToolBar": {
                "padding-bottom": "0px !important",
            }
        },
    )
import os
import pandas as pd
import streamlit as st

from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode
from st_aggrid.shared import ExcelExportMode

from data_pull import read_match_scouting_data

if __name__ == "__main__":
    st.set_page_config(
        page_title="GarageScouter Analytics",
        layout="wide"
    )
    st.title("GarageScouter Analytics")
    data: pd.DataFrame = read_match_scouting_data()


    st.header("Raw Data", anchor="raw-data")
    st.dataframe(data=data)
    
    data_grid = GridOptionsBuilder.from_dataframe(data)
    data_grid.configure_pagination(enabled=True,paginationAutoPageSize=True)
    data_grid.configure_default_column(groupable="true",filterable="true")
    data_grid.configure_grid_options(alwaysShowHorizontalScroll=True)
    data_grid.configure_side_bar(filters_panel=True)

    AgGrid(data,
        gridOptions=data_grid.build(),
        # excel_export_mode=ExcelExportMode.MANUAL,
        # height=400,
        # allow_unsafe_jscode=True,
        # custom_css={ "#gridToolBar": { "padding-bottom": "0px !important", } }
    )



from typing import List
import streamlit as st
import pandas as pd
import os

from query_data import load_tba_opr_data, load_tba_opr_options

event_options: List[str] = load_tba_opr_options()
event: str = ""

event = st.selectbox(
    label="Select the Event", options=event_options, index=None
)

if event:
    st.dataframe(load_tba_opr_data(event=event))
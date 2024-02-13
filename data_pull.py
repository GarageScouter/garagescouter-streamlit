import os

import pandas as pd
import streamlit as st

# @st.cache_data
def read_pit_scouting_data() -> pd.DataFrame:
    return read_data(os.path.join("data", "pit"))

# @st.cache_data
def read_match_scouting_data() -> pd.DataFrame:
    return read_data(os.path.join("data", "match"))

# @st.cache_data
def read_super_scouting_data() -> pd.DataFrame:
    return read_data(os.path.join("data", "super"))

def read_data(folder_path: str) -> pd.DataFrame:
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
    dataframe = None

    for file in csv_files:
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)
        df['source'] = os.path.basename(file_path)
        dataframe = pd.concat([dataframe, df])

    return pd.concat([dataframe])
import os
from typing import List
import pandas as pd

def query_pit_scouting_data_by_event(event: str) -> pd.DataFrame:
    path: str = os.path.join("data", event, "raw", "pit")
    
    csv_files = [file for file in os.listdir(path) if file.endswith('.csv')]
    dataframe = None

    for file in csv_files:
        file_path = os.path.join(path, file)
        df = pd.read_csv(file_path)
        df['source'] = os.path.basename(file_path)
        df['event'] = event
        dataframe = pd.concat([dataframe, df])

    return pd.concat([dataframe])

def get_events_available() -> List[str]:
    return os.listdir("data")

def query_all_pit_scouting_data() -> pd.DataFrame:
    dataframe = None
    for event in os.listdir("data"):
        dataframe = pd.concat([dataframe, query_pit_scouting_data_by_event(event=event)])
    return dataframe


def query_match_scouting_data_by_event(event: str) -> pd.DataFrame:
    path: str = os.path.join("data", event, "raw", "match")
    
    csv_files = [file for file in os.listdir(path) if file.endswith('.csv')]
    dataframe = None

    for file in csv_files:
        file_path = os.path.join(path, file)
        df = pd.read_csv(file_path)
        df['source'] = os.path.basename(file_path)
        df['event'] = event
        dataframe = pd.concat([dataframe, df])

    return pd.concat([dataframe])

def query_all_match_scouting_data() -> pd.DataFrame:
    dataframe = None
    for event in os.listdir("data"):
        dataframe = pd.concat([dataframe, query_match_scouting_data_by_event(event=event)])
    return dataframe
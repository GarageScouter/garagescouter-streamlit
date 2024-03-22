import os
from typing import List
import pandas as pd
import json

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
        event_data = query_match_scouting_data_by_event(event=event)
        event_data["event"] = event
        dataframe = pd.concat([dataframe, event_data])
    return dataframe


def load_tba_opr_options() -> List[str]:
    return [file.removesuffix(".json").capitalize() for file in os.listdir(os.path.join("tba_oprs"))]


def load_tba_opr_data(event: str) -> pd.DataFrame:
    path: str = os.path.join("tba_oprs", f"{event.lower()}.json")

    if not os.path.exists(path):
        raise Exception("Path does not exist for that event.")
    
    # Read initial data (the way TBA formatted it)
    data: dict = {}
    with open(path, 'r') as file:
        data = json.load(file)

    # Re-organize the Dictionary to have the team number as the key
    flattened_data: dict = {}
    for key, values in data.items():
        for value in values:
            if not flattened_data.get(key, None):
                flattened_data[key] = {}
            flattened_data[key][value[0]] = value[1]

    df = pd.DataFrame(flattened_data)
    
    # The Team Number is the index, we want it explicitly labelled.
    df["Team Number"] = df.index

    # Make the Team Number the first column in the DF
    df = df[["Team Number", *df.columns.difference(["Team Number"])]]
    
    # Numerically sort by Team Number
    df["Team Number"] = df["Team Number"].astype(int)
    df = df.sort_values(by=["Team Number"]).reset_index(drop=True)
    df["Team Number"] = df["Team Number"].astype(str)
    
    return df
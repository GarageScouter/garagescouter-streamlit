# OpenScouter Analysis Tool
This repository serves as an Analysis portal to help teams find information about teams given the context of the data
collected by GarageScouter.

## How to run locally
You may not always have internet access available. So, in order to run offline with locally hosted data, 
you can clone this repository and follow the following steps.

1. Create virtual environment
  - If using Conda
    `conda create --name garagescouter python=3.11`
  - If using VirtualEnv
    `python -m venv venv`
2. Activate virtual environment
  - If using Conda
    `conda activate garagescouter`
  - If using VirtualEnv, follow your Operating System's requirements
3. Install dependencies
  - `pip install -r requirements.txt`
4. Run the development server for StreamLit
  - If using VSCode, use the built-in runner
  - Otherwise, run from the Shell with `streamlit run main.py`

## How to run the ETL process for Filtered Data

## How to contribute data
1. Fork this repository on GitHub
2. Upload data to your own fork of the code (we only use CSVs for flat files)
3. Make a PR

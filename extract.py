import pandas as pd

def load_data(file_path):
    """
    Loads the CSO, sewage pump station (SPS), and rainfall (RG_A) data.

    Parameters:
    - file_path: Path to the Excel file.

    Returns:
    - Dictionary of DataFrames.
    """
    cso = pd.read_excel(file_path, sheet_name='CSO_A')
    sps_a1 = pd.read_excel(file_path, sheet_name='SPS_A1')
    sps_a2 = pd.read_excel(file_path, sheet_name='SPS_A2')
    rainfall = pd.read_excel(file_path, sheet_name='RG_A')

    return {
        'cso': cso,
        'sps_a1': sps_a1,
        'sps_a2': sps_a2,
        'rainfall': rainfall
    }

def preview_dataframes(data_dict):
    """
    Prints the first few rows and shape of each dataset.
    """
    for name, df in data_dict.items():
        print(f"\n{name.upper()} — Shape: {df.shape}")
        print(df.head())

preview_dataframes(load_data('data/DataChallengeData2025.xlsx'))
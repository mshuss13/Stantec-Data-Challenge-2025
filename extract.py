import pandas as pd

def load_data(file_path):
    """
    Loads the CSO, sewage pump station (SPS), and rainfall (RG_A) data.

    Parameters:
    - file_path: Path to the Excel file.

    Returns:
    - Tuple of (cso_df, sps_a1_df, sps_a2_df, rainfall_df)
    """
    cso_df = pd.read_excel(file_path, sheet_name='CSO_A')
    sps_a1_df = pd.read_excel(file_path, sheet_name='SPS_A1')
    sps_a2_df = pd.read_excel(file_path, sheet_name='SPS_A2')
    rainfall_df = pd.read_excel(file_path, sheet_name='RG_A')

    return cso_df, sps_a1_df, sps_a2_df, rainfall_df
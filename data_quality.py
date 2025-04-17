import pandas as pd

def check_missing_values(df):
    """
    Check for missing values in the dataset.
    
    :param df: pandas DataFrame
    :return: DataFrame containing missing value counts and percentages
    """
    missing = df.isnull().sum()
    missing_percentage = (missing / len(df)) * 100
    return pd.DataFrame({
        'Missing Values': missing,
        'Percentage': missing_percentage
    })

def check_duplicates(df):
    """
    Check for duplicate records in the dataset.
    
    :param df: pandas DataFrame
    :return: Dictionary containing duplicate statistics
    """
    # Find duplicates based on entire row
    duplicates = df.duplicated(keep='first')
    
    # Get duplicate records
    duplicate_records = df[duplicates]
    
    # Count duplicates
    duplicate_count = len(duplicate_records)
    duplicate_percentage = (duplicate_count / len(df)) * 100
    
    return {
        'duplicate_count': duplicate_count,
        'duplicate_percentage': duplicate_percentage,
        'duplicate_records': duplicate_records
    }

def check_variable_ranges(df, column_ranges):
    """
    Check if values in specified columns fall within expected ranges.
    
    :param df: pandas DataFrame
    :param column_ranges: Dictionary mapping column names to their expected (min, max) range
                         Format: {'column_name': (min_value, max_value)}
    :return: Dictionary containing range check results
    """
    results = {}
    
    for column, (min_val, max_val) in column_ranges.items():
        # Check if columns exist in the df
        if column not in df.columns:
            results[column] = {
                'status': 'error',
                'message': f'Column {column} not found in DataFrame'
            }
            continue
        
        # Count values outside range
        values_below_min = len(df[df[column] < min_val])
        values_above_max = len(df[df[column] > max_val])
        
        if values_below_min > 0 or values_above_max > 0:
            results[column] = {
                'status': 'warning',
                'message': f'Values outside range [{min_val}, {max_val}] found',
                'below_min_count': values_below_min,
                'above_max_count': values_above_max
            }
        else:
            results[column] = {
                'status': 'ok',
                'message': 'All values are within expected range'
            }
    
    return results

def analyse_temporal_coverage(df, datetime_col):
    """
    Analyse temporal coverage of the dataset.
    
    :param df: pandas DataFrame containing the data
    :param datetime_col: Name of the column containing datetime values
    :return: Dictionary containing temporal coverage statistics
    """
    try:
        df[datetime_col] = pd.to_datetime(df[datetime_col]) # Standardise all dates into a consistent datetime format
    except Exception as e:
        raise ValueError(f"Error converting {datetime_col} to datetime format. Error: {str(e)}") # Raise error if a date cannot be parsed
    
    # Get the date range
    start_date = df[datetime_col].min()
    end_date = df[datetime_col].max()

    # The number of days between start and end dates (inclusive)
    total_days = (end_date - start_date).days + 1
    
    # Create a complete date range
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Get all dates in the data (including duplicates)
    all_dates = df[datetime_col].dt.date
    
    # Get unique dates to identify missing dates
    unique_days = all_dates.unique()
    
    # Count missing dates
    missing_dates = len(date_range) - len(unique_days)
    
    return {
        'Start Date': start_date,
        'End Date': end_date,
        'Total Days': total_days,
        'Total Entries': len(all_dates),
        'Unique Days': len(unique_days),
        'Missing Dates': missing_dates
    }

def check_sps_status_consistency(df):
    """
    Check if Status and StateDesc columns are consistent in SPS data.
    Status 1 should correspond to 'RUNNING' and Status 0 to 'STOPPED'.
    
    :param df: pandas DataFrame containing SPS data
    :return: Dictionary containing consistency check results
    """
    # Check for inconsistent records
    running_inconsistent = (df['Status'] == 1) & (df['StateDesc'] != 'RUNNING')
    stopped_inconsistent = (df['Status'] == 0) & (df['StateDesc'] != 'STOPPED')
    
    # Get inconsistent records
    inconsistent_records = df[running_inconsistent | stopped_inconsistent]
    inconsistent_count = len(inconsistent_records)
    
    if inconsistent_count > 0:
        return {
            'status': 'warning',
            'message': f'Found {inconsistent_count} records where Status and StateDesc are inconsistent',
            'inconsistent_count': inconsistent_count,
            'inconsistent_records': inconsistent_records
        }
    else:
        return {
            'status': 'ok',
            'message': 'Status and StateDesc columns are consistent'
        }

def analyse_cso_data(cso_df):
    """
    Analyse CSO data quality.
    
    :param cso_df: pandas DataFrame containing CSO data
    :return: Dictionary containing various analysis results
    """
    # Check missing values and data types
    missing_values = check_missing_values(cso_df)
    
    # Check for duplicates
    duplicates = check_duplicates(cso_df)
    
    # Check for outliers
    Q1 = cso_df['Level'].quantile(0.25)
    Q3 = cso_df['Level'].quantile(0.75)
    IQR = Q3 - Q1
    outliers = cso_df[(cso_df['Level'] < (Q1 - 1.5 * IQR)) | (cso_df['Level'] > (Q3 + 1.5 * IQR))] # Needed to use bitwise or
    
    # Check variable ranges
    level_ranges = check_variable_ranges(cso_df, {'Level': (0, 100)}) # Assuming level should be between 0 and 100m
    
    # Analyse temporal coverage
    temporal = analyse_temporal_coverage(cso_df, 'DateTime')
    
    return {
        'missing_values': missing_values,
        'duplicates': duplicates,
        'outlier_count': len(outliers),
        'outlier_percentage': (len(outliers) / len(cso_df)) * 100,
        'variable_ranges': level_ranges,
        'temporal_coverage': temporal
    }

def analyse_sps_data(sps_df, dataset_name):
    """
    Analyse SPS data quality.
    
    :param sps_df: pandas DataFrame containing SPS data
    :param dataset_name: Name of the SPS dataset (e.g., 'SPS_A1' or 'SPS_A2')
    :return: Dictionary containing various analysis results
    """
    # Check missing values and data types
    missing_values = check_missing_values(sps_df)
    
    # Check for duplicates
    duplicates = check_duplicates(sps_df)
    
    # Check status consistency
    status_consistency = check_sps_status_consistency(sps_df)
    
    # Analyse status changes
    status_changes = sps_df.groupby('Site')['Status'].value_counts()
    
    # Check variable ranges
    status_ranges = check_variable_ranges(sps_df, {'Status': (0, 1), 'StateDesc': ('RUNNING', 'STOPPED')})
    
    # Standardise datetime
    sps_df['Timestamp'] = pd.to_datetime(sps_df['Timestamp'])
    
    # Analyse temporal coverage
    temporal = analyse_temporal_coverage(sps_df, 'Timestamp')
    
    return {
        'missing_values': missing_values,
        'duplicates': duplicates,
        'status_consistency': status_consistency,
        'status_changes': status_changes,
        'variable_ranges': status_ranges,
        'temporal_coverage': temporal
    }

def analyse_rainfall_data(rainfall_df):
    """
    Analyse rainfall data quality.
    
    :param rainfall_df: pandas DataFrame containing rainfall data
    :return: Dictionary containing various analysis results
    """
    # Check missing values and data types
    missing_values = check_missing_values(rainfall_df)
    
    # Check for duplicates
    duplicates = check_duplicates(rainfall_df)
    
    # Check for zero rainfall periods
    zero_rainfall = (rainfall_df['RG_A'] == 0).sum()
    zero_rainfall_pct = (zero_rainfall / len(rainfall_df)) * 100
    
    # Check variable ranges
    rainfall_ranges = check_variable_ranges(rainfall_df, {'RG_A': (0, 100)}) # Assuming rainfall should be between 0 and 100mm
    
    # Analyse temporal coverage
    temporal = analyse_temporal_coverage(rainfall_df, 'time')
    
    return {
        'missing_values': missing_values,
        'duplicates': duplicates,
        'zero_rainfall_count': zero_rainfall,
        'zero_rainfall_percentage': zero_rainfall_pct,
        'variable_ranges': rainfall_ranges,
        'temporal_coverage': temporal
    }

# TODO: MAKE THIS LESS UGLY. Too many return blocks :/
def detect_potential_false_spills(cso_df, sps_df, threshold=43.0, window_hours=6):
    """
    Detect potential false spill events in CSO data.
    
    A false spill event is defined as:
    1. CSO level exceeding the threshold
    2. Pump activation shortly after
    3. Level dropping without remaining high
    
    :param cso_df: DataFrame containing CSO level data
    :param sps_df: DataFrame containing pump status data
    :param threshold: Level threshold for spill events (in meters)
    :param window_hours: Time window to look for pump activation after level exceeds threshold
    :return: Dictionary containing detected false spill events
    """
    # Ensure datetime columns are properly formatted
    cso_df['DateTime'] = pd.to_datetime(cso_df['DateTime'])
    sps_df['Timestamp'] = pd.to_datetime(sps_df['Timestamp'])
    
    # Find periods where level exceeds threshold
    high_level_periods = cso_df[cso_df['Level'] >= threshold].copy()
    
    if high_level_periods.empty:
        return {
            'status': 'ok', # Used to differentiate between false spills and normal spills. ok = normal
            'message': 'No periods found where CSO level exceeds the threshold.',
            'false_spills': []
        }
    
    # Group into 1 hour periods, i.e, only 1 spill event per hour.
    high_level_periods['group'] = (high_level_periods['DateTime'].diff() > pd.Timedelta(hours=1)).cumsum()
    
    # For each spill event, check if pumps were activated shortly after
    potential_false_spills = []
    
    for _, period in high_level_periods.groupby('group'):
        start_time = period['DateTime'].min()
        end_time = period['DateTime'].max()
        
        # Look for pump activation within window_hours after a spill event
        pump_window_start = start_time
        pump_window_end = start_time + pd.Timedelta(hours=window_hours)
        
        # Check if any pumps were activated during this window
        pumps_activated = sps_df[(sps_df['Timestamp'] >= pump_window_start) & (sps_df['Timestamp'] <= pump_window_end) & (sps_df['Status'] == 1)]
        
        if not pumps_activated.empty:
            # Check if level dropped within 24 hours of pump activation
            level_after_pump = cso_df[(cso_df['DateTime'] > pump_window_end) & (cso_df['DateTime'] <= pump_window_end + pd.Timedelta(hours=24))]
            
            if not level_after_pump.empty and level_after_pump['Level'].max() < threshold:
                # This looks like a false spill - level exceeded threshold, pumps activated, level dropped
                potential_false_spills.append({
                    'start_time': start_time,
                    'end_time': end_time,
                    'max_level': period['Level'].max(),
                    'pump_activation_time': pumps_activated['Timestamp'].min()
                })
    
    if potential_false_spills:
        return {
            'status': 'warning', # warning = false spill
            'message': f'Found {len(potential_false_spills)} potential false spill events.',
            'false_spills': potential_false_spills
        }
    else:
        return {
            'status': 'ok',
            'message': 'No potential false spill events found.',
            'false_spills': []
        } 
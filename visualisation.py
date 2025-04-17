import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# OLD - PRENDING UPDATE/REMOVAL
def create_missing_values_table(analyses):
    """
    Create a formatted table of missing values across all datasets.
    
    :param analyses: Dictionary containing analysis results for each dataset
    :return: DataFrame containing the formatted table
    """
    # Create a list to store the data
    data = []
    
    # Add data for each dataset
    for dataset_name, analysis in analyses.items():
        total_missing = analysis['missing_values']['Missing Values'].sum()
        data.append({
            'Dataset': dataset_name,
            'Missing Values': total_missing
        })
    
    # Create DataFrame and format it
    df = pd.DataFrame(data)
    df = df.set_index('Dataset')
    
    # Save to CSV
    df.to_csv('output/tables/missing_values_summary.csv')
    
    return df

def plot_time_series(df, datetime_col, value_col, title, output_path):
    """
    Create a time series plot.
    
    :param df: pandas DataFrame containing the data
    :param datetime_col: Name of the column containing datetime values
    :param value_col: Name of the column containing values to plot
    :param title: Title for the plot
    :param output_path: Path where to save the plot
    """
    plt.figure(figsize=(15, 6))
    plt.plot(df[datetime_col], df[value_col])
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel(value_col)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_distribution(df, column, title, output_path):
    """
    Create a distribution plot.
    
    :param df: pandas DataFrame containing the data
    :param column: Name of the column to plot distribution for
    :param title: Title for the plot
    :param output_path: Path where to save the plot
    """
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x=column, bins=50)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_sps_status_distribution(df, title, output_path):
    """
    Create a bar plot showing status distribution by site for SPS data.
    
    :param df: pandas DataFrame containing SPS data
    :param title: Title for the plot
    :param output_path: Path where to save the plot
    """
    plt.figure(figsize=(10, 6))
    
    # Get status counts by site
    status_counts = df.groupby('Site')['Status'].value_counts().unstack()
    
    # Create bar plot
    status_counts.plot(kind='bar', width=0.8)
    
    plt.title(title)
    plt.xlabel('Site')
    plt.ylabel('Count')
    plt.legend(title='Status')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_temporal_coverage(temporal_stats, title, output_path):
    """
    Create a bar plot of temporal coverage statistics.
    
    :param temporal_stats: Dictionary containing temporal coverage statistics
    :param title: Title for the plot
    :param output_path: Path where to save the plot
    """
    plt.figure(figsize=(10, 6))
    
    # Prepare data for plotting
    stats = {
        'Total Days': temporal_stats['Total Days'],
        'Days with Data': temporal_stats['Unique Days'],
        'Missing Days': temporal_stats['Missing Dates']
    }
    
    # Create bar plot
    plt.bar(stats.keys(), stats.values(), color=['blue', 'green', 'red'])
    
    # Add value labels on top of bars
    for i, (key, value) in enumerate(stats.items()):
        plt.text(i, value, str(value), ha='center', va='bottom')
    
    plt.title(title)
    plt.ylabel('Number of Days')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

# Could not use in ppt, but interesting plot.
def plot_daily_counts(df, datetime_col, title, output_path):
    """
    Create a bar plot of daily entry counts.
    
    :param df: pandas DataFrame containing the data
    :param datetime_col: Name of the column containing datetime values
    :param title: Title for the plot
    :param output_path: Path where to save the plot
    """
    plt.figure(figsize=(15, 6))
    
    # Count entries per day
    daily_counts = df.groupby(df[datetime_col].dt.date).size()
    
    # Create bar plot
    plt.bar(daily_counts.index, daily_counts.values, alpha=0.7)
    
    # Add a line showing the mean count
    mean_count = daily_counts.mean()
    plt.axhline(y=mean_count, color='r', linestyle='--', label=f'Mean: {mean_count:.1f} entries/day')
    
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Number of Entries')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_spill_events(df, datetime_col, level_col, threshold, title, output_path):
    """
    Create a plot showing CSO spill events over time.
    
    :param df: pandas DataFrame containing the data
    :param datetime_col: Name of the column containing datetime values
    :param level_col: Name of the column containing level values
    :param threshold: Level threshold for spill events (in meters)
    :param title: Title for the plot
    :param output_path: Path where to save the plot
    """
    plt.figure(figsize=(15, 6))
    
    # Identify spill events
    spill_events = df[df[level_col] >= threshold].copy()
    
    # Create scatter plot of spill events
    plt.scatter(spill_events[datetime_col], spill_events[level_col], color='red', alpha=0.6, label='Spill Events')
    
    # Add threshold line
    plt.axhline(y=threshold, color='red', linestyle='--', label=f'Spill Threshold ({threshold}m)')
    
    # Add regular level data as background
    plt.plot(df[datetime_col], df[level_col], color='blue', alpha=0.3, label='CSO Level')
    
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Level (m)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    
    # Return spill event statistics
    return {
        'total_spills': len(spill_events),
        'spill_dates': spill_events[datetime_col].dt.date.nunique(),
        'max_level': spill_events[level_col].max(),
        'avg_level': spill_events[level_col].mean()
    }

def plot_missing_values_heatmap(df, title, output_path):
    """
    Create a heatmap visualisation of missing values in the dataset.
    
    :param df: pandas DataFrame containing the data
    :param title: Title for the plot
    :param output_path: Path where to save the plot
    """
    plt.figure(figsize=(12, 8))
    
    # Calculate missing values
    missing_data = df.isnull()
    
    # Create heatmap
    sns.heatmap(missing_data, cmap='YlOrRd', cbar_kws={'label': 'Missing Value'}, yticklabels=False) # Orange themed heatmap with no y-labels
    
    plt.title(f"{title} - Missing Values Heatmap", fontsize=14, pad=20)
    plt.xlabel('Columns', fontsize=12)
    plt.ylabel('Rows', fontsize=12)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    
    return {
        'missing_counts': df.isnull().sum().to_dict(),
        'missing_percentages': (df.isnull().sum() / len(df) * 100).to_dict()
    }

def plot_rainfall_cso_correlation(cso_df, rainfall_df, start_date, end_date, title, output_path):
    """
    Create a plot showing the correlation between rainfall and CSO levels over a specified time period.
    
    :param cso_df: pandas DataFrame containing CSO data
    :param rainfall_df: pandas DataFrame containing rainfall data
    :param start_date: Start date for the analysis period
    :param end_date: End date for the analysis period
    :param title: Title for the plot
    :param output_path: Path where to save the plot
    """
    # Create figure with two y-axes
    fig, ax1 = plt.subplots(figsize=(15, 8))
    ax2 = ax1.twinx()
    
    # Filter data for the specified time period. Series of True and False values known as a mask. Not necessary, but cleaner.
    cso_mask = (cso_df['DateTime'] >= start_date) & (cso_df['DateTime'] <= end_date)
    rainfall_mask = (rainfall_df['time'] >= start_date) & (rainfall_df['time'] <= end_date)
    
    # Take the dates with the correct masks
    cso_period = cso_df[cso_mask]
    rainfall_period = rainfall_df[rainfall_mask]
    
    # Plot CSO levels
    line1 = ax1.plot(cso_period['DateTime'], cso_period['Level'], color='blue', label='CSO Level', alpha=0.7)
    ax1.set_xlabel('Date', fontsize=12)
    ax1.set_ylabel('CSO Level (m)', color='blue', fontsize=12)
    ax1.tick_params(axis='y', labelcolor='blue')

    # Add threshold line at 43mm
    ax1.axhline(y=43.0, color='red', linestyle='--', label='Spill Threshold (43m)')
    
    # Plot rainfall
    line2 = ax2.plot(rainfall_period['time'], rainfall_period['RG_A'], color='red', label='Rainfall', alpha=0.7)
    ax2.set_ylabel('Rainfall (mm)', color='red', fontsize=12)
    ax2.tick_params(axis='y', labelcolor='red')
    
    # Add title and legend
    plt.title(title, fontsize=14, pad=20)
    
    # Combine legends
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left')
    
    # Format x-axis
    plt.xticks(rotation=45)
    
    # Add grid
    ax1.grid(True, alpha=0.3)
    
    # Adjust layout
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_sps_cso_correlation(cso_df, sps_df, start_date, end_date, title, output_path):
    """
    Create a plot showing the correlation between SPS (pump status) and CSO levels over a specified time period.
    
    :param cso_df: pandas DataFrame containing CSO level data
    :param sps_df: pandas DataFrame containing SPS pump status data
    :param start_date: Start date for the plot
    :param end_date: End date for the plot
    :param title: Plot title
    :param output_path: File path to save the output image
    """
    # Create figure and axis
    fig, ax1 = plt.subplots(figsize=(15, 8))
    ax2 = ax1.twinx()

    # Filter for the given time window
    cso_period = cso_df[(cso_df['DateTime'] >= start_date) & (cso_df['DateTime'] <= end_date)].copy()
    sps_period = sps_df[(sps_df['Timestamp'] >= start_date) & (sps_df['Timestamp'] <= end_date)].copy()

    # Add threshold line at 43mm
    ax1.axhline(y=43.0, color='red', linestyle='--', label='Spill Threshold (43m)')

    # Plot CSO levels
    line1 = ax1.plot(cso_period['DateTime'], cso_period['Level'], label='CSO Level', color='blue')
    ax1.set_ylabel('CSO Level (m)', color='blue', fontsize=12)
    ax1.tick_params(axis='y', labelcolor='blue') # Match axis label to line colour :)

    # Plot pump activations
    running_pumps = sps_period[sps_period['Status'] == 1].copy()
    # Match each pump activation to nearest CSO level for y-position
    running_pumps = pd.merge_asof(
        running_pumps.sort_values('Timestamp'),
        cso_period[['DateTime', 'Level']].sort_values('DateTime'),
        left_on='Timestamp',
        right_on='DateTime',
        direction='nearest'
    )
    scatter = ax2.scatter(
        running_pumps['Timestamp'],
        running_pumps['Level'],
        marker='^',
        color='green',
        s=60,
        label='Pump Activation'
    )
    ax2.set_ylabel('Pump Activation (Markers)', color='green', fontsize=12)
    ax2.tick_params(axis='y', labelcolor='green')

    # Format and title
    ax1.set_xlabel("Date")
    plt.title(title, fontsize=14, pad=20)

    # Combine legend items
    lines = line1 + [scatter]
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left')

    plt.xticks(rotation=45)
    ax1.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_duplicates(df, title, output_path):
    """
    Create a simple visualisation of duplicates in the dataset.
    
    :param df: pandas DataFrame containing the data
    :param title: Title for the plot
    :param output_path: Path where to save the plot
    """
    plt.figure(figsize=(10, 6))
    
    # Find duplicates based on entire row
    duplicates = df.duplicated(keep='first')
    duplicate_records = df[duplicates]
    duplicate_count = len(duplicate_records)
    total_count = len(df)
    
    # Create a simple bar chart
    plt.bar(['Duplicates', 'Unique'], [duplicate_count, total_count - duplicate_count], color=['red', 'green'])
    
    # Add count labels on top of bars
    plt.text(0, duplicate_count, f"{duplicate_count:,}", ha='center', va='bottom')
    plt.text(1, total_count - duplicate_count, f"{total_count - duplicate_count:,}", ha='center', va='bottom')
    
    # Add percentage labels
    duplicate_percentage = (duplicate_count / total_count) * 100
    if duplicate_count > 0:  # Only show percentage label for duplicates if there are any. 
        plt.text(0, duplicate_count/2, f"{duplicate_percentage:.2f}%", ha='center', va='center', color='white') # Show % in the center of the bar.
    plt.text(1, (total_count - duplicate_count)/2, f"{100-duplicate_percentage:.2f}%", ha='center', va='center', color='white') # Show exact number above bar plot. Stole this but it's cool.
    
    plt.title(f"{title} - Duplicates", fontsize=14, pad=20)
    plt.ylabel('Number of Records', fontsize=12)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    
    return {
        'duplicate_count': duplicate_count,
        'unique_count': total_count - duplicate_count,
        'duplicate_percentage': duplicate_percentage
    }

def plot_sps_status_consistency(df, title, output_path):
    """
    Create a heatmap showing the distribution of Status-StateDesc combinations.
    This helps identify any inconsistencies between Status and StateDesc values.
    
    :param df: pandas DataFrame containing SPS data
    :param title: Title for the plot
    :param output_path: Path where to save the plot
    """
    plt.figure(figsize=(8, 6))
    
    # Create cross-tabulation of Status and StateDesc
    status_matrix = pd.crosstab(df['Status'], df['StateDesc'])
    
    # Create heatmap
    sns.heatmap(status_matrix, annot=True, fmt='d', cmap='YlOrRd') # did not turn out orange because values ended up lying on far ends :(
    
    plt.title(f"{title} - Status vs StateDesc Distribution")
    plt.xlabel('State Description')
    plt.ylabel('Status')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    
    # Return inconsistency count if any
    expected_combinations = {(1, 'RUNNING'), (0, 'STOPPED')}
    actual_combinations = set((status, state) for status, state in zip(df['Status'], df['StateDesc']))
    inconsistent_combinations = actual_combinations - expected_combinations
    
    return {
        'inconsistent_combinations': list(inconsistent_combinations),
        'inconsistent_count': len(df[~((df['Status'] == 1) & (df['StateDesc'] == 'RUNNING')) & 
                                    ~((df['Status'] == 0) & (df['StateDesc'] == 'STOPPED'))])
    }

def plot_potential_false_spills(cso_df, sps_df, false_spills, threshold=43.0, title="Potential False Spill Events", output_path="output/figures/potential_false_spills.png"):
    """
    Create a visualisation to show potential false spill events.
    
    :param cso_df: DataFrame containing CSO level data
    :param sps_df: DataFrame containing pump status data
    :param false_spills: List of dictionaries containing false spill event details
    :param threshold: Level threshold for spill events (in meters)
    :param title: Title for the plot
    :param output_path: Path where to save the plot
    """
    # Ensure datetime columns are properly formatted
    cso_df['DateTime'] = pd.to_datetime(cso_df['DateTime'])
    sps_df['Timestamp'] = pd.to_datetime(sps_df['Timestamp'])

    # Define the zoomed-in window. Picked a timeframe of 20 days.
    start_date = '2017-11-01'
    end_date = '2017-11-20'

    # Filter both CSO and pump data
    cso_zoom = cso_df[(cso_df['DateTime'] >= start_date) & (cso_df['DateTime'] <= end_date)].copy()
    sps_zoom = sps_df[(sps_df['Timestamp'] >= start_date) & (sps_df['Timestamp'] <= end_date)].copy()

    # Create visualisation
    plt.figure(figsize=(14, 6))

    # Plot CSO level
    level_line, = plt.plot(cso_zoom['DateTime'], cso_zoom['Level'], color='blue', label='CSO Level')

    # Threshold line
    threshold_line = plt.axhline(y=threshold, color='red', linestyle='--', label='Spill Threshold')

    # Pump activations at correct CSO levels
    pump_activations = sps_zoom[sps_zoom['Status'] == 1].copy()
    pump_activations['DateTime'] = pd.to_datetime(pump_activations['Timestamp'])

    # Match to nearest CSO level for correct y-values
    pump_activations = pd.merge_asof(
        pump_activations.sort_values('DateTime'),
        cso_zoom[['DateTime', 'Level']].sort_values('DateTime'),
        on='DateTime',
        direction='nearest'
    )

    # Plot pumps
    pump_markers = plt.scatter(
        pump_activations['DateTime'],
        pump_activations['Level'],
        marker='^', color='green', s=80, label='Pump Activated'
    )

    # Create plot
    plt.title(f"Zoomed-In View: CSO Level & Pump Activation ({start_date} to {end_date})")
    plt.xlabel("Date")
    plt.ylabel("CSO Level")
    plt.legend(handles=[level_line, threshold_line, pump_markers], loc='upper left')
    plt.tight_layout()
    plt.savefig("output/figures/zoomed_false_spill.png")
    plt.close()

    return {
        'count': len(false_spills)
    } 
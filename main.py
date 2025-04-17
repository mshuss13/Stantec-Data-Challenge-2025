from pathlib import Path
from extract import *
from data_quality import *
from visualisation import *
import pandas as pd

# TODO: CREATE APPROPRIATE CSV FILES RATHER THAN PRINTING. Target location: output/tables
def main():
    print("\n" + "="*80)
    print("DATA QUALITY REPORT")
    print("="*80)
    
    for dataset_name, analysis in analyses.items():
        print(f"\n{dataset_name} DATA QUALITY")
        print("-"*40)
        
        # Missing values
        print("\nMISSING VALUES:")
        print(analysis['missing_values'])
        
        # Duplicates
        duplicates = analysis.get('duplicates', {})
        if duplicates:
            print(f"\nDUPLICATES: {duplicates['duplicate_count']:,} records ({duplicates['duplicate_percentage']:.2f}%)")
        
        # Variable ranges
        ranges = analysis.get('variable_ranges', {})
        if ranges:
            print("\nVARIABLE RANGES:")
            for column, result in ranges.items():
                print(f"{column}: {result['message']}")
                if result['status'] == 'warning':
                    if 'unexpected_values' in result:
                        print(f"Unexpected values: {result['unexpected_values']}")
                    if 'below_min_count' in result:
                        print(f"Values below min: {result['below_min_count']}")
                        print(f"Values above max: {result['above_max_count']}")
        
        # Dataset-specific checks
        if dataset_name == 'CSO':
            print(f"\nOUTLIERS: {analysis['outlier_count']:,} records ({analysis['outlier_percentage']:.2f}%)")
        
        elif dataset_name.startswith('SPS'):
            print("\nSTATUS CHANGES:")
            print(analysis['status_changes'])
        
        elif dataset_name == 'Rainfall':
            print(f"\nZERO RAINFALL: {analysis['zero_rainfall_count']:,} records ({analysis['zero_rainfall_percentage']:.2f}%)")
        
        # Temporal coverage
        temporal = analysis.get('temporal_coverage', {})
        if temporal:
            print("\nTEMPORAL COVERAGE:")
            print(f"  Start Date: {temporal['Start Date']}")
            print(f"  End Date: {temporal['End Date']}")
            print(f"  Total Days: {temporal['Total Days']}")
            print(f"  Days with Data: {temporal['Unique Days']}")
            print(f"  Missing Days: {temporal['Missing Dates']}")
    
    print("\n" + "="*80)

    # Create output directories
    Path('output/figures').mkdir(parents=True, exist_ok=True)
    Path('output/tables').mkdir(parents=True, exist_ok=True)
    
    # Load data
    print("Loading data...")
    cso_df, sps_a1_df, sps_a2_df, rainfall_df = load_data("data/DataChallengeData2025.xlsx")
    
    # Analyse CSO data
    print("\nAnalyzing CSO data...")
    cso_analysis = analyse_cso_data(cso_df)
    
    # Analyse SPS data
    print("Analyzing SPS_A1 data...")
    sps_a1_analysis = analyse_sps_data(sps_a1_df, 'SPS_A1')
    print("Analyzing SPS_A2 data...")
    sps_a2_analysis = analyse_sps_data(sps_a2_df, 'SPS_A2')
    
    # Analyse rainfall data
    print("Analyzing rainfall data...")
    rainfall_analysis = analyse_rainfall_data(rainfall_df)
    
    # Create missing values summary table
    analyses = {
        'CSO': cso_analysis,
        'SPS_A1': sps_a1_analysis,
        'SPS_A2': sps_a2_analysis,
        'Rainfall': rainfall_analysis
    }
    missing_values_table = create_missing_values_table(analyses)
    
    # # Create data type distribution visualisations
    # print("\nGenerating data type distribution visualisations...")
    # plot_data_types_distribution(cso_df, 'CSO Data Types', 'output/figures/cso_data_types.png')
    # plot_data_types_distribution(sps_a1_df, 'SPS_A1 Data Types', 'output/figures/sps_a1_data_types.png')
    # plot_data_types_distribution(sps_a2_df, 'SPS_A2 Data Types', 'output/figures/sps_a2_data_types.png')
    # plot_data_types_distribution(rainfall_df, 'Rainfall Data Types', 'output/figures/rainfall_data_types.png')
    
    # Create SPS status consistency visualisations
    print("\nGenerating SPS status consistency visualisations...")
    plot_sps_status_consistency(sps_a1_df, 'SPS_A1', 'output/figures/sps_a1_status_consistency.png')
    plot_sps_status_consistency(sps_a2_df, 'SPS_A2', 'output/figures/sps_a2_status_consistency.png')
    
    # Create distribution plots for each dataset
    plot_distribution(cso_df, 'Level', 'CSO Level Distribution', 'output/figures/cso_level_distribution.png')
    plot_distribution(rainfall_df, 'RG_A', 'Rainfall Distribution', 'output/figures/rainfall_distribution.png')
    
    # Create SPS status distribution plots
    plot_sps_status_distribution(sps_a1_df, 'SPS_A1 Status Distribution by Site', 'output/figures/sps_a1_status_distribution.png')
    plot_sps_status_distribution(sps_a2_df, 'SPS_A2 Status Distribution by Site', 'output/figures/sps_a2_status_distribution.png')
    
    # Plot CSO spill events
    print("Analysing CSO Spill Events...")
    spill_stats = plot_spill_events(cso_df, 'DateTime', 'Level', 43.0,'CSO Spill Events (Level ≥ 43m)','output/figures/cso_spill_events.png')
    
    # Print spill statistics
    print("\nCSO Spill Event Statistics:")
    print(f"Total number of spill events: {spill_stats['total_spills']:,}")
    print(f"Number of days with spills: {spill_stats['spill_dates']:,}")
    print(f"Maximum level during spills: {spill_stats['max_level']:.2f}m")
    print(f"Average level during spills: {spill_stats['avg_level']:.2f}m")
    
    # Analyse potential false spill events
    print("\nAnalysing potential false spill events...")
    # Combine SPS data from both sites
    sps_combined = pd.concat([sps_a1_df, sps_a2_df])
    
    # Detect potential false spills
    false_spills_result = detect_potential_false_spills(cso_df, sps_combined, threshold=43.0, window_hours=6)
    
    # Create visualisation for potential false spills
    if false_spills_result['status'] == 'warning': # warning = false spill
        false_spills = false_spills_result['false_spills']
        plot_potential_false_spills(
            cso_df, sps_combined, false_spills, threshold=43.0,
            title="Potential False Spill Events (CSO Level > 43m with Pump Activation)",
            output_path="output/figures/potential_false_spills.png"
        )
        print(f"Found {len(false_spills)} potential false spill events.")
    else:
        print(false_spills_result['message']) # For normal spills
    
    # Plot rainfall vs CSO level correlation for a few days
    print("\nGenerating rainfall vs CSO level correlation plot...")

    significant_rainfall = rainfall_df[rainfall_df['RG_A'] > 5.0]  # More than 5mm of rain

    # Find a 5 day period with significant rainfall
    if not significant_rainfall.empty:
        start_date = significant_rainfall['time'].iloc[0]
        end_date = start_date + pd.Timedelta(days=5)
        
        # Create the plot
        plot_rainfall_cso_correlation(cso_df, rainfall_df, start_date, end_date, 'Rainfall vs CSO Level Correlation', 'output/figures/rainfall_cso_correlation.png')

        # Put these here for nice related plots
        plot_sps_cso_correlation(cso_df, sps_a1_df, start_date, end_date,'SPS_A1 vs CSO Level Correlation', 'output/figures/sps_a1_cso_correlation.png')
        plot_sps_cso_correlation(cso_df, sps_a2_df, start_date, end_date,'SPS_A2 vs CSO Level Correlation', 'output/figures/sps_a2_cso_correlation.png')
    else:
        print("\nNo significant rainfall events found in the dataset.")
    
    print("\nAnalysis complete. Results saved to output directory.")

if __name__ == "__main__":
    main() 
# Stantec Data Challenge 2025

This repository contains code for the Stantec Data Challenge 2025.

## Project Overview

This project analyses CSO (Combined Sewer Overflow), sewage pump station (SPS), and rainfall data.

## Data

This analysis explores potential relationships between:
- Rainfall and CSO level spikes
- Pump activations and potential spill events
- False positive spill signals caused by quick pump response
- Temporal and categorical patterns in event data

It includes:
- Data quality assessment (missing values, outliers, temporal coverage)
- Visualisation of CSO levels, pump events, and rainfall over time
- Correlation plots between rainfall, CSO, and SPS activity
- Detection of potential false spill events based on level thresholds and pump timings

## Data Sources

The project uses the following sheets from the provided Excel workbook:

| Sheet      | Description                                 |
|------------|---------------------------------------------|
| `RG_A`     | Rainfall intensity data (in mm)             |
| `CSO_A`    | Combined Sewer Overflow level readings      |
| `SPS_A1`   | Pump Station A1 events                      |
| `SPS_A2`   | Pump Station A2 events                      |

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Place your data file in the `data` directory

## Usage

Run the full analysis pipeline:
```
python main.py
```

## License

[N/A] 
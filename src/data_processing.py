import argparse
import os
from pathlib import Path
import pandas as pd
from utils import aggregate_to_hourly, sum_across_psr_types, remap

def process_file(filename, folder_path, data_type):
    if data_type == 'load':
        country_code = Path(filename).stem.split('_')[-1]
    elif data_type == 'gen':
        country_code = Path(filename).stem.split('_')[1]
    else:
        raise ValueError("Invalid data type. Use 'load' or 'gen'.")

    filepath = os.path.join(folder_path, filename)
    df = pd.read_csv(filepath)

    df['StartTime'] = pd.to_datetime(df['StartTime'], format='%Y-%m-%dT%H:%M+00:00Z')
    df['EndTime'] = pd.to_datetime(df['EndTime'], format='%Y-%m-%dT%H:%M+00:00Z')

    df['Country'] = country_code
    df = df.drop(columns=['AreaID'])

    df = aggregate_to_hourly(df, data_type)
    return df

def interpolate_missing_values(df):
    # Replace zeros with NaN to include them in interpolation
    df.replace(0, pd.NA, inplace=True)

    # Interpolate missing values (NaNs)
    df.interpolate(method='linear', limit_direction='forward', axis=0, inplace=True)

    # After interpolation, there might still be NaNs at the start or end of the DataFrame if those were missing,
    # as linear interpolation cannot fill these. You can decide to fill them with the first/last valid value or drop them.
    df.bfill(inplace=True)  # Backward fill
    df.ffill(inplace=True)  # Forward fill

    return df

def process_all_files_in_folder(folder_path):
    load_dataframes = []
    gen_dataframes = []
    Green_psrTypes = ["b01", "b09", "b10", "b11", "b12", "b13", "b15", "b16", "b18", "b19"]

    for file in os.listdir(folder_path):
        if file.endswith('.csv'):
            data_type = file.split('_')[0].lower()
            psr_type = file.split('_')[-1].split('.')[0].lower()
            try:
                if data_type == 'load':
                    aggregated_data = process_file(file, folder_path, data_type)
                    load_dataframes.append(aggregated_data)
                elif data_type == 'gen' and psr_type in Green_psrTypes:
                    aggregated_data = process_file(file, folder_path, data_type)
                    gen_dataframes.append(aggregated_data)
            except ValueError as e:
                print(f"Error processing {file}: {e}")


    if load_dataframes:
        load_df = pd.concat(load_dataframes, ignore_index=True)


    if gen_dataframes:
        gen_df = sum_across_psr_types(gen_dataframes)
    
    combined_df = remap(gen_df, load_df)
    return combined_df


def parse_arguments():
    parser = argparse.ArgumentParser(description='Data processing script for Energy Forecasting Hackathon')
    parser.add_argument(
        '--input_file',
        type=str,
        default='./data/raw_data/',
        help='Path to the raw data file folder to process'
    )
    parser.add_argument(
        '--output_file', 
        type=str, 
        default='./data/data.csv', 
        help='Path to save the processed data'
    )
    return parser.parse_args()

def main(input_folder, output_file):
    processed_df = process_all_files_in_folder(input_folder)
    cleaned_df = interpolate_missing_values(processed_df)
    cleaned_df.to_csv(output_file, index=False)

if __name__ == "__main__":
    args = parse_arguments()
    main(args.input_file, args.output_file)
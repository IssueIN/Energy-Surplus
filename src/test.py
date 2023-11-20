from utils import process_all_files_in_folder, remap

# process_all_files_in_folder('./data/raw_data/', './data/load_combined_data.csv', './data/green_energy_combined_data.csv')

# remap('./data/load_combined_data.csv', './data/green_energy_combined_data.csv', './data/data.csv')

import matplotlib.pyplot as plt
import pandas as pd

def plot_all_countries():
    df = pd.read_csv('./data/data.csv')
    # Set the 'StartTime' as the index for plotting
    df['StartTime'] = pd.to_datetime(df['StartTime'])
    df.set_index('StartTime', inplace=True)
    
    # Figure setup
    plt.figure(figsize=(15, 10))

    # Assuming the pattern 'green_energy_{CC}' for generation and '{CC}_Load' for load data
    for column in df.columns:
        if 'green_energy' in column or '_Load' in column:
            plt.plot(df.index, df[column], label=column, marker='o')

    # Titles and labels
    plt.title('Green Energy and Load Data Over Time')
    plt.xlabel('Time')
    plt.ylabel('Energy (Quantity/Load)')
    
    # Legend and grid
    plt.legend()
    plt.grid(True)
    
    # Improve layout to accommodate the legend
    plt.tight_layout()
    
    # Rotate date labels for better readability
    plt.xticks(rotation=45)
    
    # Show the plot
    plt.show()

plot_all_countries()
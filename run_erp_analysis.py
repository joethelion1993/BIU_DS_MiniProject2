from fingers_erp import calc_mean_erp
import os

# Define file paths
trial_points = os.path.join('mini_project_2_data', 'events_file_ordered.csv')
ecog_data = os.path.join('mini_project_2_data', 'brain_data_channel_one.csv')

# Ensure data availability
if os.path.exists(trial_points) and os.path.exists(ecog_data):
    
    print("Starting ERP analysis...")

    # Execute ERP calculation
    fingers_erp_mean = calc_mean_erp(trial_points, ecog_data)

    # Verify output dimensions
    print("-" * 30)
    print("Analysis Complete.")
    print(f"Matrix 'fingers_erp_mean' generated.")
    print(f"Shape: {fingers_erp_mean.shape}")

else:
    print("ERROR: Data files not found.")
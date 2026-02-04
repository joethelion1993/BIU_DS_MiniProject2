import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def calc_mean_erp(trial_points, ecog_data):
    """
    Calculates and plots the averaged Event-Related Potential (ERP) for five finger movements.
    
    Parameters:
    -----------
    trial_points : str
        Path to the CSV file containing event markers.
    ecog_data : str
        Path to the CSV file containing the ECOG electrode time series.
        
    Returns:
    --------
    numpy.ndarray
        A 5x1201 matrix named 'fingers_erp_mean' ordered by fingers 1-5.
    """
    
    # Load event markers (force int type)
    events_df = pd.read_csv(trial_points, dtype=int)
    
    # Load continuous ECOG signal
    raw_ecog_signal = pd.read_csv(ecog_data, header=None).squeeze()
    
    # Define epoch time window (200ms pre, 1ms onset, 1000ms post)
    PRE_ONSET_SAMPLES = 200
    POST_ONSET_SAMPLES = 1000
    TOTAL_WINDOW_SIZE = PRE_ONSET_SAMPLES + 1 + POST_ONSET_SAMPLES
    
    # Initialize output matrix
    fingers_erp_mean = np.zeros((5, TOTAL_WINDOW_SIZE))
    
    plt.figure(figsize=(10, 6))
    
    # Process each finger class
    for finger_id in range(1, 6):
        
        # Filter events for current finger
        finger_events = events_df[events_df['finger'] == finger_id]
        
        # Collect valid epochs
        finger_epochs = []
        
        for start_index in finger_events['starting_point']:
            window_start = start_index - PRE_ONSET_SAMPLES
            window_end = start_index + POST_ONSET_SAMPLES + 1 
            
            # Boundary check
            if window_start >= 0 and window_end <= len(raw_ecog_signal):
                epoch = raw_ecog_signal[window_start:window_end].values
                finger_epochs.append(epoch)
        
        # Compute mean and store
        if finger_epochs:
            mean_response = np.mean(finger_epochs, axis=0)
            fingers_erp_mean[finger_id - 1, :] = mean_response
            plt.plot(mean_response, label=f'Finger {finger_id}')
        
    # Plot configuration
    plt.title('Averaged Brain Response by Finger')
    plt.xlabel('Time Points (Indices)')
    plt.ylabel('Signal Amplitude')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    return fingers_erp_mean
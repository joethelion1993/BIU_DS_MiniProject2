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

    # Load event markers (force int type for indices)
    events_df = pd.read_csv(trial_points, dtype=int)

    # Load continuous ECOG signal
    raw_ecog_signal = pd.read_csv(ecog_data, header=None).squeeze()

    # Define epoch time window (200ms pre, 1ms onset, 1000ms post)
    PRE_ONSET = 200
    POST_ONSET = 1000
    WINDOW_SIZE = PRE_ONSET + 1 + POST_ONSET

    # Initialize output matrix
    fingers_erp_mean = np.zeros((5, WINDOW_SIZE))

    plt.figure(figsize=(10, 6))

    # Process each finger class (1-5)
    for finger_id in range(1, 6):
        
        # Filter events for the specific finger
        finger_events = events_df[events_df['finger'] == finger_id]
        finger_epochs = []

        # Extract epochs based on starting points
        for start_idx in finger_events['starting_point']:
            w_start = start_idx - PRE_ONSET
            w_end = start_idx + POST_ONSET + 1

            # Validate indices against signal boundaries
            if w_start >= 0 and w_end <= len(raw_ecog_signal):
                epoch = raw_ecog_signal[w_start:w_end].values
                finger_epochs.append(epoch)

        # Compute average across trials
        if finger_epochs:
            mean_response = np.mean(finger_epochs, axis=0)
            
            # Store result (Row 0 = Finger 1)
            fingers_erp_mean[finger_id - 1, :] = mean_response
            
            # Add to plot
            plt.plot(mean_response, label=f'Finger {finger_id}')

    # Finalize plot
    plt.title('Averaged Brain Response by Finger')
    plt.xlabel('Time Points (Indices)')
    plt.ylabel('Signal Amplitude')
    plt.legend()
    plt.grid(True)
    plt.show()

    return fingers_erp_mean
import numpy as np

def detect_significant_drop(sequence, window=4, significance_factor=2):
    if len(sequence) <= window:
        raise ValueError("Sequence length must be greater than the window size.")
    
    recent_values = sequence[-window:]
    past_values = sequence[:-window]
 
    mean_past = np.mean(past_values)
    std_past = np.std(past_values)
    mean_recent = np.mean(recent_values)
 
    significance_threshold = mean_past - (significance_factor * std_past)
    is_significant_drop = mean_recent < significance_threshold
 
    drop_continuation_period = 0
    for i in range(len(recent_values) - 1):
        if recent_values[i] > recent_values[i + 1]:
            drop_continuation_period += 1
        else:
            break

    return is_significant_drop, {
        "mean_past": mean_past,
        "std_past": std_past,
        "mean_recent": mean_recent,
        "significance_threshold": significance_threshold,
        "recent_values": recent_values,
        "drop_continuation_period": drop_continuation_period,
    }

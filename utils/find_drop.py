import numpy as np
import pandas as pd 

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


def create_quarterly_growth(df: pd.DataFrame, quarter: str = "Mar", row_index: int = 0) -> tuple: 
    filter_df = df.iloc[row_index]
    filter_df = filter_df[filter_df.index.str.startswith(quarter)]
    raw_diff, perc_diff = [], []
    for i in range(1, len(filter_df)) : 
        raw_diff.append(filter_df.iloc[i] - filter_df.iloc[i-1])
        perc_diff.append(round(((filter_df.iloc[i] - filter_df.iloc[i-1])/filter_df.iloc[i])*100, 2))

    return raw_diff, perc_diff, filter_df
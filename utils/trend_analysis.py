import numpy as np
from scipy.stats import linregress
from scipy.stats import pearsonr

def classify_trend(sequence): 
    x = np.arange(len(sequence))
    y = np.array(sequence) 
    weights = np.linspace(0.1, 1, len(sequence))   

    x_mean = np.average(x, weights=weights)
    y_mean = np.average(y, weights=weights)

    cov_xy = np.sum(weights * (x - x_mean) * (y - y_mean)) / np.sum(weights)
    var_x = np.sum(weights * (x - x_mean) ** 2) / np.sum(weights)
 
    slope = cov_xy / var_x
    intercept = y_mean - slope * x_mean
 
    y_pred = slope * x + intercept
    ss_total = np.sum(weights * (y - y_mean) ** 2)
    ss_residual = np.sum(weights * (y - y_pred) ** 2)
    r_squared = 1 - ss_residual / ss_total
 
    if slope > 0:
        direction = "Upward"
    elif slope < 0:
        direction = "Downward"
    else:
        direction = "No Trend"

    correlation = np.sqrt(r_squared) if slope >= 0 else -np.sqrt(r_squared)

    if abs(correlation) > 0.75:
        strength = "Strong"
    elif abs(correlation) > 0.5:
        strength = "Medium"
    else:
        strength = "Weak"

    return {
        "direction": direction,
        "strength": strength,
        "slope": slope,
        "corr": correlation
    }
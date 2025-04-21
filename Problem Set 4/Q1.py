import numpy as np

# Define the mixing matrix M
M = np.array([
    [0.119, 0.053, 0.074, 0.055, 0.022],
    [0.031, 0.067, 0.061, 0.026, 0.011],
    [0.025, 0.027, 0.083, 0.024, 0.006],
    [0.049, 0.033, 0.043, 0.073, 0.011],
    [0.006, 0.005, 0.005, 0.005, 0.085]
])

# Calculate err_r (sum of diagonal elements)
err = np.trace(M)

# Calculate ar_r (sum of rows)
ar = np.sum(M, axis=1)

print("err:", err)
print("ar:", ar)

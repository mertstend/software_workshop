import numpy as np
from matplotlib import pyplot as plt

# Generate some data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create a figure and axis
fig, ax = plt.subplots()

# Plot the data
ax.plot(x, y, label='Sine Wave')

# Add a title and labels
ax.set_title('Simple Sine Wave Plot')
ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')

# Add a legend
ax.legend()

# Show the plot
plt.savefig('manuscript/figures/sine_wave.png')
plt.show()
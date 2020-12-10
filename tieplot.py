import os
import sys
import matplotlib.pyplot as plt
import pandas as pd
import pdb

# Dict where key = subject, value = list of screen switches in seconds
# Can potentially pull this from a csv
subjects = pd.read_csv('summary_data.csv')
i = 0
for sub in subjects:
    screen = subjects[sub].dropna().sort_values(ascending=False)
    color = 'b'
    label = 'Screen A'
    for x in screen:
        if i == 0:
            plt.barh(sub, x, color=color, label = 'Screen A', height = 0.5)
        elif i == 1:
            plt.barh(sub, x, color=color, label = 'Screen B', height = 0.5)
        else:
            plt.barh(sub, x, color=color, height = 0.5)
        i += 1
        if color == 'b':
            color = 'r'
        else:
            color = 'b'

# Need to add legend

plt.plot()
plt.xlabel("Elapsed time (s)")
plt.ylabel("Subject")
plt.title("WonderWoW Tie Plot")
plt.legend(loc='upper right')
plt.show()
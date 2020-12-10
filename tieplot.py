import os
import sys
import matplotlib.pyplot as plt
import pandas as pd
import pdb

subjects = pd.read_csv('https://raw.githubusercontent.com/EricRob/wonderwow/main/summary_data.csv')
i = 0
for sub in subjects:
    screen = subjects[sub].dropna().sort_values(ascending=False)
    if screen.size % 2 == 1:
        color = 'b'
        label = 'Screen A'
    else:
        color = 'r'
        label = 'Screen B'

    for x in screen:
        if i == 0:
            plt.barh(sub, x, color=color, label = label, height = 0.5)
            if label == 'Screen A':
                label = 'Screen B'
            else:
                label == 'Screen A'
        elif i == 1:
            plt.barh(sub, x, color=color, label = label, height = 0.5)
        else:
            plt.barh(sub, x, color=color, height = 0.5)
        
        i += 1
        
        if color == 'b':
            color = 'r'
        else:
            color = 'b'

plt.plot()
plt.xlabel("Elapsed time (s)")
plt.ylabel("Subject")
plt.title("WonderWoW Tie Plot")
plt.legend(loc='upper right')
plt.show()
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from operator import itemgetter
import pdb

# Sample annotation data
# Jeff will probably write these as "Start Times," whereas screen switches are
# "End Times." We can either handle this when saving the data, or afterward.
# Currently, this is written to receive End Times.
annotations = {"TM": [("HPI", 489.48), ("A&P", 1200), ("PE", 750)],
               "CC": [("HPI", 222.18), ("A&P", 2000), ("PE", 1000)],
               "JC": [("HPI", 304.04), ("A&P", 1200), ("PE", 750)],
               "SR": [("HPI", 250), ("A&P", 1200), ("PE", 750)],
               "NT": [("HPI", 250), ("A&P", 1200), ("PE", 750)]}

#annotations data frame
af = pd.read_csv('https://raw.githubusercontent.com/EricRob/wonderwow/main/annotation.csv')
# pdb.set_trace()


# Sort annotations data in descending order
for subject in annotations:
  annotations[subject].sort(key=itemgetter(1), reverse=True)

#Load subject times into a dataframe
subjects = pd.read_csv('https://raw.githubusercontent.com/EricRob/wonderwow/main/summary_data.csv')
i = 0
j = 0
index = np.arange(subjects.size + 1)
height = 0.3
ann_colors = {"HPI": 'bisque', "A&P": 'violet', "PE": 'skyblue'}

# helper method for drawing annotations
def draw_annotations(ind, sub, label=False):
  if label:
    for part in annotations[sub]:
      plt.barh(ind - height/2, part[1], color=ann_colors[part[0]], label=part[0], height=height)
  else:
    for part in annotations[sub]:
      plt.barh(ind - height/2, part[1], color=ann_colors[part[0]], height=height)

for sub in subjects:
    # Place one subject's data into a series, last switch at the first index
    screen = subjects[sub].dropna().sort_values(ascending=False)
    
    # If there is an odd number of switches, A is the last screen (and thus 
    # the first to be drawn). Otherwise B. 
    if screen.size % 2 == 1:
        color = 'b'
        label = 'Screen A'
    else:
        color = 'r'
        label = 'Screen B'
    
    # Draw annotation data once for each subject
    j += 1
    if j == 1:
      draw_annotations(index[j], sub, label=True)
    else:
      draw_annotations(index[j], sub)

    # Each switch will be a rectangle with width equal to its timestamp
    # Earlier timestamps are drawn on top of the previous rectangle (hence the
    # descending order)
    for x in screen:
        if i == 0:
            plt.barh(index[j] + height/2, x, color=color, label=label, height=height)
            if label == 'Screen A':
                label = 'Screen B'
            else:
                label == 'Screen A'
        elif i == 1:
            plt.barh(index[j] + height/2, x, color=color, label=label, height=height)
        else:
            plt.barh(index[j] + height/2, x, color=color, height=height)
        
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

# plt.show()

plt.cla()
# Calculate time per screen
stamps_b = subjects.iloc[1::2, :]
stamps_a = subjects.iloc[::2, :]

subj_order = []

screen_a_sums = []
screen_b_sums = []

pct_screen_a = []
pct_screen_b = []

total_times = []
total_switches = []

# round to n digits
n = 1

for subject in subjects:
  subj_order.append(subject)

  st_b = stamps_b[subject].dropna().array
  st_a = stamps_a[subject].dropna().array
  total_switches.append(st_a.size + st_b.size)

  if st_b.size != st_a.size:
    st_b = np.append(st_b,0)
    fix = True
  else:
    fix = False
  
  times_b = st_b - st_a
  times_a = st_a - np.roll(st_b,1)

  if fix:
    times_b = times_b[:-1]
  else:
    times_a[0] = st_a[0]

  screen_sum_a = np.sum(times_a)
  screen_sum_b = np.sum(times_b)
  total_time = (screen_sum_a + screen_sum_b).round(n)

  screen_a_sums.append(screen_sum_a.round(n))
  screen_b_sums.append(screen_sum_b.round(n))
  total_times.append(total_time.round(n))

  pct_screen_a.append(((screen_sum_a / total_time)*100).round(n))
  pct_screen_b.append(((screen_sum_b / total_time)*100).round(n))

columns = subj_order
rows = ['Screen A (%)', 'Screen B (%)', 'Total A (s)', 'Total B (s)', 'Total switches']
cell_text = [pct_screen_a, pct_screen_b, screen_a_sums, screen_b_sums, total_switches]
the_table = plt.table(cellText=cell_text,
                      rowLabels=rows,
                      colLabels=columns)
# plt.show()

plt.clf()

width = 0.35

plt.bar(1-width/2, np.mean(pct_screen_a), width = width, color='orange', label='Screen A')
plt.bar(1+width/2, np.mean(pct_screen_b), width = width, color='blue', label='Screen B')


for pct in pct_screen_a:
  plt.plot(1-width/2, pct,'o', c='k', mfc='none')
for pct in pct_screen_b:
  plt.plot(1+width/2, pct,'o', c='k', mfc='none')
# plt.axis([0.5,2.5,0,100])
plt.ylabel('Percent of total time')




# Building per-section paired plots
sub_df = af.iloc[:,0]
an_sections = []

group_a_sums = []
group_b_sums = []

group_a_pcts = []
group_b_pcts = []

group_time_totals = []
group_switches = []

group_order = []

for i in range(1,len(af.columns),2):

    # make a dataframe of subject, start, end for each annotation section.
    # This assumes the start and end times are paired, like in the
    # example that Eric sent Jeff.
    an_set = af.iloc[:,[i, i+1]]
    an_set['subjects'] = sub_df.values
    an_set = an_set.sort_index(axis=1, ascending=False)
    an_sections.append(an_set)

    screen_a_sums = []
    screen_b_sums = []

    pct_screen_a = []
    pct_screen_b = []

    total_times = []
    total_switches = []

    first_pass = True

    # Loop over rows and take slices of overall stamps based on the
    # annotation start and end times
    for index, row in an_set.iterrows():
        subject, start, end = row[0], row[1], row[2]

        # This little block pulls out the annotation section name
        if first_pass:
            group_order.append(an_set.columns[1][:-6])
            first_pass = False

        # Take a slice of the stamps array 
        st_b = stamps_b[subject].dropna().array
        st_b = st_b[st_b > start]
        st_b = st_b[st_b < end]

        st_a = stamps_a[subject].dropna().array
        st_a = st_a[st_a > start]
        st_a = st_a[st_a < end]
        
        # if first switch to screen is earliest, then annotation section
        # started on that screen
        if st_a[0] > st_b[0]:
            st_a = np.insert(st_a, 0, start)
            start_a = False
        else:
            st_b = np.insert(st_b, 0, start)
            start_a = True

        # if last switch to screen is latest, then annotation section
        # finished on the other screen
        if st_a[-1] > st_b[-1]:
            st_b = np.append(st_b, end)
            end_a = False
        else:
            st_a = np.append(st_a, end)
            end_a = True

        # In the event you start and end on different screens, need to
        # adjust the array length to allow numpy subtraction
        if (start_a and not end_a):
            st_a = np.append(st_a,end-0.1)
        elif (not start_a and end_a):
            st_b = np.append(st_b,end-0.1)
        # screen time is the sum of intervals
        if start_a:
            times_a = st_a - st_b
            times_b = np.roll(st_b,-1) - st_a
        else:
            times_b = st_b - st_a
            times_a = np.roll(st_a,-1) - st_a

        # After the roll and in the cases of start/end mismatches there
        # will be a negative value, remove it
        times_a = times_a[times_a >= 0]
        times_b = times_b[times_b >= 0]
        total_switches.append(max(times_a.size + times_b.size - 1, 0))
        
        screen_sum_a = np.sum(times_a)
        screen_sum_b = np.sum(times_b)
        total_time = (screen_sum_a + screen_sum_b).round(n)

        screen_a_sums.append(screen_sum_a.round(n))
        screen_b_sums.append(screen_sum_b.round(n))

        total_times.append(total_time.round(n))

        pct_screen_a.append(((screen_sum_a / total_time)*100).round(n))
        pct_screen_b.append(((screen_sum_b / total_time)*100).round(n))

    group_a_sums.append(screen_a_sums)
    group_b_sums.append(screen_b_sums)

    group_a_pcts.append(pct_screen_a)
    group_b_pcts.append(pct_screen_b)

    group_time_totals.append(total_time)
    group_switches.append(total_switches)

# Draw the paired bar plots with individual data points
for i in range(len(group_order)):
    idx = i + 2
    plt.bar(idx-width/2, np.mean(group_a_pcts[i]), width = width, color='orange', label='Screen A')
    plt.bar(idx+width/2, np.mean(group_b_pcts[i]), width = width, color='blue', label='Screen B')    

    for pct in group_a_pcts[i]:
        plt.plot(idx-width/2, pct,'o', c='k', mfc='none')
    for pct in group_b_pcts[i]:
        plt.plot(idx+width/2, pct,'o', c='k', mfc='none')

plt.xticks(np.arange(1, len(group_order)+2), ['total'] + group_order)
plt.axis([0.5,len(group_order) + 1.5,0,100])
plt.show()
plt.legend(loc='upper right')
plt.title('Screen time by section')
pdb.set_trace()

























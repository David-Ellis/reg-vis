'''
Visualise regression results
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.transforms import ScaledTranslation

plt.rc('font', size=11) #controls default text size

data={
      'Variable group' : ["Animal", "Animal", "Age (years)",
                          "Age (years)", "Age (years)"],
      'Variable':["Cat", "Dog", "1-2", "3-4", "5-6"],
      'Odds Ratio': [1.,2.3,1.3,2.7, 6.],
      'Conf int upper' : ["Ref", 2.5, 1.4, 3.0, 7.],
      'Conf int lower' : ["Ref", 2.1, 1.2, 2.4, 5.],
      }

df=pd.DataFrame(data)

def pack_errors(df):
    num_items = len(df['Odds Ratio'])
    errors = np.zeros((2, num_items))
    for i in range(num_items):
        # if ref, check that upper and lower are both marked as reference
        if df["Conf int upper"][i] == "Ref" or df["Conf int lower"][i] == "Ref":
            assert df["Conf int upper"][i] == df["Conf int lower"][i],\
                "Both upper and lower error value should be \"Ref\""
            pass
        else:
            errors[0, i] = df['Conf int upper'][i] - df["Odds Ratio"][i]
            errors[1, i] = df["Odds Ratio"][i] - df['Conf int lower'][i]
    return errors

def pack_group_names(df):
    group_names = []
    num_items = len(df['Odds Ratio'])
    last_group = "Start"
    for i in range(num_items):
        group_i = df['Variable group'][i]
        if group_i != last_group:
            group_names.append(group_i)
            last_group = group_i
        else:
            group_names.append("")
    return group_names

def pack_odds_values(df):
    odds_values = []
    num_items = len(df['Odds Ratio'])
    for i in range(num_items):
        if df["Conf int upper"][i] == "Ref":
            new_val = "    Reference"
        else:
            new_val = "{:.2f} ({:.2f}, {:.2f})".format(df["Odds Ratio"][i],
                                                    df["Conf int lower"][i],
                                                    df["Conf int upper"][i])
        odds_values.append(new_val)
    return odds_values

num_items = len(df['Odds Ratio'])

fig = plt.figure(figsize = (7, num_items),)


gs = GridSpec(num_items*100 + 100, 1300)
head1 = plt.subplot(gs[:100, :500])
head2 = plt.subplot(gs[:100, 500:900])
head3 = plt.subplot(gs[:100, 900:])

ax1 = plt.subplot(gs[100:, :500])
ax2 = plt.subplot(gs[100:, 500:900])
ax3 = plt.subplot(gs[100:, 900:])

ticks = np.arange(1, num_items+1)



## Headers ##
header_labels = ["Variable", "Odds Ratio", 
                 "       Odds Ratio\n(Confidence Interval)"]
header_offset = [-2.1, -1.7, -1.73]
for i, head in enumerate([head1, head2, head3]):
    head.set_xticks([])
    head.yaxis.set_label_position("right")
    head.yaxis.tick_right()
    head.set_yticks([0.5])
    head.set_yticklabels([header_labels[i]])
    head.tick_params(right = False, left = False)
    # offset y ticks
    offset = ScaledTranslation(header_offset[i], 0, fig.dpi_scale_trans)
    for label in head.yaxis.get_majorticklabels():
        label.set_transform(label.get_transform() + offset)
        
## Variable names ##
group_names = pack_group_names(df)
# move y-axis to the right
ax1.yaxis.set_label_position("right")
ax1.yaxis.tick_right()
# set ticks
ax1.set_yticks(ticks)
ax1.set_yticklabels(group_names[::-1])
ax1.set_xticks([])
ax1.set_ylim(1-0.2*num_items, num_items+0.2*num_items)
ax1.set_xlim(0, 1)

# offset y ticks
offset_ax1 = ScaledTranslation(-2.1, 0, fig.dpi_scale_trans)
for label in ax1.yaxis.get_majorticklabels():
    label.set_transform(label.get_transform() + offset_ax1)

        
## Odds ratio plot ##
errors = pack_errors(df)

ax2.errorbar(df["Odds Ratio"], ticks[::-1], xerr=errors, fmt = "ko")
# move y-axis to the right
ax2.yaxis.set_label_position("right")
ax2.yaxis.tick_right()
# plot reference line
ax2.plot([1, 1], [1-0.2*num_items, num_items+0.2*num_items], "k--")
ax2.set_ylim(1-0.2*num_items, num_items+0.2*num_items)
#ax2.set_yticks([])
ax2.set_yticks(ticks)
ax2.set_yticklabels(df["Variable"].values[::-1])
ax2.tick_params(right = False, left = False)

# offset y ticks
offset_ax2 = ScaledTranslation(-2.5, 0, fig.dpi_scale_trans)
for label in ax2.yaxis.get_majorticklabels():
    label.set_transform(label.get_transform() + offset_ax2)

## Odds ratio numbers ##
odds_values = pack_odds_values(df)
# move y-axis to the right
ax3.yaxis.set_label_position("right")
ax3.yaxis.tick_right()
ax3.set_xticks([])
ax3.set_yticks(ticks)
ax3.set_yticklabels(odds_values[::-1])
ax3.set_ylim(1-0.2*num_items, num_items+0.2*num_items)

ax3.tick_params(right = False, left = False)

# offset y ticks
offset_ax3 = ScaledTranslation(-1.55, 0, fig.dpi_scale_trans)
for label in ax3.yaxis.get_majorticklabels():
    label.set_transform(label.get_transform() + offset_ax3)
    
plt.savefig("example.png", bbox_inches="tight")
    
    
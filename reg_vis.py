'''
Visualise regression results
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.transforms import ScaledTranslation

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

def firstUnqiue(input_list):
    output = []
    for item in input_list:
        if item not in output:
            output.append(item)
    return output

def getGroupBoundaries(df):
    '''
    Parameters
    ----------
    all_groups : array-like
        list of the group each variable belongs to .

    Returns
    -------
    boundaries : array
        array of lists containing boundaries for each group.
    '''
    all_groups = df["Variable group"].values
    groups = firstUnqiue(all_groups)
    N_groups = len(groups)
    boundaries = np.zeros(N_groups, dtype = object)
    last = len(all_groups)
    for i, group in enumerate(groups):
        N_group_i = len(all_groups[all_groups == group])
        new_boundary = [last, last - N_group_i]
        last -= N_group_i
        boundaries[i] = new_boundary
    return boundaries

class reg_plot:
    def __init__(self):
        self.font_size = 10
        self.header_size = 11
        self.group_size = 10.5
        self.var_offset = 0
        
    def load_data(self, data_path):
        extension = data_path.split(".")[-1]
        if extension == "csv":
            self.df = pd.from_csv(data_path)
        elif extension == "xlsx":
            self.df = pd.read_excel(data_path)
    
    def plot(self, 
             counts = False,
             group1_color = None,
             group2_color = None,
             group_alpha = 0.2):
        # set plot size
        plt.rc('font', size=self.font_size)
        
        num_items = len(self.df['Odds Ratio'])
        
        if counts:
            specWidth = 1500
            figWidth = 10
        else: 
            specWidth = 1300
            figWidth = 8
        
        self.fig = plt.figure(figsize = (figWidth, num_items-2),)
        
        gs = GridSpec(num_items*100 + 100, specWidth)
        head1 = plt.subplot(gs[:100, :500])
        head2 = plt.subplot(gs[:100, 500:900])
        head3 = plt.subplot(gs[:100, 900:1300])
        
        ax1 = plt.subplot(gs[100:, :500])
        ax2 = plt.subplot(gs[100:, 500:900])
        ax3 = plt.subplot(gs[100:, 900:1300])
        
        ticks = np.arange(1, num_items+1)
        ylims = [1-0.1*num_items, num_items+0.1*num_items]
        
        ## Headers ##
        header_labels = ["Variable", 
                         "Odds Ratio", 
                         "       Odds Ratio\n(Confidence Interval)",
                         "Number (N)"]
        header_offset = [-2.35, -1.9, 
                         -1.83- counts*0.11, -1.05]        
        heads = [head1, head2, head3]
        
        if counts:
            head4 = plt.subplot(gs[:100, 1300:specWidth])
            heads.append(head4)
            ax4 = plt.subplot(gs[100:, 1300:specWidth])

        for i, head in enumerate(heads):
            head.set_xticks([])
            head.yaxis.set_label_position("right")
            head.yaxis.tick_right()
            head.set_yticks([0.5])
            head.set_yticklabels([header_labels[i]])
            head.tick_params(right = False, left = False)
            head.tick_params(axis='both', which='major', 
                             labelsize=self.header_size)
            # offset y ticks
            offset = ScaledTranslation(header_offset[i], 0, self.fig.dpi_scale_trans)
            for label in head.yaxis.get_majorticklabels():
                label.set_transform(label.get_transform() + offset)
                
        ## Variable names ##
        group_names = pack_group_names(self.df)
        # move y-axis to the right
        ax1.yaxis.set_label_position("right")
        ax1.yaxis.tick_right()
        # set ticks
        ax1.set_yticks(ticks)
        ax1.set_yticklabels(group_names[::-1])
        ax1.set_xticks([])
        ax1.set_ylim(ylims)
        ax1.set_xlim(0, 1)
        ax1.tick_params(axis='both', which='major', 
                             labelsize=self.group_size)
        
        # offset y ticks
        offset_ax1 = ScaledTranslation(-2.4, 0, self.fig.dpi_scale_trans)
        for label in ax1.yaxis.get_majorticklabels():
            label.set_transform(label.get_transform() + offset_ax1)
        
                
        ## Odds ratio plot ##
        errors = pack_errors(self.df)
        
        ax2.errorbar(self.df["Odds Ratio"], ticks[::-1], xerr=errors, fmt = "ko")
        # move y-axis to the right
        ax2.yaxis.set_label_position("right")
        ax2.yaxis.tick_right()
        # plot reference line
        ax2.plot([1, 1], [1-0.2*num_items, num_items+0.2*num_items], "k--")
        ax2.set_ylim(ylims)
        #ax2.set_yticks([])
        ax2.set_yticks(ticks)
        ax2.set_yticklabels(self.df["Variable"].values[::-1])
        ax2.tick_params(right = False, left = False)
        ax2.set_xlim(min(self.df['Odds Ratio'])-0.3, 
                     max(self.df['Odds Ratio'])*1.3)
        
        
        # offset y ticks
        offset_ax2 = ScaledTranslation(-2.85 + self.var_offset, 0, self.fig.dpi_scale_trans)
        for label in ax2.yaxis.get_majorticklabels():
            label.set_transform(label.get_transform() + offset_ax2)
        
        ## Odds ratio numbers ##
        odds_values = pack_odds_values(self.df)
        # move y-axis to the right
        ax3.yaxis.set_label_position("right")
        ax3.yaxis.tick_right()
        ax3.set_xticks([])
        ax3.set_yticks(ticks)
        ax3.set_yticklabels(odds_values[::-1])
        ax3.set_ylim(ylims)
        
        ax3.tick_params(right = False, left = False)
        ax3.set_xlim(0, 1)
        # offset y ticks
        offset_ax3 = ScaledTranslation(-1.60 - counts*0.11, 0, self.fig.dpi_scale_trans)
        for label in ax3.yaxis.get_majorticklabels():
            label.set_transform(label.get_transform() + offset_ax3)
            
        ## Variable counts ##
        
        if counts:
            ax4.set_xticks([])
            ax4.set_yticks(ticks)
            ax4.yaxis.tick_right()
            ax4.tick_params(right = False, left = False)
            # Add the numbers here
            ax4.set_yticklabels(self.df["Number"].values[::-1])
            ax4.set_ylim(ylims)
            ax4.set_xlim(0, 1)
            # get maximum number magnitude to move positions accordingly
            max_mag = np.log10(max(self.df["Number"].values)) + 1
            offset_ax4 = ScaledTranslation(-0.6-max_mag/20, 0, self.fig.dpi_scale_trans)
            for label in ax4.yaxis.get_majorticklabels():
                label.set_transform(label.get_transform() + offset_ax4)
            
        ## Group color ##
        if group1_color != None or group2_color != None :
            boundaries = getGroupBoundaries(self.df)
            for i, boundary in enumerate(boundaries):
                if i % 2 == 0:
                    color = group1_color
                else:
                    color = group2_color
                    
                if i == 0:
                    boundary[0] = ylims[1]
                elif i == len(boundaries)-1:
                    boundary[1] = ylims[0]-0.5
                if color != None:    
                    ax1.fill_between([0, 1], 
                                     [boundary[0]+0.5,boundary[0]+0.5],
                                     [boundary[1]+0.5,boundary[1]+0.5],
                                     color = color,
                                     lw = 0,
                                     alpha = group_alpha)
                    ax2.fill_between([-10, 10], 
                                     [boundary[0]+0.5,boundary[0]+0.5],
                                     [boundary[1]+0.5,boundary[1]+0.5],
                                     color = color,
                                     lw = 0,
                                     alpha = group_alpha)
                    ax3.fill_between([0, 1], 
                                     [boundary[0]+0.5,boundary[0]+0.5],
                                     [boundary[1]+0.5,boundary[1]+0.5],
                                     color = color,
                                     lw = 0,
                                     alpha = group_alpha)
                    if counts:
                        ax4.fill_between([0, 1], 
                                     [boundary[0]+0.5,boundary[0]+0.5],
                                     [boundary[1]+0.5,boundary[1]+0.5],
                                     color = color,
                                     lw = 0,
                                     alpha = group_alpha)
    def save_plot(self, save_path):
        plt.savefig(save_path, bbox_inches="tight")





    
    
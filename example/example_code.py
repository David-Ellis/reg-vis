# -*- coding: utf-8 -*-
"""
Example code for using reg-vis
"""
import sys
sys.path.append('..')

import reg_vis

reg_vis = reg_vis.reg_plot()

reg_vis.load_data("example_data.xlsx")
reg_vis.plot(counts = True, 
             group1_color = None,
             group2_color = "yellow",
             group_alpha = 0.15,
             head_fill = "gray")

reg_vis.save_plot("example_plot.png")
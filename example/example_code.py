# -*- coding: utf-8 -*-
"""
Example code for using reg-vis
"""
import sys
sys.path.append('..')

import reg_vis

reg_vis = reg_vis.reg_plot()
reg_vis.load_data("example_data.xlsx")
reg_vis.plot()
reg_vis.save_plot("example.png")
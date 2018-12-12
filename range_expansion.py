# -*- coding: utf-8 -*-
"""
Matthew Allcock
Research Intern, Animal Ethics
"""

import numpy as np

x_range = 100  # 15000
y_range = 20
t_range = 100

x_vals = np.arange(x_range)
y_vals = np.arange(y_range)

xx, yy = np.meshgrid(x_vals, y_vals)

t_vals = np.arange(t_range)

m = 0.01  # mutation probability
m_m = 0.1  # magnitude of mutation

K = 20  # equilibrium density
R = 3  # maximum possible mean number of offspring

# Initialise pseudogenes for reproduction, competitive ability, dispersal
pRep = np.empty_like(xx)
pRep[:] = np.nan
pRep[:y_range, :] = 0.3

pComp = np.empty_like(xx)
pcomp[:] = np.nan
pComp[:y_range, :] = 0.3

pDisp = np.empty_like(xx)
pDisp[:] = np.nan
pDisp[:y_range, :] = 0.4


lamb = pRep * R

survival_prob = min(K * pComp / sComp, 1)

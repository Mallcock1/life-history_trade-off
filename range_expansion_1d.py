# -*- coding: utf-8 -*-
"""
Matthew Allcock
Research Intern, Animal Ethics
"""

import numpy as np

Nx = 10  # total number of patches in x
Nx_init = 10  # number of intially habitable patches in x
Nt = 100  # number of generational iterations

x_vals = np.arange(Nx)

t_vals = np.arange(Nt)

m = 0.01  # mutation probability
m_m = 0.1  # magnitude of mutation

K = 5  # equilibrium density
R = 3  # maximum possible mean number of offspring

## Initialise pseudogenes for reproduction, competitive ability, dispersal
#pRep = np.empty_like(xx)
#pRep[:] = np.nan
#pRep[:y_range, :] = 0.3
#
#pComp = np.empty_like(xx)
#pcomp[:] = np.nan
#pComp[:y_range, :] = 0.3
#
#pDisp = np.empty_like(xx)
#pDisp[:] = np.nan
#pDisp[:y_range, :] = 0.4


# initialise trait lists
num_animals = np.zeros(Nx, dtype=object)
pRep = np.empty(Nx, dtype=object)
pComp = np.empty(Nx, dtype=object)
pDisp = np.empty(Nx, dtype=object)
for i in range(Nx):
    pRep[i] = []
    pComp[i] = []
    pDisp[i] = []

# set up dictionary
habitat = {
  "x": x_vals,
  "num of animals": num_animals,
  "pRep": pRep,
  "pComp": pComp,
  "pDisp": pDisp,
}

# Set up initial individuals
init_number = 15  # 500 # initial number of individuals
for i in range(init_number):
    r = np.random.randint(0, Nx_init)
    pRep_ran = np.random.random()
    pComp_ran = np.random.random()
    pDisp_ran = np.random.random()

    total = pRep_ran + pComp_ran + pDisp_ran

    # Normalise
    pRep_norm = pRep_ran / total
    pComp_norm = pComp_ran / total
    pDisp_norm = pDisp_ran / total

    habitat["num of animals"][r] = habitat["num of animals"][r] + 1
    habitat["pRep"][r].append(pRep_norm)
    habitat["pComp"][r].append(pComp_norm)
    habitat["pDisp"][r].append(pDisp_norm)

for t in t_vals:  # iterate through time
    for x in habitat["x_vals"]:  # iterate through patches
        sComp = sum(habitat["pComp"][x])  # Sum of competitiveness of all individuals of given patch
        for i in range(habitat["num of animals"][x]):  # iterate through individuals in a patch
            lamb = habitat["pRep"][x][i] * R  # lambda value for Poisson distribution
            
            pComp = habitat["pComp"][x][i]
            surv_prob = min(K * pComp / sComp, 1)  # probability of survival to next generation
            
            surv_ran = np.random.random()
            if surv_ran < surv_prob:
                # animal dies
                habitat["num of animals"][x] -= 1
                del habitat["pRep"][x][i]
                del habitat["pComp"][x][i]
                del habitat["pDisp"][x][i]
            else:
                # animal reproduces 
            # FINISH THIS BIT and start a github repo
            
            
            
            
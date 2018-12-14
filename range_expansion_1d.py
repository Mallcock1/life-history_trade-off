# -*- coding: utf-8 -*-
"""
Matthew Allcock
Research Intern, Animal Ethics
"""

import numpy as np

Nx = 10  # total number of patches in x
Nx_init = 10  # number of intially habitable patches in x
Nt = 10  # number of generational iterations

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
    for x in habitat["x"]:  # iterate through patches
        sComp = sum(habitat["pComp"][x])  # Sum of competitiveness of all individuals of given patch
        indices_to_die = []
        for i in range(habitat["num of animals"][x]):  # iterate through individuals in a patch
            print(i)
            print(habitat["pRep"][x])
            lam = habitat["pRep"][x][i] * R  # lambda value for Poisson distribution
            
            pComp = habitat["pComp"][x][i]
            surv_prob = min(K * pComp / sComp, 1)  # probability of survival to next generation
            
            surv_ran = np.random.random()
            if surv_ran < surv_prob:
                # animal dies
                indices_to_die.append(i)
#                habitat["num of animals"][x] -= 1
#                del habitat["pRep"][x][i]
#                del habitat["pComp"][x][i]
#                del habitat["pDisp"][x][i]
            else:
                # animal reproduces 
                # Parental traits
                pRep = habitat["pRep"][x][i]
                pComp = habitat["pComp"][x][i]
                pDisp = habitat["pDisp"][x][i]
                num_offspring = np.random.poisson(lam=lam)
                habitat["num of animals"][x] += num_offspring
                for offspring in range(num_offspring):
                    mut_ran = np.random.random()
                    if mut_ran < m:
                        # mutate one of the traits
                        trait_ran = np.random.randint(0, 3)
                        mut_mag_ran = np.random.uniform(-m_m, m_m)
                        if trait_ran == 0:
                            # mutate pRep
                            pRep_new = min(max(pRep + mut_mag_ran, 0), 1)
                            trait_change = pRep_new - pRep
                            pComp_new = pComp - (trait_change * pComp) / (pComp + pDisp)
                            pDisp_new = pDisp - (trait_change * pDisp) / (pComp + pDisp)
                        elif trait_ran == 1:
                            # mutate pComp
                            pComp_new = min(max(pComp + mut_mag_ran, 0), 1)
                            trait_change = pComp_new - pComp
                            pRep_new = pRep - (trait_change * pRep) / (pRep + pDisp)
                            pDisp_new = pDisp - (trait_change * pDisp) / (pRep + pDisp)
                        else:
                            pDisp_new = min(max(pDisp + mut_mag_ran, 0), 1)
                            trait_change = pDisp_new - pDisp
                            pComp_new = pComp - (trait_change * pComp) / (pRep + pComp)
                            pRep_new = pRep - (trait_change * pRep) / (pRep + pComp)                        
                    else:
                        # Offspring directly inherit parental traits
                        pRep_new = pRep
                        pComp_new = pComp
                        pDisp_new = pDisp
                    habitat["pRep"][x].append(pRep_new)
                    habitat["pComp"][x].append(pComp_new)
                    habitat["pDisp"][x].append(pDisp_new)
        for i in sorted(indices_to_die, reverse=True):
            habitat["num of animals"][x] -= 1
            del habitat["pRep"][x][i]
            del habitat["pComp"][x][i]
            del habitat["pDisp"][x][i]
                
    # disperse with probability pDisp into one of 2 surrounding patches.
    for x in habitat["x"]:  # iterate through patches
        indices_to_die = []
        for i in range(habitat["num of animals"][x]):  # iterate through individuals in a patch
            disp_ran = np.random.random()
            pDisp = habitat["pRep"][x][i]
            print("pDisp = ", pDisp)
            print("pDisp_ran = ", disp_ran)
            if disp_ran < pDisp:
                # disperse
                if np.random.random() < 0.5:
                    # disperse left
                    print("disperse left")
                    habitat["num of animals"][x - 1] += 1
                    habitat["pRep"][x - 1].append(habitat["pRep"][x][i])
                    habitat["pComp"][x - 1].append(habitat["pComp"][x][i])
                    habitat["pDisp"][x - 1].append(habitat["pDisp"][x][i])
                else:
                    # disperse right
                    print("disperse left")
                    habitat["num of animals"][(x + 1) % Nx] += 1
                    habitat["pRep"][(x + 1) % Nx].append(habitat["pRep"][x][i])
                    habitat["pComp"][(x + 1) % Nx].append(habitat["pComp"][x][i])
                    habitat["pDisp"][(x + 1) % Nx].append(habitat["pDisp"][x][i])
                indices_to_die.append(i)
        print("itd = ", indices_to_die)
        for i in sorted(indices_to_die, reverse=True):
            # remove from previous patch
            habitat["num of animals"][x] -= 1
            del habitat["pRep"][x][i]
            del habitat["pComp"][x][i]
            del habitat["pDisp"][x][i]
                
# Looks like class for each animal would be better.

pRep_array = np.empty(0)
for x in habitat["x"]:
    for i in range(habitat["num of animals"][x]):
        print("this is " + str(habitat["pRep"][x][i]))
        pRep_array = np.append(pRep_array, habitat["pRep"][x][i])
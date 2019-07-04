import numpy as np
from scipy import stats

# SMALL LOOP
def single_run(capital, token):
    # Initialize local variables
    capital_path = np.array([capital]) # Initialize Numpy array to record a given path, first element is equal to capital
    while capital > 0:
        if np.random.uniform(0,1) > 0.97297297297:
            capital=capital+(token*36)
            capital_path=np.append(capital_path,[capital])
        else: 
            capital=capital-token
            capital_path=np.append(capital_path,[capital])
    return (capital_path) 
    
# CONSTANTS
capital=100 # Initial capital
token=2 # Color tokens notional - used for betting on roulette's single numbers
mc_sim = 90 # Number of required MC simulation of the process

# BIG LOOP
glob_cap_path=np.ndarray(shape=(mc_sim,1))
size_distrib=np.ndarray(shape=(mc_sim,1))
max_distrib=np.ndarray(shape=(mc_sim,1))
std_distrib=np.ndarray(shape=(mc_sim,1))

for i in range(0,mc_sim):
    glob_cap_path = single_run(capital, token) #Assigning output from the `single_run` function 
    size_distrib[i]=np.size(glob_cap_path)
    #max_distrib[i]=np.max(glob_cap_path)
    std_distrib[i]=np.std(glob_cap_path)
    

print("Mediana Odchylenia Standardowego: ")
print(stats.mode(std_distrib))

#print("Mediana Maksymalnych Wartosci:")
#print(stats.mode(max_distrib))

print("Mediana Iteracji Gry: ")
print(stats.mode(size_distrib))



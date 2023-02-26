# Code to create the importance frequency plot for Tabular results

# SETUP -----------------------------------------------

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Setup Repository
with open("repo_info.txt", "r") as repo_info:
    path_to_repo = repo_info.readline()
  
print(path_to_repo)

path_to_data = f"{path_to_repo}data/"
path_to_raw = f"{path_to_data}raw/"
path_to_processed = f"{path_to_data}processed/"
path_to_lda = f"{path_to_data}lda/"
path_to_icd = f"{path_to_data}icd_codes/"
path_to_models = f"{path_to_repo}models/"
path_to_results = f"{path_to_repo}results/"
path_to_figures = f"{path_to_repo}figures/"

os.makedirs(path_to_figures, exist_ok=True)

# 1. LOAD THE DATASET -------------------------------------------------

# Load the dataset
imp = pd.read_excel(f'{path_to_results}tabular/importance_frequency.xlsx')

# Keep only the first 20 variables
imp = imp.head(20)

# Rename the columns and keep only relevant ones
imp = imp[['Unnamed: 0', 'percent']]
imp.columns = ['variable', 'percent']

# define a function that saves figures
def save_fig(fig_id, tight_layout=True):
    # The path of the figures folder ./Figures/fig_id.png (fig_id is a variable that you specify 
    # when you call the function)
    path = os.path.join(fig_id + ".png") 
    print("Saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format='png', dpi=300)

imp.plot(x="variable", y="percent", kind="barh", figsize = (12,12), legend = False).invert_yaxis()
plt.title(f'Relative Feature Importance', fontsize = 20)
plt.ylabel("")
plt.yticks(fontsize = 15)
plt.xticks(fontsize = 15)
save_fig(f'{path_to_figures}figure_2_featimp_tabular')
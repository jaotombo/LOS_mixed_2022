# Code to get CSVs of the Top 20 LDA features used in our Mixed Models

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
path_to_tables = f"{path_to_repo}tables/"

os.makedirs(path_to_tables, exist_ok=True)

# 1. LOAD THE DATASET -------------------------------------------------

iter_dict = {'spacy':
             {'frequency': ['F268', 'F240', 'F180', 'F88', 'F60', 'F174', 'F16', 'F101', 'F87', 'F86', 'F251']
              ,'onehot': ['F258', 'F27', 'F184', 'F81', 'F232', 'F163', 'F284', 'F80', 'F279', 'F277']
              ,'tf_idf': ['F59', 'F205', 'F198', 'F122', 'F123', 'F233','F121']}
              ,'stemming':
              {'frequency': ['F274', 'F87', 'F195', 'F32', 'F242', 'F92', 'F219', 'F294']
               ,'onehot': ['F99', 'F43', 'F27', 'F255', 'F286', 'F210', 'F12', 'F141', 'F202']
               ,'tf_idf': ['F1', 'F123', 'F162', 'F57', 'F60', 'F21']}}

for key, value in iter_dict.items():
    for method, topics in value.items():
        # Load the dataset
        imp = pd.read_excel(f'{path_to_results}{key}/output_lda_{key}.xlsx', sheet_name=f'{method}')
        store = []
        for i in topics:
            df = pd.DataFrame(imp.sort_values(by = [i], ascending=False)['Unnamed: 0'].head(20))
            df.columns = [i]
            store.append(df.reset_index(drop = True))
        store = pd.concat(store, axis = 1)
        store.to_csv(f'{path_to_tables}top_20{key}{method}.csv')
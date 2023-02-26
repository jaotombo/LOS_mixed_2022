# Code to create the importance frequency plot for Tabular results
# Creates tables for Appendix 1 and Appendix 2


# SETUP -----------------------------------------------

import os
import pandas as pd
import numpy as np
from tqdm import tqdm

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

# 1. LOAD THE DATA -----------------------------------------------------------------

df = pd.read_csv(f"{path_to_processed}df_mixed_discharge.csv.gzip", compression = 'gzip')

# drop the variables to be exempted from the analysis and rename new dataset
df = df.drop(columns = ['hadm_id', 'subject_id','icu_los'])

# Transform the LOS timedelta to days (as decimal values to increase precision)
df['los'] = pd.to_timedelta(df.los)
df['los'] = df.los/pd.to_timedelta(1, unit='D')

# selection criterion : only patients 18 and older and with a length of stay or 1 day or greater
df = df.loc[(df['age']>=18) & (df['los']>=1),:]
# check proportion of missing values
missing = pd.DataFrame(df.isna().mean(), columns = ['proportions'])
missing.sort_values('proportions',ascending = False)
# drop variables having more than 20 % missing values
print(f"Variables with more than 20% Missing Values: {list(missing.loc[missing.proportions >= 0.2].index)}")
df = df.drop(columns=missing.loc[missing.proportions >= 0.2].index)
# impute missing values
df = df.interpolate()
df.isna().mean()

# compute Lower and Upper Fence according to Tukey's criteria
y = df['los']
Q1 = np.percentile(y, 25)
Q3 = np.percentile(y, 75)
IQR = Q3-Q1
LF = Q1 - 1.5*IQR
UF = Q3 + 1.5*IQR
print(f'First quartile = {Q1:.3f}, Third Quartile = {Q3:.3f}, Interquartile Interval = {IQR:.3f}')
print(f'Lower Fence = {LF:.3f}, Upper Fence = {UF:.3f}')
# create categorical LOS variable where prolonged LOS is any value greater than Upper Fence
df['los_cat'] = df['los']> UF

# Select numerical and categorical columns
cat_cols = df.drop(columns = ['text']).select_dtypes(['object', 'bool']).columns.tolist()
num_cols = df.select_dtypes(['int64', 'float64']).columns.tolist()

# Calculate the LOS Split
val1 = df.loc[(df.los_cat == True)].shape[0]
val2 = df.loc[(df.los_cat == False)].shape[0]
tot = val1 + val2
perc1 = round(val1/tot*100,2)
perc2 = round(val2/tot*100,2)


# 2. EDA: Descriptive Statistics (APPENDIX 1) ---------------------------------------------------------

store = [['LOS (Binary)', "", f"{int(val1)} ({perc1}%)", f"{int(val2)} ({perc2}%)"]]
for col in tqdm(cat_cols):
    if col == 'los_cat': continue
    count_mod = 0
    for mod in df[col].unique().tolist():
        # Now compute the descriptive table
        sub = df.loc[df[col] == mod]
        val1 = sub.loc[(sub.los_cat == True)].shape[0]
        val2 = sub.loc[(sub.los_cat == False)].shape[0]
        tot = val1 + val2
        perc1 = round(val1/tot*100,2)
        perc2 = round(val2/tot*100,2)
        if count_mod == 0:
            store.append([col, mod, f"{int(val1)} ({perc1}%)", f"{int(val2)} ({perc2}%)"])
        else:
            store.append(["", mod, f"{int(val1)} ({perc1}%)", f"{int(val2)} ({perc2}%)"])
        count_mod += 1
        
store = pd.DataFrame(store, columns = ['Variable', 'Modality', 'PLOS', 'RLOS'])

store.to_csv(f"{path_to_tables}descriptive_stat_categorical.csv", index = False)

# Now do the same for the numerical variables
store = []
for col in tqdm(num_cols):

    # Now compute the descriptive table
    mean1 = df.loc[(df.los_cat == True)][col].mean()
    std1 = df.loc[(df.los_cat == True)][col].std()
    mean2 = df.loc[(df.los_cat == False)][col].mean()
    std2 = df.loc[(df.los_cat == False)][col].std()

    store.append([col, f"{round(mean1,2)} ({round(std1,2)})", f"{round(mean2,2)} ({round(std2,2)})"])
        
store = pd.DataFrame(store, columns = ['Variable', 'PLOS', 'RLOS'])

store.to_csv(f"{path_to_tables}descriptive_stat_numerical.csv", index = False)


# 3. BASELINE CODE (APPENDIX 2) --------------------------------------------------------------

# BASELINE WITH A PRIORI DISTRIBUTION

perc = df.los_cat.value_counts()[True]/df.shape[0]

tot_plos = df.loc[df.los_cat].shape[0]
tot_rlos = df.loc[df.los_cat == False].shape[0]

TN = tot_rlos*(1-perc)
FP = tot_rlos*perc
FN = tot_plos*(1-perc)
TP = tot_plos*perc

matrix = [[TN, FP],[FN, TP], [TN+FN, FP+TP]]
pd.DataFrame(matrix)

acc = (TP+TN)/(TP+TN+FP+FN)

prec = TP/(TP+FP)
recall = TP/(TP+FN)

f1 = TP/(TP+(FP+FN)/2)


# UNIFORM DISTRIBUTION BASELINE


perc = 0.5

TN = tot_rlos*(1-perc)
FP = tot_rlos*perc
FN = tot_plos*(1-perc)
TP = tot_plos*perc

matrix = [[TN, FP],[FN, TP], [TN+FN, FP+TP]]
pd.DataFrame(matrix)

acc = (TP+TN)/(TP+TN+FP+FN)

prec = TP/(TP+FP)
recall = TP/(TP+FN)


f1 = TP/(TP+(FP+FN)/2)
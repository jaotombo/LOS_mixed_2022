# Code to create the importance frequency plot for Tabular results
# And the figures from the LIME feature importance for all the Text Predictors

# SETUP -----------------------------------------------

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle

# Setup Repository
with open("codes/repo_info.txt", "r") as repo_info:
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

# Set to True if we want to include deaths
death_incl = False
death_tag = np.where(death_incl,"_death", "")


# 1. TABULAR FEATURE IMPORTANCE -------------------------------------------------

# Load the dataset
imp = pd.read_excel(f'{path_to_results}tabular/importance_frequency{death_tag}.xlsx')

# Keep only the first 20 variables
# Show the top 20 negative and positive values
# using the top 20 in absolute value
imp['imp_abs'] = imp.importance.apply(lambda x: abs(x))
# Order them by absolute importance
imp.sort_values(by = ['imp_abs'], ascending=False, inplace = True)

imp = imp.head(20)

# Rename the columns and keep only relevant ones
imp = imp[['Unnamed: 0', 'percent', 'importance']]
imp.columns = ['variable', 'percent', 'importance']

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
save_fig(f'{path_to_figures}figure_2_featimp_tabular_perc{death_tag}')

# Do also one with the raw feature importance
imp.plot(x="variable", y="importance", kind="barh", figsize = (12,12), legend = False).invert_yaxis()
plt.title(f'Raw Feature Importance', fontsize = 20)
plt.ylabel("")
plt.yticks(fontsize = 15)
plt.xticks(fontsize = 15)
save_fig(f'{path_to_figures}figure_2_featimp_tabular_raw{death_tag}')

# 2. LIME FEAT IMPORTANCE ---------------------------------------------------------------------------------------------------

# Iterate over our main methods of vectorization

vect_dict = {'stemming': (False, False),
             'spacy': (True, True)}

             
for key, value in vect_dict.items():
    print(key)
    # PARAMETERS

    lemmatize = value[0] # set to false if we want to do stemming
    lemma_tag = str(np.where(lemmatize, "_lemma",""))
    spacy = value[1]

    if spacy: 
        lemma_tag = str(np.where(lemmatize, "_lemma_spacy",""))

    preprocessing = True # set to true if we want to clean and perform some preprocessing
    preproc_heavier = True # set to True if we want a heavier preprocessing
    preproc_tag_2 = np.where(preproc_heavier, '_heavier', '')
    preproc_tag = np.where(preprocessing, f'_preproc{preproc_tag_2}', f'{preproc_tag_2}')

    # load weights
    try :
        with open(f'{path_to_data}feature_importance/text_only_weights{preproc_tag}{lemma_tag}{death_tag}.pkl', 'rb') as handle:
            weights = pickle.load(handle)
            print('Weights loaded')
            print(len(weights))
    except :
        weights = [] # initialize an empty dictionary if no existing file is present
        print('New Weight List')
    # load labels
    try :
        with open(f'{path_to_data}feature_importance/text_only_labels{preproc_tag}{lemma_tag}{death_tag}.pkl', 'rb') as handle:
            labels = pickle.load(handle)
            print('Label Loaded')
            print(len(labels))
    except :
        labels = [] # initialize an empty dictionary if no existing file is present
        print('New Label List')

    # Now we process the list of labels and weights
    words = [word for single_list in labels for word in single_list]
    print(len(words))
    words = list(set(words)) # get unique values
    len(words)
    # Get a dictionary of words
    dict_of_words = {i:0 for i in words}

    # And get the correct weights
    for count, single_list in enumerate(weights):
        for i, weight in enumerate(single_list):
            dict_of_words[labels[count][i]] += weight

    # Transform everything to a pandas dataframe
    weight_df = pd.DataFrame([dict_of_words.keys(), dict_of_words.values()]).T
    weight_df.columns = ['word', 'weight']
    weight_df['weight'] = weight_df.weight.astype(int)
    weight_df['abs_weight'] = weight_df.weight.apply(lambda x: abs(x))

    # sort values by absolute mean - and get only the top 30 words by absolute value
    abs_mean = weight_df.sort_values('abs_weight', ascending = False).head(30)
    abs_mean.weight = abs_mean.weight/len(weights)
    abs_mean.abs_weight = abs_mean.abs_weight/len(weights)
    # normalize by 100%
    abs_mean.abs_weight = abs_mean.abs_weight/abs_mean.abs_weight.max()*100
    abs_mean = abs_mean.sort_values('abs_weight', ascending = True)

    #Plot abs mean --------------------------------------------------
    fig, ax = plt.subplots(nrows=1, ncols=1,figsize=(10,15))

    y_ticks = range(len(abs_mean))
    y_labels = abs_mean.word
    plt.barh(y=y_ticks,width=abs_mean.abs_weight)

    plt.yticks(ticks=y_ticks,labels=y_labels,size= 15)
    plt.title('LIME Weights - Average Absolute Values of Test Set Explanations')
    plt.ylabel('')
    plt.xlabel('Mean |Weight|',size=20)

    plt.savefig(f"{path_to_repo}figures/lime_{preproc_tag}{lemma_tag}{death_tag}", bbox_inches='tight')
    plt.show()

    #Plot the raw mean --------------------------------------------------
    fig, ax = plt.subplots(nrows=1, ncols=1,figsize=(10,15))

    abs_mean.sort_values('weight', ascending = True, inplace = True)

    y_ticks = range(len(abs_mean))
    y_labels = abs_mean.word
    plt.barh(y=y_ticks,width=abs_mean.weight)

    plt.yticks(ticks=y_ticks,labels=y_labels,size= 15)
    plt.title('LIME Weights - Average Raw Values of Test Set Explanations')
    plt.ylabel('')
    plt.xlabel('Mean Weight',size=20)

    plt.savefig(f"{path_to_repo}figures/lime_{preproc_tag}{lemma_tag}{death_tag}_raw", bbox_inches='tight')
    plt.show()
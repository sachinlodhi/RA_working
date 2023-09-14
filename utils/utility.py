import pandas as pd
import re
import  os
import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import OrdinalEncoder
import warnings
import math
import shutil
import glob
from .cleaner import clean
from .transform import cat_df, fix_missing, encode, impute
from .graph import corr_mat_cat, corr_mat_ord, scatter_plt, freq_graph

warnings.filterwarnings('ignore')

read_func ={
    ".csv" : pd.read_csv,
    ".xls" : pd.read_excel
}

# attributes exteractor
def load_file(filename):
    global read_func
    df = read_func[filename[-4:]](filename)
    return df.columns.tolist()


# This filters out the attrs automatically(predefined)
def filter_personal(attributes):
    words_to_filter = ["email", "name", "cwid"]

    # Create a regex pattern that matches any of the words in a case-insensitive manner
    pattern = re.compile(r"|".join(re.escape(word) for word in words_to_filter), re.IGNORECASE)

    # Filter the list to get elements that match the pattern
    filtered_list = [word for word in l if pattern.search(word)]

    # Print the filtered list
    # print(filtered_list)


# this function removes the columns baesd on the user selection
def filter_cols(all_cols, selected_cols):
    return [i for i in all_cols if i not in selected_cols]

# assigning the serial number and creating another file to save record
def mapping(filename):
    df = read_func[filename[-4:]](filename)

    # Assigning Serial Nos to all the recs
    df["Sr. No."] = pd.Series(range(1, len(df)+1))
    main_df_len = len(df)

    # creating 5 digits unique numbers

    unique_digits = set()
    while True:
        unique_digits.add(random.randint(10000, 99999))
        if len(unique_digits) == main_df_len:
            break
    map_df = pd.DataFrame()
    map_df["Sr. No."] = df["Sr. No."]
    map_df["uid"] = list(unique_digits)
    _, file_extension = os.path.splitext(filename)
    map_df.to_csv(_ +"_mapping.csv",index=False)
    print("Success Mapping")

# loading  the df and starting further process
def begin(filename):
    # read csv file here
    global read_func
    freq_graphs =[]
    scatter_plots = []
    ord_corr_mat = []
    cat_corr_mat = []
    rec = read_func[filename[-4:]](filename) # read the file according to its extension
    rec1 = rec.copy()
    # print(rec.head())

    # 1. returns the column with the removed attrs
    rec = clean(rec)
    print("Attrs removed")
    # 2. send the rec for imputation
    rec = fix_missing(rec)
    print("Impuatation Done")

    # 3. draw freq graph for the EDA
    freq_graphs = freq_graph(rec)
    print('Frequency graph done')

    #4. draw scatter plot
    scatter_graphs = scatter_plt(rec)
    print("sactter plot done")


    # 5. Encode the data
    rec = encode(rec) # returns rec with ordinal attrs
    print("encode done")

    #6. plot the correlation matrix for ordinal data
    ord_corr_mat = corr_mat_ord(rec)
    print("ordinal heatmap plotted")
    # 7. get the three copies for the categorical dataframe
    df_chi, df_pVal, df_cramer  = cat_df(rec1) # sending unaltered dataframe
    print("data frames prepared")
    #8. graphing the 3 heatmaps
    corr_mat_cat(rec1, df_chi, df_pVal, df_cramer)
    print("categorical heatmap plotted")














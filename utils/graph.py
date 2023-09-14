import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import OrdinalEncoder
import warnings
import random
import researchpy as rp
import os
import math
import glob

save_dir = "static/graphs"

# plotting the graphs
def freq_graph(rec):
    try:
        os.makedirs("static/graphs/"+"frequency_graphs")
    except:
        pass

    '''Plotting frequency graph for the dataframe and dsiplaying image'''

    attributes_to_plot = list(rec.columns.values)
    # print(len(attributes_to_plot))
    num_rows = math.ceil(len(attributes_to_plot) / 5)
    num_cols = 5

    # Frequency graphs
    for i in attributes_to_plot:
        frequency_counts = rec[i].value_counts().sort_index()
        plt.figure(figsize=(10, 6))  # Set the figure size
        frequency_counts.plot(kind='bar', color='skyblue')
        plt.xlabel('Unique Values')  # X-axis label
        plt.ylabel('Frequency')  # Y-axis label
        plt.title(f'Frequency Distribution of {i}')
        plt.xticks(rotation=45)
        plt.grid(axis='y')
        # plt.show()  # Show the plot
        plt.savefig(save_dir+'/frequency_graphs/' +i+".svg",format='svg', dpi=1200)
    # print("Freq distr saved")
    freq_lis = glob.glob(save_dir+"/frequency_graphs/" + "*.svg")
    return freq_lis # lists of the images

def scatter_plt(rec):
    # # scatter plot
    # Create a list to store the scatter plots
    try:
        os.makedirs("static/graphs/" + "scatter_graphs")
    except:
        pass
    scatter_plots = []
    attributes_to_plot = list(rec.columns.values)
    num_rows = math.ceil(len(attributes_to_plot) / 5)
    num_cols = 5

    # Loop through each attribute and create scatter plots
    for i, attribute in enumerate(attributes_to_plot):
        row = i // num_cols
        col = i % num_cols
        plt.figure(figsize=(10, 8))  # Set the figure size
        sns.scatterplot(x=attribute, y='Grade', data=rec)
        plt.xlabel(attribute)
        plt.ylabel('Grade')
        plt.title(f'{attribute} vs. Grade')
        plt.xticks(rotation=45)  # Rotate x-axis labels if needed
        # Append the current plot to the list of scatter plots
        scatter_plots.append(plt)
        plt.savefig(save_dir + '/scatter_graphs/' + attribute + ".svg",format='svg', dpi=1200)
    scatter_lis = glob.glob(save_dir + "/scatter_graph/" + "*.svg")
    return scatter_lis


# 6. function to draw graph using the ordinal data
def corr_mat_ord(rec):
    correlation_matrix = rec.corr()
    try:
     os.makedirs("static/graphs/" + "heatmaps")
    except:
        pass

    # Create a heatmap of the correlation matrix
    plt.figure(figsize=(30, 30))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=.5,)
    plt.title("Correlation Matrix Heatmap(ORDINAL CONSIDERATION OF ATTRIBUTES)")
    plt.savefig(save_dir + "/heatmaps/" + "ordinal.svg",format='svg', dpi=1200)
    # plt.show()
    ord_heatmap = glob.glob(save_dir + "/heatmaps/" + "ordinal.svg")
    return ord_heatmap

#8. function to draw graph with the consideration of the data as categorical
def corr_mat_cat(rec, df_chi, df_pVal, df_cramer):
    try:
        os.makedirs("static/graphs/" + "heatmaps")
    except:
        pass

    attribute_labels = list(rec.columns.values)
    dfs = {'chi': df_chi, "pVal": df_pVal, "cramer": df_cramer}

    cat_heatmap = []
    for i in dfs:
        data = dfs[i].iloc[1:, 1:].astype(float)

        # print(len(attribute_labels))
        # Create a heatmap using seaborn
        plt.figure(figsize=(30, 30))  # Adjust the figure size as needed
        sns.heatmap(data, annot=True, cmap='coolwarm', linewidths=0.5, xticklabels=attribute_labels,
                    yticklabels=attribute_labels)

        plt.title(f'{i} value correlation matrix')
        plt.savefig(save_dir + "/heatmaps/" + str(i) +".svg", format='svg', dpi=1200)
        cat_heatmap.append(save_dir + "/heatmaps/" + str(i) +".svg")
        # plt.show()
    return cat_heatmap



import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import OrdinalEncoder
import warnings
import random
import researchpy as rp

# helper function for "fix_missing" function
def impute(rec, attr, val_to_handle):

    dstrbn = rec.groupby(attr)['Grade'].value_counts().unstack().fillna(0)

    rec.loc[rec[attr] == val_to_handle, attr] = ''
    temp_df = rec[['Grade', attr]].copy()
    temp_df = temp_df[temp_df[attr] != '']
    dstrbn = temp_df.groupby('Grade')[attr].value_counts().unstack().fillna(0)


    # finding most frequent values for each grade(storing in dictionary) from Parent level edu attr
    most_fr_vals = {}
    # Iterate through unique values in the "Grade" column
    for grade_value in temp_df['Grade'].unique():
        # Filter the DataFrame for the current grade value
        filtered_df = temp_df[temp_df['Grade'] == grade_value]
        # Find the most frequent value in the "Parent level edu" column for this grade value
        most_frequent = filtered_df[attr].mode().iloc[0]
        # Store the result in the dictionary
        most_fr_vals[grade_value] = most_frequent

    key_lis = list(most_fr_vals.keys())

    # updating the empty value
    for idx, row in rec.iterrows():
        if row[attr] == "":
            # print(row["Grade"])
            grade = row["Grade"][0]  # A+, A-, B+, B- are considered same no impact of sign here
            # print(most_frequent_values[grade])
            try:  # try getting the grade and corresponding most freq attr val
                rec.at[idx, attr] = most_fr_vals[grade]
            except  KeyError:  # if the jey is not availabe in the dictionary
                random_key = key_lis[random.randint(0, len(key_lis) - 1)]
                rec.at[idx, attr] = most_fr_vals[random_key]

    return rec


'''
2. Function to handle the "unkonwn" and "Data Change" values in different columns
'''
def fix_missing(rec):
    # 1. underrepresented : replacing Unknown values based on the ferequency of YES/NO for each grade,
    # i.e. if df["underrepresented"] == Unknown then get corresponding df["Grade"]and find df.underrepresented[max(Yes,No)] and assign that value

    missing_rows = rec['underrepresented'].isin(['Unknown'])
    # Finding distribution for each value so Unknown values can be imputed
    dstrbn = rec.groupby('underrepresented')['Grade'].value_counts().unstack().fillna(0)

    grades = ["A+", "A", "A-", "B-", "B", "B+", "C", "D", "F"]
    for grade in grades:
        if dstrbn[grade][0] >= dstrbn[grade][2]:
            rec.loc[(rec['Grade'] == grade) & (rec['underrepresented'] == 'Unknown'), 'underrepresented'] = 'No'
        else:
            rec.loc[(rec['Grade'] == grade) & (rec['underrepresented'] == 'Unknown'), 'underrepresented'] = 'Yes'

    for i in ["Admit Type", "Parent level edu"]:
        rec = impute(rec, i, "Unknown")

    # Program Action missing val handle
    rec = impute(rec, "Program Action", "Data Change")

    return rec


# 4. function to encode the data into the ordinal values
def encode(rec):
    # encoding Grade oridinally
    grade_mapping = {'A+': 7, 'A': 6, 'A-': 5, 'B+': 4, 'B': 3, 'B-': 2, 'C': 1, 'D': 0, 'F': -1}
    # Encode the "Grade" column
    rec['Grade'] = rec['Grade'].map(grade_mapping)
    # Calculate the correlation matrix
    correlation_matrix = rec["Grade"].corr(rec["GPA"])


    # encoding First Generation Attr(ordinal)
    rec['First Generation'] = rec['First Generation'].map({'Yes': 1, 'No': 0})
    corr_mat = rec["Grade"].corr(rec["First Generation"])


    # UNderrepresented : Ordinal Yes:0 and No: 1
    rec['underrepresented'] = rec['underrepresented'].map({"No": 0, "Yes": 1})

    # Graduated -> 0%(0) or 100%(1)
    rec["Graduated"] = rec["Graduated"].map({"0%     (0)": 0, "100%     (1)": 1})
    rec["Not Graduated Not Enrolled"] = rec["Not Graduated Not Enrolled"].map({"0%     (0)": 0, "100%     (1)": 1})
    rec["Enrolled Not Graduated"] = rec["Enrolled Not Graduated"].map({"0%     (0)": 0, "100%     (1)": 1})

    # Academic Career: Ordinal-> based on EDA: scatter plot has the more Better grades for PostBac
    # rec["Postbaccalaureate"] = 1, rec["Undegraduate"] = 0
    rec["Academic Career"] = rec["Academic Career"].map({"Undergraduate": 0, "Postbaccalaureate": 1})

    '''Admit type : Ordinal; According to scatter plot GRAD/PB students are likely to get better grades> UG> First Time Freshman
    rec['First-Time Freshmen'] = 0
    rec['Grad/PB'] = 2
    rec['UG Transfer'] = 1
    '''
    rec["Admit Type"] = rec["Admit Type"].map({"First-Time Freshmen": 0, "UG Transfer": 1, "Grad/PB": 2})

    '''
    Cohort: Ordinal -> According to scatter plot:
    rec['Graduated'] = 2
    rec['Enrolled Not Graduated'] = 1
    rec['Not Graduated Not Enrolled'] = 0
    '''
    rec["Cohort Type"] = rec["Cohort Type"].map(
        {"Not Graduated Not Enrolled": 0, "Enrolled Not Graduated": 1, "Graduated": 2})
    '''
    Class: Ordinal -> According to scatter plot:
    rec['CPSC~597~02'] = 1
    rec['CPSC~483~01'] = 0
    rec['CPSC~598~01'] = DONT USE>>>> OUTLIER
    '''
    rec["Class"] = rec["Class"].map({"CPSC~483~01": 0, "CPSC~597~02": 1})

    '''
    Parent Level edu ; Ordinal(Loosely) as from scatter plot there is not direct pattern
    '''
    rec["Parent level edu"] = rec["Parent level edu"].map(
        {"Student is First Generation College": 0, "Parent Attended Some College": 1, "Parent Graduated College": 2})
    rec["Program Status"] = rec["Program Status"].map({"Active in Program": 0, "Completed Program": 1})
    rec["Program Action"] = rec["Program Action"].map(
        {"Completion of Program": 1, "Plan Change": 0, "Matriculation": 2})
    rec["Major at Entry"] = rec["Major at Entry"].map(
        {"*Computer Science    Minor 1BA": 2, "Comm/Public Relations  2MJ 1BA": 1, "Undegrad Undeclared    1MJ 1BA": 1,
         "Electrical Engineering 1MJ 1BS": 0, "Biological Science    1MJ 1BA": 0})
    return rec







'''
function for generating the df for chi, p, and crmaer's value 

'''

# 8. for taking raw df and creating 3 empty dfs for heatmap of cramer, chi and pVal
def cat_df(rec): # takes full and unfiltered dataframe and returns 3 empty df
    attrs_lst = list(rec.columns.values)
    attrs_len = len(attrs_lst)
    size = attrs_len + 1
    df = pd.DataFrame(index=range(size), columns=range(size))
    # first col assignment
    df.iloc[1:, 0] = attrs_lst[0:]

    # first row assignment
    df.iloc[0, 1:] = attrs_lst[0:]

    # zero filling
    df.iloc[1:, 1:] = 0

    df_cramer = df.copy(deep=True)  # to save the cramer's val
    df_chi = df.copy(deep=True)  # to save chi val
    df_pVal = df.copy(deep=True)  # to save p value

    for i in range(len(attrs_lst)):
        # print(attrs_lst[i])
        for j in range(len(attrs_lst)):
            cramer_v = rp.crosstab(rec[attrs_lst[i]], rec[attrs_lst[j]], prop='cell', test='chi-square')
            # print(cramer_v[1]["results"][2]) #Cramer's V
            # print(cramer_v[1]["results"][2], end=" ")
            df_chi[i + 1][j + 1] = cramer_v[1]["results"][0]
            df_pVal[i + 1][j + 1] = cramer_v[1]["results"][1]
            df_cramer[i + 1][j + 1] = cramer_v[1]["results"][2]

    return [df_chi, df_pVal, df_cramer]


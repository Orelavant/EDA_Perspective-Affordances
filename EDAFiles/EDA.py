# Imports
import pandas as pd
import numpy as np
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt
sns.set(color_codes=True)
sns.set(style='ticks')

# Read-in.
avatarRaw = pd.read_csv("PT_Avatar_Raw.csv")
cylinderRaw = pd.read_csv("PT_Cylinder_Raw.csv")

# Cleaning up data by removing participants
# Shows rows with NaN: avatarRaw[avatarRaw["Response_Time"].isnull()]
# Removing “Can’t Reach” trials, response times < 200 ms, and response times 3 SD above and below mean.
# Type: avatar or cylinder
def cleanData(dataframe, type):
    # Creating duplicate to preserve original
    cleanDF = dataframe

    # If type avatar, drop participant 9, and other specifics.
    if type == "avatar":
        cleanDF.drop(cleanDF[cleanDF["Participant"] == 9].index, inplace=True)
        cleanDF.drop(columns=["Acc_dc"], inplace=True)

    # If type cylinder, drop specifics.
    if type == "cylinder":
        cleanDF.drop(columns=["%CanReach", "Accuracy_dc"], inplace=True)

    # Remove any NaNs
    cleanDF.dropna(inplace=True)

    # Removing Accuracy and Acc_dc column (96-99% accuracy rate)
    cleanDF.drop(columns=['Accuracy'], inplace=True)

    # Dropping rows with "Can't reach" as a response
    cleanDF.drop(cleanDF[cleanDF["Response"] == "Can't Reach"].index, inplace=True)

    # Converting response time to floats
    cleanDF["Response_Time"] = cleanDF["Response_Time"].astype(float)

    # Dropping response times < 200ms
    cleanDF.drop(cleanDF[cleanDF["Response_Time"] < .2].index, inplace=True)

    # Dropping response times 3 std devs outside of the mean
    # Source: https://kite.com/python/answers/how-to-remove-outliers-from-a-pandas-dataframe-in-python
    z_scores = stats.zscore(cleanDF["Response_Time"])
    abs_z_scores = np.abs(z_scores)
    filtered_entries = (abs_z_scores < 3)
    cleanDF = cleanDF[filtered_entries]

    return cleanDF

# Assigning newDFs names
avatarClean = cleanData(avatarRaw, "avatar")
cylinderClean = cleanData(cylinderRaw, "cylinder")


# Plots

# TODO: Compare ball rotation & response times across the two studies
# Barplots of response time over ball rotation
# sns.barplot(x=avatarClean['Ball_Rotation'], y=avatarClean["Response_Time"], hue=avatarClean['Chair_Type']).set_title('Avatar: Ball Rotation & Response Time')
# plt.show()
# sns.barplot(x=cylinderClean['Ball_Rotation'], y=cylinderClean["Response_Time"], hue=cylinderClean['Chair_Type']).set_title('Cylinder: Ball Rotation & Response Time')
# plt.show()

# Barplots of response time over ball distance
# sns.barplot(x=avatarClean['Ball_Distance'], y=avatarClean["Response_Time"], hue=avatarClean['Chair_Type']).set_title('Avatar: Ball Distance & Response Time')
# plt.show()
# sns.barplot(x=cylinderClean['Ball_Distance'], y=cylinderClean["Response_Time"], hue=cylinderClean['Chair_Type']).set_title('Cylinder: Ball Distance & Response Time')
# plt.show()

# Testing
# print(avatarClean["Response_Time"].mean())
# print(avatarClean["Response_Time"].std())
# print(avatarClean.dtypes)
# print(avatarClean.isnull().sum())
# print(avatarClean.head(11))


# Qualtrics Data

# Read-in
avatarQual = pd.read_csv("PT Qualtrics Data Avatar.csv")
cylinderQual = pd.read_csv("PT Qualtrics Data Cylinder.csv")

# Clean-up
avatarQual.drop(avatarQual.index[4], inplace=True)

# Combining qualtrics answers with response times from the dfs above
# Labels: [Participant #, Arm_Length, Gender, Strategy_Change?, Avg Response Time]
def combineDF(qualtricsDF, dataDF):
    # Create a new dataframe with select columns from qualtrics csv
    newDF = qualtricsDF[['Please have the experimenter enter your participant number.',
                         'Please have the participant enter your arm length.',
                         'Please select the gender that you best identify with.',
                         'Did your strategy for completing the task change when the cylinder was present?']].copy()

    # Rename the column names
    newDF.columns = ['Participant_Number', 'Arm_Length', 'Gender', 'Strategy_Change']

    # TODO: Add avg response time to each participant from their data csv

    return newDF

# Assigning newDFs names
avatarCombined = combineDF(avatarQual, avatarClean)
cylinderCombined = combineDF(cylinderQual, cylinderClean)
print(avatarCombined.head(5))



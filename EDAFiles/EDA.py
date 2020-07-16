# Imports
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(color_codes=True)

# TODO: Implement qualtrics data

# Read-in.
avatarRaw = pd.read_csv("PT_Avatar_Raw.csv")
cylinderRaw = pd.read_csv("PT_Cylinder_Raw.csv")

# Cleaning up data by removing participants
# Shows rows with NaN: avatarRaw[avatarRaw["Response_Time"].isnull()]
# Removing “Can’t Reach” trials, response times < 200 ms, and response times 3 SD above and below mean.
# TODO: If slow, you can speed this up by specifying multiple drop conditions through one pass of the df
def cleanData(dataframe, type="cylinder"):
    # Creating duplicate to preserve original
    cleanDF = dataframe

    # If type avatar, drop participant 9
    if type == "avatar":
        cleanDF.drop(cleanDF[cleanDF["Participant"] == 9].index, inplace=True)

    # Remove any NaNs
    cleanDF.dropna(inplace=True)

    # Removing Accuracy and Acc_dc column (96-99% accuracy rate)
    cleanDF.drop(columns=['Accuracy', "Acc_dc"], inplace=True)

    # Dropping rows with "Can't reach" as a response
    cleanDF.drop(cleanDF[cleanDF["Response"] == "Can't Reach"].index, inplace=True)

    # Converting response time to floats
    cleanDF["Response_Time"] = cleanDF["Response_Time"].astype(float)

    # Dropping response times < 200ms
    cleanDF.drop(cleanDF[cleanDF["Response_Time"] < .2].index, inplace=True)

    return cleanDF

avatarClean = cleanData(avatarRaw, "avatar")

# Plot
boxPlot = sns.boxplot(x=avatarClean['Response_Time'])
plt.show()

# Testing
# print(avatarClean.dtypes)
# print(avatarClean.isnull().sum())
# print(avatarClean.head(11))







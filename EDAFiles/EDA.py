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
# Removing “Can’t Reach” trials, response times < 200 ms, and response times 3 SD above and below mean.
# def clean_data(dataframe):

# Participant 9 in avatarRaw was also removed for accuracy below 50%
# def avatarClean(dataframe):






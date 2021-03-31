#! /bin/python3
#  PAI789 (PJW)
#
#  Demonstrate drawing a simple heatmap. Note: to run this 
#  script you'll need to download the demo.csv file from 
#  the course Google Drive for this assignment.
#

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#
#  Read a grid of data
#

data = pd.read_csv('demo.csv',index_col="name")

print(data)

#
#  Now draw the heatmap
#

fig, ax1 = plt.subplots(dpi=300)
sns.heatmap(data,annot=True,fmt=".0f",ax=ax1)
fig.suptitle("Demo Data Heatmap")
ax1.set_xlabel("Column")
ax1.set_ylabel("Row")
fig.tight_layout()
fig.savefig('demo.png')
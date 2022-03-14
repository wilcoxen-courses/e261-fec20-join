"""
demo.py
Spring 2022 PJW

Demonstrate drawing a simple heatmap.
"""

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

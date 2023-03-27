"""
demo.py
Spring 2023 PJW
Demonstrate multi-level column indexes and drawing simple heatmaps.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['figure.dpi'] = 300

#
#  Read data in long form where each record consists of a
#  row name, a column name, a mean, and a count.
#

data = pd.read_csv('demo.csv',index_col=["row","col"])

#%%
#
# Now unstack the columns
#

grid = data.unstack('col')

#
# The columns are now a multi-index with the mean and count as the
# top level and the column names as the second level
#

print( grid )

#%%
#
# For convenience, extract the two blocks of data using the top level
# column names
#

means = grid['mean']
counts = grid['count']

#
#  Now draw some heatmaps. Set the size of the figure to be larger
#  than usual: 12 inches wide and 6 inches high.
#

fig, axs = plt.subplots(1,2,figsize=(12,6))
fig.suptitle("Examples of Data Heatmaps")

sns.heatmap(means,annot=True,fmt=".0f",cmap='Spectral',ax=axs[0])
axs[0].set_title('Means: Example data with a pattern')

sns.heatmap(counts,annot=True,fmt=".0f",cmap='Spectral',ax=axs[1])
axs[1].set_title('Counts: Example random data')

for ax in axs:
    ax.set_xlabel("Column")
    ax.set_ylabel("Row")

fig.tight_layout()
fig.savefig('demo.png')

#%%
#
# It's also possible to pick out data based on the lower level of
# the column index using the .xs() method:
#

print('\nData associated with column c1:\n')
c1 = grid.xs('c1',axis='columns',level=1)
print(c1)

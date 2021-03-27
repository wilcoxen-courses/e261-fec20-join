# Exercise: Cleaning and Analyzing the 2016 Election Data

### Summary

This exercise cleans up the election data from the previous assignment,
joins it with some additional information from the FEC, and then does 
a little analysis.

### Input Data

The following input files are available on the course Google Drive: 
**contrib_by_zip.csv**, the result of the previous exercise aggregating
political contributions, **pocodes.csv**, a list of states that will be 
used for filtering the data, **committees.csv**, FEC information about 
campaign committees, and **candidates.csv**, FEC information about 
candidates. Note that **committees.csv** and **candidates.csv** contain
information about House and Senate races, not just the Presidential 
election, and there is data for some years other than 2016. We'll filter
all that out.

### Deliverables

The deliverables for this assignment are three scripts, **contrib_clean.py**,
which removes some unneeded records from the aggregated contributions
data, **com_cand_info.py**, which builds a file of information about 
committees and candidates, and **by_place_cand.py** that builds a joined 
dataset and does a little analysis. Instructions for each are provided below.

### Instructions

**A. Script contrib_clean.py**

1. Set `contrib` to `pd.read_csv()` applied to file `contrib_by_zip.csv`
using `dtype=str`.

1. Make `contrib['amt']` numeric by setting it to `contrib['amt']` with 
the `.astype(float)` method applied to it.

1. Set `po` to `pd.read_csv()` applied to file `pocodes.csv`.

1. Drop the `Name` column from `po` by using the `.drop()` method with 
arguments `'Name'`, `axis='columns'`, and `inplace=True`. From here on,
any instructions to drop variables should use the same approach. If you 
need to drop multiple variables at once, you can use a list rather than 
a single variable name.

1. To filter out all the state codes that aren't in the 50 states 
plus Washington, DC, and Puerto Rico (PR), we'll join on a list of the 
state codes we want to keep, which are in `po`. That will let us detect 
everything else. To do the join, set `contrib` to `contrib.merge()` with 
the following arguments: `po`, `left_on='STATE'`, `right_on='PO'`, 
`how='outer'`, `validate='m:1'`, and `indicator=True`. This will use the 
two-letter postal codes as the keys in the join. If you're using an older 
version of Pandas you might get an error about `validate` being unexpected.
If so, omit the `validate='m:1'` argument and also omit similar arguments 
in other merges.

1. Print `contrib['_merge'].value_counts()` to check the results of the
    merge. Records for places in `pocodes.csv` will be listed as 'both'. Those 
    in the FEC data but not in `pocodes.csv` will be listed as 'left_only'. 
    Anything that was in `pocodes.csv` but not in the FEC data would be shown as 
    'right_only' but that should be 0 in this case. 

    Please note that this step will come up after most or all of the merges. 
    From here on out the instruction *print the merge indicator* will 
    mean to do something like this for the preceding merge. 
    
1. Set `state_bad` to `contrib['_merge'] != 'both'`. We'll use that to 
remove the records that didn't match the geographic entities in `pocodes.csv`. 
We'll refer to these as bad states because we're focusing on the states 
plus DC and PR. However, a lot of them are actually legitimate postal codes 
for things other than US states, such as US military addresses, US 
territories, Canadian provinces, and foreign country codes.

1. Drop the `'_merge'` and `'PO'` columns from `contrib`. We're done with 
them.

1. Next we'll tabulate the data that's going to be dropped when we exclude
    records with bad state codes. Start by picking out the bad records 
    and grouping them by state as shown below:
    
    ```
    bad_recs = contrib[state_bad].groupby('STATE')
    ```
    
    The `contrib[state_bad]` selects the records where `state_bad` is True
    and `.groupby('STATE')` groups the selected records by state code.
    
1. Sum up the contributions in those states by setting `state_bad_amt` 
to the result of applying the `.sum()` method to `bad_recs['amt']`.

1. Print `state_bad_amt` to show the state codes and total contributions.
Then print `state_bad_amt.sum()` to show the total contributions from 
those states. It's always useful to have a concrete idea about how 
much data is lost when filtering out records.

1. Now filter out the records by setting `contrib` to the rows of 
`contrib` where `state_bad` is `False`.

1. Now we'll look for bad zipcodes by finding any that aren't purely 
numeric. To do that, set `num_zip` to the result of calling the 
`pd.to_numeric()` function with the following arguments: `contrib['zip']` 
and `errors='coerce'`. That tells Pandas to build a new series by converting
the `zip` column into its numeric equivalent. The important feature is the 
`errors='coerece'` argument: that tells Pandas to put in the missing data 
code for anything that can't be converted to a number rather than stopping 
with an error message. 

1. Set `zip_bad` to `num_zip` with the `.isna()` method applied to it.
The result will be a series with true where the corresponding value of 
num_zip is missing and false everywhere else.

1. Do an analysis similar to that for `state_bad`. Set `bad_recs` to 
`contrib[zip_bad].groupby('zip')`. Then set `zip_bad_amt` to the result of 
summing `bad_recs['amt']`, print `zip_bad_amt`, and print the result of 
summing it.

1. Now filter out the records by setting `contrib` to the rows of 
`contrib` where `zip_bad` is `False`.

1. Use the `.to_pickle()` method of `contrib` to write a file called  
`contrib_clean.pkl`.

1. Now we'll compute total contributions by committee, which will 
be useful later. Start by summing the contributions to each committee. 
Set `by_com` to `contrib` grouped by the committee `'CMTE_ID'` and then, 
create `com_total` by applying the `.sum()` method to `by_com['amt']`. 

1. Then change the name of the data in the series to `'total_amt'` to 
reflect that it is the total by committee. That's done by setting the 
`name` attribute of the series to `'total_amt'` as follows:

    ```
    com_total.name = 'total_amt'
    ```
    
1. Finally, use the `.to_csv()` method to write `com_total` to file 
`com_total.csv`. If you might be using a version of Pandas prior to 0.24.0
include the keyword `header=True` in the call. If you're not sure, it won't 
hurt to include it.

**B. Script com_cand_info.py**

1. Set `contrib` to the result of using `pd.read_pickle()` to reload the 
data written by the previous script.

1. Set `com_total` to the result of using `pd.read_csv()` on 
`com_total.csv`.

1. Set `com_info` to the result of applying `pd.read_csv()` to file 
`committees.csv` using the argument `dtype=str`.

1. Trim down `com_info` by setting it to the following list of columns of 
its columns: `['CMTE_ID', 'CMTE_NM', 'CMTE_PTY_AFFILIATION', 'CAND_ID']`.
 
1. Now we'll join the total contributions onto `com_info`. Set `com_merged` 
to the result of `com_info.merge()` called with the following arguments: 
`com_total`, `how='right'`, `validate='m:1'`, and `indicator=True`. We're 
using a right join because we only want the committees that had 
contributions in the presidential race. 

1. Print the merge indicator to verify that all of the committees with 
contributions were found in `com_info`.

1. Drop `'_merge'`.

1. In principle, a committee could fund multiple candidates, which would 
be a problem because we wouldn't know how the committee split its donations
between the candidates. We'll check whether that's an issue. Set `numcan` 
to `com_info` with the `.groupby()` method applied using the argument 
`'CMTE_ID'` and then apply the `.size()` method at the end. The `.size()` 
method counts the number of entries in each group, so the result will be a 
series with the number of times each committee appears in `com_info`.

1. Print `numcan` for entries where `numcan > 1`. If all has gone well 
the result will be an empty series. That indicates that there aren't any 
committees with more than one candidate.

1. Now read the information about candidates. Set `pres` to the result of 
using `pd.read_csv()` to read `candidates.csv` using `dtype=str`.

1. Next we'll filter out everyone who wasn't running for President in 2016. 
Start by setting `is_pres` to `pres['CAND_OFFICE'] == 'P'`. That will be true
for Presidential candidates and false for everyone else.

1. Set `is_2016` in a similar manner but use `'CAND_ELECTION_YR'` and 
`'2016'`.

1. Set `keep` to `is_pres & is_2016`. That will be true for Presidential 
candidates in 2016 and false everywhere else.

1. Set `pres` to the subset `pres[keep]`. That will eliminate all the 
other candidates and election years.

1. Drop `'CAND_OFFICE'` and `'CAND_ELECTION_YR'` from `pres`: we're done 
with them.

1. Now we'll join the candidate date onto the committee information. Set 
`com_cand` to `com_merged.merge()` with the following arguments: `pres`, 
`how='left'`, `validate='m:1'`, `indicator=True`. Because we're not 
specifying any join keys, Pandas will default to using all the columns 
that exist in both dataframes. Here, that's only `CAND_ID`, which is 
exactly what we want.

1. Print the merge indicator. You should see that committees were 
eliminated: those were committees for candidates from previous elections
who happened to have some transactions in the 2016 election cycle.

1. Set `com_cand` to its subset where `com_cand['_merge'] == 'both'`.

1. Drop `'_merge'` from com_cand.

1. Use the `to_csv()` method to write `com_cand` to `com_cand_info.csv`.

**C. Script by_place_cand.py**

1. Set `contrib` to the result of using `pd.read_pickle()` to reload 
`contrib_clean.pkl` and set `com_cand` to the result of using `pd.read_csv()`
to read `com_cand_info.csv`.

1. Create `merged` by joining `com_cand` onto `contrib` using 
`contrib.merge()` with the following arguments: `com_cand`,`on='CMTE_ID'`,
`validate='m:1'`, and `indicator=True`.

1. Print the merge indicator to verify that all records matched.

1. Drop `'_merge'` from `merged`.

1. Since a number of the candidates have more than one committee, we'll now
aggregate the data to candidates. Set `group_by_place_cand` to 
`merged.groupby()` called with a list consisting of the following columns: 
`'STATE'`,`'zip'`,`'CAND_NAME'`.

1. Set `by_place_cand` to the result of applying the `.sum()` method to 
`group_by_place_cand['amt']`. That will total up the contributions to each 
candidate by each place (state and zipcode combination).

1. Use `.to_csv()` to write `by_place_cand` out to file `by_place_cand.csv`.

1. Now we'll do a little analysis to see which places provided the largest 
contributions to each candidate. Start by setting `by_cand` to `com_cand` grouped 
by `'CAND_NAME'`. Then set `cand_tot` to the result of applying `.sum()` 
to `by_cand['total_amt']`. 

1. Now set `top10` to the result of applying `.sort_values()` to `cand_tot`
using the argument `ascending=False`. Then pick out the candidates with 
the 10 largest total contributions by using `[0:10]` on the result of the
sort.

1. Print `top10`.

1. Now create a for loop over `top10.index` using running variable `name`.
Within the loop do the following:

    1. Print a blank line and then message something like "Top 5 places for" 
    and then `name`.
    
    1. Set `subset` to `by_place_cand.loc[:,:,name]`. That will pick out 
    the rows of `by_place_cand` for the current candidate.
    
    1. Set `top5` to the result of applying `.sort_values()` to `subset`
    with argument `ascending=False`. Then pick out the first 5 rows using 
    `[0:5]`.
    
    1. Print `top5`.

### Submitting

Once you're happy with everything and have committed all of the changes to
your local repository, please push the changes to GitHub. At that point, 
you're done: you have submitted your answer.

### Tips

+ A subsequent assignment will map some of the detailed data saved in 
`by_place_cand.csv`. In the mean time, you might find it interesting to 
look up a few zipcodes you know to see what contributions looked like 
in those areas.

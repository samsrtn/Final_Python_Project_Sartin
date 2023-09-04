# Final Python Assignment
import pandas as pd

###########################################################
###########################################################
# 1. Load the data and convert it into a dataframe.
df_trials = pd.read_excel('Trial_order.xlsx')
df_sub = pd.read_excel('Sub_info.xlsx')
print(df_trials)
print(df_sub)

#################################################################################
#################################################################################
# 2. Calculate the final size estimate (without estimation noise; see README.md).
# Perform the subtraction (raw_est - est_noise) and assign the result to a new column "final_est".
# Calculate the difference between raw_est and est_noise using apply and lambda
df_trials['final_est'] = df_trials.apply(
    lambda row: row['raw_est'] - df_sub.loc[df_sub['subject'] == row['subject'], 'est_noise'].values[0], axis=1)

print(df_trials)

###########################################################
###########################################################
# 3. Search for outliers
# 3.1 For each subject, calculate mean and standard deviation (SD) for each condition
# Calculate mean and SD for each group
grouped = df_trials.groupby(['subject', 'noise', 'size'])['final_est'].agg(['mean', 'std']).reset_index()

# Merge the calculated statistics back to the original dataframe
df_trials = df_trials.merge(grouped, on=['subject', 'noise', 'size'])

# 3.2 Calculate the threshold for outliers (mean +/- 2.5 SDs)
df_trials['upper_threshold'] = df_trials['mean'] + 2.5 * df_trials['std']
df_trials['lower_threshold'] = df_trials['mean'] - 2.5 * df_trials['std']

# 3.3 Print rows considered outliers
outliers = df_trials[
    (df_trials['final_est'] > df_trials['upper_threshold']) |
    (df_trials['final_est'] < df_trials['lower_threshold'])
]
print("Outliers:")
print(outliers)
print(outliers[['noise', 'size']])

# 3.4 Create a new dataframe filtering out the outliers
df_without_outliers = df_trials[
    (df_trials['final_est'] <= df_trials['upper_threshold']) &
    (df_trials['final_est'] >= df_trials['lower_threshold'])
]

# Display the new dataframe without outliers and remove unuseful columns
df_without_outliers = df_without_outliers.drop(columns=['upper_threshold', 'lower_threshold', 'mean', 'std'])
print(df_without_outliers)
df_without_outliers.to_excel('df_trials_wo_outliers.xlsx', index=False)

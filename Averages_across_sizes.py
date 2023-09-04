# Final Python Assignment
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as st
from scipy.stats import ttest_rel
from statsmodels.stats.multitest import multipletests

############################################################################################
### ANALYSIS OF MEAN SIZE ESTIMATES IN THE DIFFERENT NOISE CONDITIONS (IRRESPECTIVE OF SIZE)
############################################################################################
# 1. Load the data and convert it into a dataframe
df_trials = pd.read_excel('df_trials_wo_outliers.xlsx')
print(df_trials)

#########################################################################################################
#########################################################################################################
# 2. Create box plot to show size estimates averaged across sizes and subjects, in all 4 noise conditions
# First, filter dataframe to include only sizes 1 and 3
df_filtered_sizes_1_3 = df_trials[df_trials['size'].isin([1, 3])]

# Calculate average final_est for sizes 1 and 3 combined (irrespective of size), for each noise condition
avg_across_sizes = df_filtered_sizes_1_3.groupby(['noise'])['final_est'].mean().reset_index()

# Define the order in which to show the noise conditions in the box plot
noise_order = ['LN', 'CN', 'RN', 'NN']

# Create the BOX PLOT
plt.figure(figsize=(6, 4))
ax = sns.boxplot(
    data=df_filtered_sizes_1_3, x='noise', y='final_est', order=noise_order, color='#fe9929',
    showcaps=False, showfliers=False)
sns.pointplot(
    data=avg_across_sizes, x='noise', y='final_est', order=noise_order, dodge=0.3, join=False, markers='s', scale=1.2,
    color='#993404')

# Set plot labels and title
plt.xlabel('Noise Condition', fontsize=9)
plt.ylabel('Grip Aperture (mm)', fontsize=9)
plt.title('Average Size Estimate for each Noise Condition', fontsize=10)
plt.show()


###########################################################
###########################################################
# 3. Create bar graph to show size estimates averaged across sizes and subjects, in all 4 noise conditions, with 95% CI

# 3.1 First, calculate statistics
# Group by noise, then calculate statistics for final_est (mean, SD, and count/sample size)
grouped_stats = df_filtered_sizes_1_3.groupby(['noise'])['final_est'].agg(['mean', 'std', 'count']).reset_index()

# Calculate 95% confidence interval
conf_interval = 0.95


def calc_conf_interval(data):
    mean = data['mean']
    std = data['std']
    n = data['count']
    standard_error = std / (n ** 0.5)  # Calculate standard error of the mean
    interval = st.norm.interval(conf_interval, loc=mean, scale=standard_error)
    return pd.Series({'lower_ci': interval[0], 'upper_ci': interval[1]})


# Calculate confidence intervals
conf_intervals = grouped_stats.groupby(['noise']).apply(calc_conf_interval).reset_index()
# Merge confidence intervals back to the grouped_stats dataframe
grouped_stats = grouped_stats.merge(conf_intervals, on=['noise'])
# Add a column with calculated amount of 95% CI
grouped_stats['CI'] = (grouped_stats['upper_ci'] - grouped_stats['lower_ci']) / 2

# Rename columns for clarity
grouped_stats.rename(columns={'mean': 'mean_group', 'std': 'st_dev', 'count': 'sample_size'}, inplace=True)

# Display the statistics with confidence intervals
print(grouped_stats)

# 3.2 Now create the Bar graph
plt.figure(figsize=(5, 4))

# Extract the data for plotting
mean_estimates = grouped_stats['mean_group']
noise_labels = ['LN', 'CN', 'RN', 'NN']

# Sort the data frame by the custom order (to assure that bars are displayed in the above-mentioned order)
grouped_stats['noise'] = pd.Categorical(grouped_stats['noise'], noise_labels)
grouped_stats = grouped_stats.sort_values('noise')

# Create the bar graph with error bars
plt.bar(noise_labels, mean_estimates, yerr=(
    grouped_stats['CI'], grouped_stats['CI']), capsize=3, color='chocolate', edgecolor='black', width=0.5,
        tick_label=noise_labels)

# Customizing plot appearance
plt.title('Average Size Estimate for each Noise Condition with 95% CI', fontsize=10)
plt.xlabel('Noise Condition', fontsize=9)
plt.ylabel('Grip Aperture (mm)', fontsize=9)
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()

plt.show()

# 4. PERFORM STATISTICAL COMPARISONS BETWEEN NOISE CONDITIONS

# Calculate Average Size Estimates for Each Subject
subject_avg_size = df_trials.groupby(['subject', 'noise'])['final_est'].mean().reset_index()

# Perform t-tests and FDR correction
# Dataframe to store t-test results
t_test_results = []

# Loop through each noise
for i in range(len(noise_labels)):
    for j in range(i + 1, len(noise_labels)):
        noise_i = noise_labels[i]
        noise_j = noise_labels[j]

        noise_i_data = subject_avg_size[subject_avg_size['noise'] == noise_i]['final_est']
        noise_j_data = subject_avg_size[subject_avg_size['noise'] == noise_j]['final_est']

        t_stat, p_value = ttest_rel(noise_i_data, noise_j_data)

        t_test_results.append({'noise_pair': f"{noise_i}-{noise_j}", 't_stat': t_stat, 'p_value': p_value})

t_test_df = pd.DataFrame(t_test_results)

# Apply FDR correction
rejected, adjusted_p_values, _, _ = multipletests(t_test_df['p_value'], method='fdr_bh')
t_test_df['adjusted_p_value'] = adjusted_p_values
t_test_df['H0_rejected'] = rejected  # null hypothesis (H0) rejected: True or False?

print(t_test_df)  # none of the comparisons were significant after adjusting for multiple comparisons
# using the FDR method (all values are "False", that is H0 cannot be rejected).

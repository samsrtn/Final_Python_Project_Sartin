# Final Python Assignment
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as st
from scipy.stats import ttest_rel
from statsmodels.stats.multitest import multipletests

######################################################################################################
### ANALYSIS OF VARIABILITY OF SIZE ESTIMATES IN THE DIFFERENT NOISE CONDITIONS (IRRESPECTIVE OF SIZE)
######################################################################################################
# 1. load the data and convert it into a dataframe
df_trials = pd.read_excel('df_trials_wo_outliers.xlsx')
print(df_trials)


###########################################################
###########################################################
# 2. Calculations
# First, filter the dataframe to include only sizes 1 and 3
df_filtered_sizes_1_3 = df_trials[df_trials['size'].isin([1, 3])]

# Calculate standard deviations of final_est (size estimates) for sizes 1 and 3, for each noise condition and for each
# subject
std_estimates = df_filtered_sizes_1_3.groupby(['subject', 'noise', 'size'])['final_est'].std().reset_index()
std_estimates = std_estimates.rename(columns={'final_est': 'std_est'})
print(std_estimates)

# Calculate the average and the standard deviation of standard deviations across subjects and sizes, for each noise
# condition, along with sample size
grouped_stats = std_estimates.groupby(['noise'])['std_est'].agg(['mean', 'std', 'count']).reset_index()
print(grouped_stats)

# Calculate 95% confidence interval
conf_interval = 0.95


def calc_conf_interval(data):
    mean = data['mean']
    std = data['std']
    n = data['count']
    standard_error = std / (n ** 0.5)  # Calculate standard error of the mean
    interval = st.norm.interval(conf_interval, loc=mean, scale=standard_error)
    return pd.Series({'lower_ci': interval[0], 'upper_ci': interval[1]})


# Calculate confidence intervals and merge the results
conf_intervals = grouped_stats.groupby('noise').apply(calc_conf_interval).reset_index()
print(conf_intervals)

# Merge confidence intervals back to the grouped_stats dataframe
grouped_stats = grouped_stats.merge(conf_intervals, on=['noise'])
grouped_stats['CI'] = (grouped_stats['upper_ci'] - grouped_stats['lower_ci']) / 2
# Rename columns for clarity
grouped_stats.rename(columns={'mean': 'mean_std', 'std': 'std_std', 'count': 'sample_size'}, inplace=True)

# Display the statistics with confidence intervals
print(grouped_stats)

###########################################################
###########################################################
# 3. PLOTS
# 3.1 Create box plot to show standard deviations of size estimates averaged across sizes and subjects, in all 4 noise
# conditions

# Define the order in which to show the noise conditions in the box plot
noise_order = ['LN', 'CN', 'RN', 'NN']

# Create the box plot with 95% confidence intervals
plt.figure(figsize=(8, 5))
ax = sns.boxplot(
    data=std_estimates, x='noise', y='std_est', order=noise_order, color='#fe9929', showcaps=False, showfliers=False)
sns.pointplot(
    data=grouped_stats, x='noise', y='mean_std', order=noise_order, dodge=0.3, join=False, markers='s', scale=1.2,
    color='#993404')

# Set plot labels and title
plt.xlabel('Noise Condition', fontsize=9)
plt.ylabel('Standard Deviation of Grip Aperture (mm)', fontsize=9)
plt.title(
    'Average Standard Deviation of Size Estimates for each Noise Condition', fontsize=10)
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)

plt.show()

# 3.2 Create bar graph to show SDs of size estimates in the 4 noise conditions, with 95% CI
# Prepare data for plotting
noise_labels = ['LN', 'CN', 'RN', 'NN']
# Sort the data frame by the custom order (to assure that bars are displayed in the above-mentioned order)
grouped_stats['noise'] = pd.Categorical(grouped_stats['noise'], noise_labels)
grouped_stats = grouped_stats.sort_values('noise')

# Create the bar graph
plt.figure(figsize=(5, 4))
plt.bar(
    grouped_stats['noise'], grouped_stats['mean_std'], yerr=(grouped_stats['CI'], grouped_stats['CI']), capsize=3,
    color='chocolate', edgecolor='black', alpha=0.7, width=0.5, tick_label=noise_labels)

# Customizing plot appearance
plt.title('Average Standard Deviation (SD) of Size Estimates'
          '\n for each Noise Condition with 95% Confidence Intervals', fontsize=10)
plt.xlabel('Noise Condition', fontsize=9)
plt.ylabel('Standard Deviation of Grip Aperture (mm)', fontsize=9)
plt.xticks(range(len(noise_labels)), noise_labels, fontsize=8)
plt.yticks(fontsize=8)
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()

plt.show()

###########################################################
###########################################################
# 4. PERFORM STATISTICAL COMPARISONS BETWEEN NOISE CONDITIONS

# Calculate Average SD of Size Estimates for Each Subject
subject_avg_size_sd = std_estimates.groupby(['subject', 'noise'])['std_est'].mean().reset_index()

# Perform t-tests and FDR correction
# Dataframe to store t-test results
t_test_results = []

# Loop through each noise
for i in range(len(noise_labels)):
    for j in range(i + 1, len(noise_labels)):
        noise_i = noise_labels[i]
        noise_j = noise_labels[j]

        noise_i_data = subject_avg_size_sd[subject_avg_size_sd['noise'] == noise_i]['std_est']
        noise_j_data = subject_avg_size_sd[subject_avg_size_sd['noise'] == noise_j]['std_est']

        t_stat, p_value = ttest_rel(noise_i_data, noise_j_data)

        t_test_results.append({'noise_pair': f"{noise_i}-{noise_j}", 't_stat': t_stat, 'p_value': p_value})

t_test_df = pd.DataFrame(t_test_results)

# Apply FDR correction
rejected, adjusted_p_values, _, _ = multipletests(t_test_df['p_value'], method='fdr_bh')
t_test_df['adjusted_p_value'] = adjusted_p_values
t_test_df['H0_rejected'] = rejected  # null hypothesis (H0) rejected: True or False?

print(t_test_df)  # none of the comparisons were significant after adjusting for multiple comparisons
# using the FDR method (all values are "False", that is H0 cannot be rejected).

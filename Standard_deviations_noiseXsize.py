# Final Python Assignment
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as st
from scipy.stats import ttest_rel
from statsmodels.stats.multitest import multipletests

########################################################################################
### ANALYSIS OF VARIABILITY OF SIZE ESTIMATES IN THE DIFFERENT NOISE x SIZE COMBINATIONS
########################################################################################
# 1. load the data and convert it into a dataframe
df_trials = pd.read_excel('df_trials_wo_outliers.xlsx')
print(df_trials)

###########################################################
###########################################################
# 2. Calculations
# First, filter the dataframe to include only sizes 1 and 3
df_filtered_sizes_1_3 = df_trials[df_trials['size'].isin([1, 3])]

# Calculate standard deviations of final_est (size estimates), for sizes 1 and 3, for each noise condition and for each
# subject
std_estimates = df_filtered_sizes_1_3.groupby(['subject', 'noise', 'size'])['final_est'].std().reset_index()
std_estimates = std_estimates.rename(columns={'final_est': 'std_est'})
print(std_estimates)

# Calculate the average, SD and count of standard deviations across subjects, for each noise x size combination
grouped_stats = std_estimates.groupby(['noise', 'size'])['std_est'].agg(['mean', 'std', 'count']).reset_index()
print(grouped_stats)

# Calculate 95% confidence interval
conf_interval = 0.95

# LP: As you are using this function across multiple scripts, this is a good example
# of code that it would be nice to factor out into a separate file and import!
# Same for lines below until 55, there seems to be a lot of overlapping with eg
# Standard_deviations_across_sizes.py. you might have to spend some time thinking
# about how to best factor out the code so that it can be used in multiple places, eg
# by specifying as an argument the columns to group by.
def calc_conf_interval(data):
    mean = data['mean']
    std = data['std']
    n = data['count']
    standard_error = std / (n ** 0.5)  # Calculate standard error of the mean
    interval = st.norm.interval(conf_interval, loc=mean, scale=standard_error)
    return pd.Series({'lower_ci': interval[0], 'upper_ci': interval[1]})


# Calculate confidence intervals and merge the results
conf_intervals = grouped_stats.groupby(['noise', 'size']).apply(calc_conf_interval).reset_index()
print(conf_intervals)

# Merge confidence intervals back to the grouped_stats dataframe
grouped_stats = grouped_stats.merge(conf_intervals, on=['noise', 'size'])
grouped_stats['CI'] = (grouped_stats['upper_ci'] - grouped_stats['lower_ci']) / 2

# Rename columns for clarity
grouped_stats.rename(columns={'mean': 'mean_std', 'std': 'std_std', 'count': 'sample_size'}, inplace=True)

# Display the statistics with confidence intervals
print(grouped_stats)

###########################################################
###########################################################
# 3. Create bar graph for sizes 1 and 3, in all 4 noise conditions, with 95% CI
# Prepare data for plotting
noise_labels = ['LN', 'CN', 'RN', 'NN']
size_labels = [1, 3]
size_legend_labels = ['Size 1', 'Size 3']
bar_colors = ['chocolate', 'saddlebrown']  # Colors for Size 1 and Size 3 bars

# Convert 'size' and 'noise' to categorical variables
grouped_stats['size'] = pd.Categorical(grouped_stats['size'], categories=[1, 3])
grouped_stats['noise'] = pd.Categorical(grouped_stats['noise'], categories=noise_labels)
# Convert 'mean_ci' and 'upper_ci' columns to float64
grouped_stats['lower_ci'] = grouped_stats['lower_ci'].astype(float)
grouped_stats['upper_ci'] = grouped_stats['upper_ci'].astype(float)

# Sort the data frame by the custom order
grouped_stats = grouped_stats.sort_values('noise')

# Create the bar graph with error bars
plt.figure(figsize=(6, 4))
bars = []

for i, noise in enumerate(noise_labels):
    size_data = grouped_stats[grouped_stats['noise'] == noise]
    y_means = size_data['mean_std']
    y_err_lower = y_means - size_data['lower_ci']
    y_err_upper = size_data['upper_ci'] - y_means

    bar_positions = [i - 0.2, i + 0.2]  # Separate positions for "Size 1" and "Size 3" bars
    bar_heights = y_means.tolist()
    bar_errors = [[y_err_lower.iloc[0], y_err_lower.iloc[1]], [y_err_upper.iloc[0], y_err_upper.iloc[1]]]

    bars.extend(plt.bar(
        bar_positions, bar_heights, yerr=bar_errors, capsize=3, width=0.4, label=noise, edgecolor='black',
        color=bar_colors))

# Customizing plot appearance
plt.title('Average Standard Deviation of Size Estimates with 95% Confidence Intervals', fontsize=10)
plt.xlabel('Noise Condition', fontsize=9)
plt.ylabel('Standard Deviation of Grip Aperture (mm)', fontsize=9)
plt.xticks(range(len(noise_labels)), noise_labels, fontsize=8)
plt.yticks(fontsize=8)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(handles=bars[:2], labels=size_legend_labels, title="Size", fontsize=9)  # Using only two bars for legend

plt.tight_layout()

plt.show()

#################################################################################
#################################################################################
# 4. PERFORM STATISTICAL COMPARISONS

# 4.1 BETWEEN SIZES 1 AND 3 WITHIN EACH NOISE CONDITION

# Calculate Average SD of Size Estimates for Each Subject
noise_size_avg_sd = std_estimates.groupby(['subject', 'noise', 'size'])['std_est'].mean().reset_index()

t_test_results_1 = []

for noise in noise_labels:
    noise_data = noise_size_avg_sd[noise_size_avg_sd['noise'] == noise]

    size_1_avg = noise_data[noise_data['size'] == 1]['std_est']
    size_3_avg = noise_data[noise_data['size'] == 3]['std_est']

    t_stat, p_value = ttest_rel(size_1_avg, size_3_avg)

    t_test_results_1.append({'noise': noise, 'size_pair': f"1-3", 't_stat': t_stat, 'p_value': p_value})

t_test_df_1 = pd.DataFrame(t_test_results_1)

# Apply FDR correction
rejected, adjusted_p_values, _, _ = multipletests(t_test_df_1['p_value'], method='fdr_bh')
t_test_df_1['adjusted_p_value'] = adjusted_p_values
t_test_df_1['H0_rejected'] = rejected     # null hypothesis (H0) rejected: True or False?

print(t_test_df_1)   # None of the comparisons is significant (p-value > 0.05) after adjusting for multiple comparisons.
# Therefore, there are no significant differences between the average standard deviations of size estimates of sizes 1
# and 3 within any noise conditions.

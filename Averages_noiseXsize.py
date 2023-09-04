# Final Python Assignment
import pandas as pd
import scipy.stats as st
import matplotlib.pyplot as plt
from scipy.stats import ttest_rel
from statsmodels.stats.multitest import multipletests

##############################################################################
### ANALYSIS OF MEAN SIZE ESTIMATES IN THE DIFFERENT NOISE x SIZE COMBINATIONS
##############################################################################
# 1. Load the data and convert it into a dataframe
df_trials = pd.read_excel('df_trials_wo_outliers.xlsx')
print(df_trials)


###########################################################
###########################################################
# 2. perform statistics (mean, SD, 95% CI)
# First, group by noise and size and then calculate statistics for final_est (mean, standard deviation, and count)
grouped_stats = df_trials.groupby(['noise', 'size'])['final_est'].agg(['mean', 'std', 'count']).reset_index()

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
conf_intervals = grouped_stats.groupby(['noise', 'size']).apply(calc_conf_interval).reset_index()
# Merge confidence intervals back to the grouped_stats dataframe
grouped_stats = grouped_stats.merge(conf_intervals, on=['noise', 'size'])
# Add a column with calculated amount of 95% CI
grouped_stats['CI'] = (grouped_stats['upper_ci'] - grouped_stats['lower_ci']) / 2

# Rename columns for clarity
grouped_stats.rename(columns={'mean': 'mean_group', 'std': 'st_dev', 'count': 'sample_size'}, inplace=True)

# Display the statistics with confidence intervals
print(grouped_stats)


###########################################################
###########################################################
# 3. Create graphs (mean, CI)
# First, filter data for sizes 1 and 3
df_filtered_sizes_1_3 = grouped_stats[grouped_stats['size'].isin([1, 3])].copy()


# Then, convert 'size' and 'noise' to categorical variables
df_filtered_sizes_1_3['size'] = pd.Categorical(df_filtered_sizes_1_3['size'], categories=[1, 2, 3])
df_filtered_sizes_1_3['noise'] = pd.Categorical(df_filtered_sizes_1_3['noise'], categories=['CN', 'LN', 'NN', 'RN'])
# Convert 'mean_ci' and 'upper_ci' columns to float64
df_filtered_sizes_1_3['lower_ci'] = df_filtered_sizes_1_3['lower_ci'].astype(float)
df_filtered_sizes_1_3['upper_ci'] = df_filtered_sizes_1_3['upper_ci'].astype(float)

print(df_filtered_sizes_1_3)

# Sort the data frame by the custom order
df_filtered_sizes_1_3 = df_filtered_sizes_1_3.sort_values('noise')


# 3.1 Create bar graph for sizes 1 and 3, in all 4 noise conditions, with 95% CI
# First, prepare data for plotting
noise_labels = ['LN', 'CN', 'RN', 'NN']
size_labels = [1, 3]
size_legend_labels = ['Size 1', 'Size 3']
bar_colors = ['chocolate', 'saddlebrown']  # Colors for Size 1 and Size 3 bars


# Now, create the bar graph with error bars
plt.figure(figsize=(6, 4))
bars = []

for i, noise in enumerate(noise_labels):
    size_data = df_filtered_sizes_1_3[df_filtered_sizes_1_3['noise'] == noise]
    y_means = size_data['mean_group']
    y_err_lower = y_means - size_data['lower_ci']
    y_err_upper = size_data['upper_ci'] - y_means

    bar_positions = [i - 0.2, i + 0.2]  # Separate positions for "Size 1" and "Size 3" bars
    bar_heights = y_means.tolist()
    bar_errors = [[y_err_lower.iloc[0], y_err_lower.iloc[1]], [y_err_upper.iloc[0], y_err_upper.iloc[1]]]

    bars.extend(plt.bar(
        bar_positions, bar_heights, yerr=bar_errors, capsize=3, width=0.4, label=noise, edgecolor='black',
        color=bar_colors))

# Customizing plot appearance
plt.title('Average Size Estimate for each Combination of Noise and Size\n with 95% Confidence Intervals', fontsize=10)
plt.xlabel('Noise Condition', fontsize=9)
plt.ylabel('Grip Aperture (mm)', fontsize=9)
plt.xticks(range(len(noise_labels)), noise_labels, fontsize=8)
plt.yticks(fontsize=8)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(handles=bars[:2], labels=size_legend_labels, fontsize=9)  # Using only two bars for legend

plt.tight_layout()

#################################################################################
#################################################################################
# 4. PERFORM STATISTICAL COMPARISONS

# 4.1 BETWEEN SIZES 1 AND 3 WITHIN EACH NOISE CONDITION

# Calculate Average Size Estimates for Each Subject
noise_size_avg = df_trials.groupby(['subject', 'noise', 'size'])['final_est'].mean().reset_index()

t_test_results_1 = []

for noise in noise_labels:
    noise_data = noise_size_avg[noise_size_avg['noise'] == noise]

    size_1_avg = noise_data[noise_data['size'] == 1]['final_est']
    size_3_avg = noise_data[noise_data['size'] == 3]['final_est']

    t_stat, p_value = ttest_rel(size_1_avg, size_3_avg)

    t_test_results_1.append({'noise': noise, 'size_pair': f"1-3", 't_stat': t_stat, 'p_value': p_value})

t_test_df_1 = pd.DataFrame(t_test_results_1)

# Apply FDR correction
rejected, adjusted_p_values, _, _ = multipletests(t_test_df_1['p_value'], method='fdr_bh')
t_test_df_1['adjusted_p_value'] = adjusted_p_values
t_test_df_1['H0_rejected'] = rejected     # null hypothesis (H0) rejected: True or False?

print(t_test_df_1)   # All comparisons are significant (p-value < 0.05) after adjusting for multiple comparisons.
# Therefore, there are significant differences between the average size estimates of sizes 1 and 3 within all
# noise conditions.


# 4.2 BETWEEN NOISE CONDITIONS WITHIN SIZES 1 AND 3
t_test_results_2 = []

for size in size_labels:
    size_data = noise_size_avg[noise_size_avg['size'] == size]

    for i in range(len(noise_labels)):
        for j in range(i + 1, len(noise_labels)):
            noise_i = noise_labels[i]
            noise_j = noise_labels[j]

            noise_i_data = size_data[size_data['noise'] == noise_i]['final_est']
            noise_j_data = size_data[size_data['noise'] == noise_j]['final_est']

            t_stat, p_value = ttest_rel(noise_i_data, noise_j_data)

            t_test_results_2.append(
                {'size': size, 'noise_pair': f"{noise_i}-{noise_j}", 't_stat': t_stat, 'p_value': p_value})

t_test_df_2 = pd.DataFrame(t_test_results_2)

# Apply FDR correction
rejected, adjusted_p_values, _, _ = multipletests(t_test_df_2['p_value'], method='fdr_bh')
t_test_df_2['adjusted_p_value'] = adjusted_p_values
t_test_df_2['H0_rejected'] = rejected     # null hypothesis (H0) rejected: True or False?

print(t_test_df_2)   # adjusted p-values are relatively high, indicating that none of the comparisons are statistically
# significant (p > 0.05) after correcting for multiple comparisons. Thus, there are no significant differences
# between the average size estimates of the different noise conditions within each size.


# Plotting significant results in the bar graph

# Loop through t-test results for sizes 1 and 3 within each noise condition (T-TEST 1)
for i, noise in enumerate(noise_labels):
    size_1_row = t_test_df_1[(t_test_df_1['noise'] == noise) & (t_test_df_1['size_pair'] == '1-3')]
    size_data = df_filtered_sizes_1_3[df_filtered_sizes_1_3['noise'] == noise]
    lower_ci = size_data['lower_ci']
    upper_ci = size_data['upper_ci']

    if not size_1_row.empty:
        size_1_p_value = size_1_row['adjusted_p_value'].values[0]

        # Check if the p-value is significant and add corresponding annotation
        if size_1_p_value < 0.001:
            plt.plot([i - 0.2, i + 0.2], [max(upper_ci) + 1, max(upper_ci) + 1], color='black', lw=1.5)
            plt.text(i, max(upper_ci) + 0.4, "***", ha='center', va='bottom', color='black', fontsize=12)
        elif size_1_p_value < 0.01:
            plt.plot([i - 0.2, i + 0.2], [max(upper_ci) + 1, max(upper_ci) + 1], color='black', lw=1.5)
            plt.text(i, max(upper_ci) + 0.4, "**", ha='center', va='bottom', color='black', fontsize=12)
        elif size_1_p_value < 0.05:
            plt.plot([i - 0.2, i + 0.2], [max(upper_ci) + 1, max(upper_ci) + 1], color='black', lw=1.5)
            plt.text(i, max(upper_ci) + 0.4, "*", ha='center', va='bottom', color='black', fontsize=12)

    size_3_row = t_test_df_1[(t_test_df_1['noise'] == noise) & (t_test_df_1['size_pair'] == '3-1')]

    if not size_3_row.empty:
        size_3_p_value = size_3_row['adjusted_p_value'].values[0]

        # Check if the p-value is significant and add corresponding annotation
        if size_3_p_value < 0.001:
            plt.plot([i - 0.2, i + 0.2], [max(upper_ci) + 1, max(upper_ci) + 1], color='black', lw=1.5)
            plt.text(i, max(upper_ci) + 0.4, "***", ha='center', va='bottom', color='black', fontsize=12)
        if size_3_p_value < 0.01:
            plt.text(i, max(upper_ci) + 0.4, "**", ha='center', va='bottom', color='black', fontsize=12)
        if size_3_p_value < 0.05:
            plt.text(i, max(upper_ci) + 0.4, "*", ha='center', va='bottom', color='black', fontsize=12)

plt.show()

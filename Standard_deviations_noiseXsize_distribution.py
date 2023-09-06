# Final Python Assignment
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

########################################################################################
### ANALYSIS OF VARIABILITY OF SIZE ESTIMATES IN THE DIFFERENT NOISE x SIZE COMBINATIONS
########################################################################################
# 1. Load the data and convert it into a dataframe
df_trials = pd.read_excel('df_trials_wo_outliers.xlsx')
print(df_trials)

####################################################################
####################################################################
# 2. Create violin plot for sizes 1 and 3, in all 4 noise conditions
# Filter dataframe to include only sizes 1 and 3 (as we are not interested in size 2; see README.md)
df_filtered_sizes_1_3 = df_trials[df_trials['size'].isin([1, 3])]

# Calculate SDs of final_est (size estimates), for sizes 1 and 3, for each noise condition and for each subject
std_estimates = df_filtered_sizes_1_3.groupby(['subject', 'noise', 'size'])['final_est'].std().reset_index()
std_estimates = std_estimates.rename(columns={'final_est': 'std_est'})
print(std_estimates)

# Calculate the average of standard deviations across subjects, for each noise x size combination
avg_sd_across_subjects = std_estimates.groupby(['noise', 'size'])['std_est'].mean().reset_index()
print(avg_sd_across_subjects)

# Merge size 1 and size 3 averages into one dataframe
avg_sd_across_subjects_merged = avg_sd_across_subjects.pivot(index='noise', columns='size', values='std_est')

# Define custom color palette for violin plot
custom_palette = sns.color_palette(['#993404', '#d95f0e'])

# Define the order in which you want to display the noise conditions
custom_order = ['LN', 'CN', 'RN', 'NN']

# Create the violin plot
plt.figure(figsize=(6, 4))
ax = sns.violinplot(
    data=std_estimates, x='noise', y='std_est', hue='size', split=True, inner='quart',
    palette=custom_palette, order=custom_order)

# Create custom legend handles and labels
handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#993404', markersize=10),
           plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#d95f0e', markersize=10)]
labels = ['Size 1', 'Size 3']

# Add jittered dots for average estimates across subjects for both sizes within each noise condition
# LP: very minor: this you could have done in a small loop (just convenient to change parameters for the plot only once if needed)
# size 1
sns.stripplot(
    data=avg_sd_across_subjects_merged, x=avg_sd_across_subjects_merged.index, y=1, color='#993404',
    edgecolor="black", size=12, ax=ax, jitter=True, linewidth=1, order=custom_order)
# size 3
sns.stripplot(
    data=avg_sd_across_subjects_merged, x=avg_sd_across_subjects_merged.index, y=3, color='#d95f0e',
    edgecolor='black', size=12, ax=ax, jitter=True, linewidth=1, order=custom_order)

# Set y-axis limits
ax.set_ylim(bottom=0, top=15)

# Set plot labels and title
plt.xlabel('Noise Condition', fontsize=9)
plt.ylabel('Standard Deviation of Grip Aperture (mm)', fontsize=9)
plt.title('Standard Deviation (SD) of Size Estimates \nfor each Combination of Noise and Size', fontsize=10)
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)

# Create custom legend using custom handles and labels
plt.legend(handles=handles, labels=labels)

plt.show()

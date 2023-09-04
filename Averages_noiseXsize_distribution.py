# Final Python Assignment
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

##############################################################################
### ANALYSIS OF MEAN SIZE ESTIMATES IN THE DIFFERENT NOISE x SIZE COMBINATIONS
##############################################################################
# 1. Load the data and convert it into a dataframe
df_trials = pd.read_excel('df_trials_wo_outliers.xlsx')
print(df_trials)

####################################################################
####################################################################
# 2. Create violin plot for sizes 1 and 3, in all 4 noise conditions
# Filter dataframe to include only sizes 1 and 3 (as we are not interested in size 2; see README.md)
df_filtered_sizes_1_3 = df_trials[df_trials['size'].isin([1, 3])]

# Calculate average final_est for each noise and size combination, across subjects
avg_across_subjects = df_filtered_sizes_1_3.groupby(['noise', 'size'])['final_est'].mean().reset_index()
# Merge size 1 and size 3 averages into one dataframe
avg_across_subjects_merged = avg_across_subjects.pivot(index='noise', columns='size', values='final_est')

# Define custom color palette for violin plot
custom_palette = sns.color_palette(['#993404', '#d95f0e'])

# Define the order in which you want to display the noise conditions
custom_order = ['LN', 'CN', 'RN', 'NN']

# Create the violin plot
plt.figure(figsize=(6, 4))
ax = sns.violinplot(
    data=df_filtered_sizes_1_3, x='noise', y='final_est', hue='size', split=True, inner='quart',
    palette=custom_palette, order=custom_order)

# Create custom legend handles and labels
handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#993404', markersize=10),
           plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#d95f0e', markersize=10)]
labels = ['Size 1', 'Size 3']

# Add jittered dots for average estimates across subjects for both sizes within each noise condition
# size 1
sns.stripplot(
    data=avg_across_subjects_merged, x=avg_across_subjects_merged.index, y=1, color='#993404',
    edgecolor="black", size=12, ax=ax, jitter=True, linewidth=1, order=custom_order)
# size 3
sns.stripplot(
    data=avg_across_subjects_merged, x=avg_across_subjects_merged.index, y=3, color='#d95f0e',
    edgecolor='black', size=12, ax=ax, jitter=True, linewidth=1, order=custom_order)

# Set y-axis limits
ax.set_ylim(bottom=15, top=90)

# Set plot labels and title
plt.xlabel('Noise Condition', fontsize=9)
plt.ylabel('Grip Aperture (mm)', fontsize=9)
plt.title('Size Estimate for each Combination of Noise and Size', fontsize=10)
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)

# Create custom legend using custom handles and labels
plt.legend(handles=handles, labels=labels)

plt.show()

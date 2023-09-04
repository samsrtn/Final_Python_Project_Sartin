# Behavioural data analysis and plotting
## _Python Final Project_
Sartin Samantha, PhD student in Cognitive and Brain Sciences, 37th cycle (2nd year)
Center for Mind/Brain Sciences (CIMeC), University of Trento



As final project I decided to analyse and plot some behavioural data that my collaborators and I collected during the last year. This README.md file is orgnized in the following sections:

- Background: Aim, experimental task, and design
- Raw data organization
- Analyses and plots
- Libraries/Packages

### Background: Aim, experimental task, and design
##### General background and aim of the study
We want to investigate whether haptic size estimation might be processed in brain areas traditionally associated with visual information processing, i.e. the visual cortex. To this aim, in previous experiments we tried to temporarirly disrupt processing in the visual cortex by presenting participants with squared patches of visual noise displayed at the center of a screen while they fixated the center of the screen and haptically explored and estimated the size of three differently sized objects (cylinders). Results were in line with the hypothesis that haptic processing also occurs in visual cortical areas. In fact, we showed significant differences in mean grip aperture (size estimate) between the noise trials and the no noise (i.e., control) trials. Here, we want to assess whether the location of visual noise in the visual field (either on the left or right side, or at the center of the screen) could affect participants' performance in the same stimulus size exploration and estimation task.
##### Experimental task
Participants sat in front of a monitor and they were presented with cylinders of different sizes (in randomized order) which where placed behind the monitor, so that they could not see the simuli. On every trial, subjects were asked to haptically explore one of three differently sized cylinders and to report the size they estimated by openining the thumb and index finger as to match the size previously explored. Thus, the grip aperture was used as a measure of the size estimate. In addition to the stimulus size we also controlled for another variable, that is the location of dynamic visual noise on the screen. In fact, while participants explored the stimulus size and reported the estimated size to the experimenter, a patch of dynamic visual noise was displayed either at the center, on the right or the left side of the screen. We also included a control condition of no noise in which no patch of visual noise was presented on the screen during given trials.
Importantly, participants always kept fixation at the center of the screen throughout the whole experiment and thus never saw the experimental stimuli.
##### Experimental design
We used a 3 by 4 factorial design, with 3 sizes (1-small, 2-medium, 3-large) and 4 noise conditions (LN-left noise, CN-center noise, RN-right noise, and NN-no noise). Sizes 1, 2 and 3 corresponded to: 55 millimiters (mm), 57.5 mm, and 60 mm, respectively. Participants (sample size N: 20) performed a total of 144 trials which were ditributes among our conditions as follows:

| Exp. condition (size - noise) | Number of trials |
| ------ | ------ |
| size 1 - noise L | 16 |
| size 1 - noise C | 16 |
| size 1 - noise R | 16 |
| size 1 - noise NN | 16 |
| size 3 - noise L | 16 |
| size 3 - noise C | 16 |
| size 3 - noise R | 16 |
| size 3 - noise NN | 16 |
| size 2 - noise L | 4 |
| size 2 - noise C | 4 |
| size 2 - noise R | 4 |
| size 2 - noise NN | 4 |
| ------ | ------ |
| TOT: 12 | TOT: 144 |
As you can see here, size 2 conditions had only 4 trials each per subject. The reason is that stimulus size 2 (or medium) was only used as a control to make the task more challenging. As a consequence, participants were forced to rely on stimulus exploration rather than on learning or memory processes in order to extract relevant information about its size. Therefore, size estimates measured during trials requiring haptic exploration of size 2 were not included in the analyses of the mean and standard deviations of our dataset.

### Raw data organization
__Subjects' information__ is stored in an excel file named "__Sub_info.xlsx__". This file contains the following columns:
- _subject_: contains subject number/id (1-20)
- _est_noise_: contains noise that is present in the measurements performed by experimenters using the digital caliper. I will come back to this point in the upcoming section
- _age_: contains the age of each participant

Since we measured grip aperture using a digital caliper, we wanted to make sure that measurements were consistent across trials for each participant. To do this, we marked two small dots on their fingers, one on the thumb and the other on the index finger and we used these as a benchmark to place the tips of the digital caliper and perform the measurement. Since there was always some distance, although subtle, between the small dots and the edge of the fingers, we decided to ask participant to bring together the 2 fingers to measure the distance between the 2 dots which we considered as noise in the size estimation. We did this at the beginning of each trial. By tracking this noise contained in the raw size estimation we were then able to subtract this noise from the measured grip aperture to obtain the final size estimate to consider for the analyses. 

__Raw experimental data__ is stored in an excel file named "__Trial_order.xlsx__". Here, I organized raw data in the following columns:
- _subject_: this column keeps track of the subject number/id (1-20)
- _trial_: this column keeps track of trial number (1-144) for each subject
- _size_: this column specifies the stimulus size (1,2 or 3) that participants were exploring during that specific trial
- _noise_: this column specifies the noise condition (LN, CN, RN, NN) presented in that specific trial
- _raw_est_: this column stores the raw size estimates (i.e., grip apertures) measured by experimenters. To resume what I previously anticipated, these estimates contain what we called the estimation noise discussed above (which is listed in the "est_noise" column of _"Sub_info.xlsx"_). 

### Analyses and plots
I organized analyses and plots in different python files based on the type of analysis and data I was focusing on.

__1) Preprocessing.py__
Here, I performed a general preprocessing of the data. The main steps I took in this python file are:
- loading of the excel files _Sub_info.xlsx_ and _Trial.order.xlsx_; converting these data into separate dataframes
- subtracting the estimate noise (noise_est in df_sub) from the raw estimate (raw_est in df_trials) to obtain the final size estimate (final_est) for subsequent analysis
- detecting and removing outliers from the dataset (data points that are 2.5 standard deviations away from the mean) and saving the new filtered dataset as a new excel file to be able to work on the cleaned data in other python files as well

__2) Averages_noiseXsize_distribution.py__
Here, I created a violin plot to look at the distribution of grip apertures/size estimates for each noise x size combination. The main steps I took in this python file are:
- loading the new filtered excel file _df_trials_wo_outliers.xlsx_
- filtering the dataframe for data associated with sizes 1 and 3 only
- calculating mean of the data (i.e., size estimate/grip aperture) for each size x noise combination
- creating a violin plot to have a look at the distribution of size estimates for each size x noise combination, with customizations including (but not limited to) colors, bars' order, legend and dots representing the mean of size estimates for each size x noise combination

__3) Standard_deviations_noiseXsize_distribution.py__
Here, I created a violin plot to look at the distribution of the standard deviations for each noise x size combination. The main steps I took in this python file are:
- loading the new filtered excel file _df_trials_wo_outliers.xlsx_
- filtering the dataframe for data associated with sizes 1 and 3 only
- calculating the standard deviations (SDs) of size estimates (final_est), for each noise x size combination, for each subject
- calculating mean of SDs of size estimates for each noise x size combination, across subjects
- creating a violin plot to have a look at the distribution of SDs of size estimates for each size x noise combination, with customizations including (but not limited to) colors, bars' order, legend and dots representing the mean SD for each size x noise combination

__4) Averages_noiseXsize.py__
Here, I analysed the average size estimate for each noise (LN, CN, RN, NN) x size (1, 3) combination, across subjects. The main steps I took in this python file are:
- loading the new filtered excel file _df_trials_wo_outliers.xlsx_
- calculating mean, standard deviation and 95% confidence intervals (CI) of the data
- filtering the dataframe for data associated with sizes 1 and 3 only
- creating a bar graph to display the group average size estimates (i.e., grip aperture) for both sizes 1 and 3 and for each noise condition. I also displayed error bars which correspond to the 95% CI previously calculated
- performing statistical comparisons 1) between average grip apertures for sizes 1 and 3, within each noise condition, and 2) between noise conditions, within sizes 1 and 3. Correcting results for multiple comparisons with FRD correction. Statistical significance is also displayed in the bar graph if present.
    - Note: Based on the violin plot I showed in _Averages_noiseXsize_distribution.py_, it appears that not all my data is normally distributed. However, since I still have to thoroughly investigate the distribution of the data, specifically of the difference between the datasets I want to compare, I decided to go for t-tests to complete the project. In the future I may perform nonparametric tests to perform the statistical comparisons I am interested in if further analysis confirms that the normality assumption is not satisfied. This applies also to the analysis of standard deviations and to all analyses I will present from now on.

__5) Averages_across_sizes.py__
Here, I analysed the average size estimate for each noise (LN, CN, RN, NN) irrespective of stimulus size and across subjects. The main steps I took in this python file are:
- loading the new filtered excel file _df_trials_wo_outliers.xlsx_
- filtering the dataframe for data associated with sizes 1 and 3 only
- creating a box plot to show size estimates averaged across sizes and subjects, in all 4 noise conditions
- calculating mean, standard deviation and 95% confidence intervals (CI) of the data to create a bar graph (for an alternative way to visualize data)
- creating a bar graph to display the group average size estimates (ie. grip aperture) for each noise condition irrespective of stimulus size. I also displayed error bars which correspond to the 95% CI previously calculated
- performing statistical comparisons between group average grip apertures for each noise condition, across sizes. Correcting results for multiple comparisons with FRD correction. Statistical significance is also displayed in the bar graph if present.
    - Note: see above.


__6) Standard_deviations_noiseXsize__
Here, I analysed the average standard deviation of size estimates for each noise (L, C, R, NN) x size (1, 3) combination. The main steps I took in this python file are:
- loading the new filtered excel file _df_trials_wo_outliers.xlsx_
- filtering the dataframe for data associated with sizes 1 and 3 only
- calculating the standard deviations (SDs) of size estimates (final_est), for each noise x size combination, for each subject
- calculating mean, SD and 95% confidence intervals (CI) of SDs of size estimates for each noise x size combination, across subjects
- creating a bar graph to display the group average SDs of size estimates for both sizes 1 and 3 and for each noise condition. I also displayed error bars which correspond to the 95% CI previously calculated
- performing statistical comparisons between average SDs of grip apertures for sizes 1 and 3, within each noise condition. Correcting results for multiple comparisons with FRD correction. Statistical significance is also displayed in the bar graph if present.
    - Note: see above.


__7) Standard_deviations_across_sizes__
Here, I analysed the average standard deviation of size estimates for each noise (L, C, R, NN) irrespective of stimulus size and across subjects. The main steps I took in this python file are:
- loading the new filtered excel file _df_trials_wo_outliers.xlsx_
- filtering the dataframe for data associated with sizes 1 and 3 only
- calculating the standard deviations (SDs) of size estimates (final_est), for each noise x size combination, for each subject
- calculating mean, standard deviation and 95% confidence intervals (CI) of SDs of size estimates for each noise condition, across sizes and subjects.
- creating a box plot to show SDs of size estimates for each noise condition, across subjects and sizes
- creating a bar graph (as an alternative way of data visualization) to display the group average SD of size estimates for each noise condition irrespective of stimulus size. I also displayed error bars which correspond to the 95% CI previously calculated
- performing statistical comparisons between group average SD of grip apertures for each noise condition, across sizes. Correcting results for multiple comparisons with FRD correction. Statistical significance is also displayed in the bar graph if present.
    - Note: see above.



### Libraries/Packages
The libraries/packages that were pip installed and used for this project are linked below.

| Library | Documentation |
| ------ | ------ |
| seaborn | https://seaborn.pydata.org/ |
| matplotlib | https://matplotlib.org/ |
| scipy | https://docs.scipy.org/doc/scipy/tutorial/ |
| pandas | https://pandas.pydata.org/ |
| statsmodels | https://www.statsmodels.org/stable/index.html |
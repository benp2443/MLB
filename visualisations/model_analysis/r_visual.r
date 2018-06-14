library('ggplot2')

df <- read.csv('temp1.csv')

ggplot(df, aes(x = value, fill = variable)) +
    geom_density(alpha = 0.6) +
    labs(x = 'Difference', y = 'Density', title = 'Difference Between Naive and Model Accuracy', fill = '')
ggsave('temp1.pdf')

a

df <- read.csv('all_models_results.csv')
sorted_df <- df[order(-df$Count), ]
positions = sorted_df$Model

ggplot(df, aes(x = Model, y = Count)) +
    geom_bar(stat = 'identity', fill = 'steelblue4') +
    scale_x_discrete(limits = positions) +
    scale_y_continuous(breaks = seq(10,110,10)) +
    theme(axis.text.x = element_text(angle = 90)) +
    labs(title = 'Model Performance')
ggsave('all_model_results.pdf')

df <- read.csv('results.csv')

ggplot(df, aes(x = pitch_vol, y = max_value, color = best_model)) +
	geom_point() +
        scale_color_manual(breaks = c('Random Forest', 'Support Vector Machine'),
                           values = c('steelblue4', 'steelblue1'))
ggsave('volatility.pdf')

ggplot(df, aes(x = max_value, y = test_value, color = best_model)) +
	geom_point() +
        scale_color_manual(breaks = c('Random Forest', 'Support Vector Machine'),
                           values = c('steelblue4', 'steelblue1'))
ggsave('train_vs_test_results.pdf')


ggplot(df, aes(x = best_model_std, y = max_value, color = best_model)) +
     geom_point() +
     scale_color_manual(breaks = c('Random Forest', 'Support Vector Machine'),
                        values = c('steelblue4', 'steelblue1'))
ggsave('acc_vs_std.pdf')

ggplot(df, aes(x = pitch_vol, y = best_model_std, color = best_model)) +
     geom_point(aes(size = max_value), alpha = 0.6) +
     scale_color_manual(breaks = c('Random Forest', 'Support Vector Machine'),
                        values = c('steelblue4', 'steelblue1')) +
     guides(size = FALSE) + 
     labs(x = 'Pitch Frequency Volatility', y = 'CV Accuracy Standard Deviation', color = '', title = 'Performance with Volatility')
ggsave('pitchVol_vs_model_std.pdf')


#ggplot(df, aes(x = ave_conf, y = rf)) +
#	geom_point()
#ggsave('pitch_conf.pdf')
#
#ggplot(df, aes(x = train_size, y = rf)) +
#	geom_point()
#ggsave('train_size.pdf')
#
#ggplot(df, aes(x = unique_pitches, y = rf)) +
#	geom_point()
#ggsave('u_pitches.pdf')
#
#ggplot(df, aes(x = start_relief, y = rf)) +
#       geom_boxplot()
#ggsave('s_vs_r.pdf')

df <- read.csv('../../feature_importance_ordered.csv')

ggplot(df, aes(x = variable,  y = value)) +
	geom_boxplot(fill = 'steelblue4') +
	scale_x_discrete(limits = unique(df$variable)) + 
	theme(axis.text.x = element_text(angle = 90)) +
        labs(x = 'Feature', y = 'Value', title = 'Feature Importance')
ggsave('fi_boxplot.pdf')

df <- read.csv('count_accuracy.csv')

order <- c('count_0-2','count_1-2','count_0-1','count_2-2','count_1-1','count_0-0', 'count_2-1','count_1-0','count_3-2','count_2-0','count_3-1','count_3-0')

ggplot(df, aes(x = variable, y = value)) +
    geom_boxplot(fill = 'steelblue4') +
    scale_x_discrete(limits = order) +
    theme(axis.text.x = element_text(angle = 90)) +
    labs(x = 'Count', y = 'Accuracy', title = 'Model Accuracy by Count')
ggsave('count_accuracy.pdf')

##### Probabilities #####

df <- read.csv('average_over_probs.csv')

df$Probability = as.factor(df$Probability)

ggplot(df, aes(x = Probability, y = Correct)) +
    geom_boxplot(fill = 'steelblue4') +
    #scale_y_continuous(breaks = seq(10,100,10)) +
    labs(x = 'Prediction Probability', y = 'Accuracy', title = 'Prediction Probability vs Accuracy')
ggsave('probs_correct.pdf')

##### Left vs Right #####

df <- read.csv('../../left_vs_right_freqs.csv')

ggplot(df, aes(x = difference)) +
    geom_density(fill = 'steelblue4') +
    labs(x = 'Difference', y = 'Density', title = 'Change in Pitch Frequencies - Left vs Right')
ggsave('left_vs_right_diff.pdf')

df <- read.csv('all_pitch_change_LvsR.csv')

ggplot(df, aes(x = variable, y = value)) +
    geom_bar(stat = 'identity', fill = 'steelblue4') +
    labs(x = 'Any Pitch type', y = 'Percent', title = 'Changing Pitch Type frequencies')
ggsave('change_PF_all.pdf')

df <- read.csv('first_pitch_change_LvsR.csv')

ggplot(df, aes(x = variable, y = value)) +
    geom_bar(stat = 'identity', fill = 'steelblue4') +
    labs(x = 'Main Pitch Type', y = 'Percent', title = 'Dominant Pitch Type Change')
ggsave('change_PF_first.pdf')


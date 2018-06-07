library('ggplot2')

df <- read.csv('../../results.csv')

ggplot(df, aes(x = pitch_vol, y = rf)) +
	geom_point()
ggsave('volatility.pdf')

ggplot(df, aes(x = ave_conf, y = rf)) +
	geom_point()
ggsave('pitch_conf.pdf')

ggplot(df, aes(x = train_size, y = rf)) +
	geom_point()
ggsave('train_size.pdf')

ggplot(df, aes(x = unique_pitches, y = rf)) +
	geom_point()
ggsave('u_pitches.pdf')

ggplot(df, aes(x = start_relief, y = rf)) +
       geom_boxplot()
ggsave('s_vs_r.pdf')

df <- read.csv('../../feature_importance_ordered.csv')

ggplot(df, aes(x = variable,  y = value)) +
	geom_boxplot() +
	scale_x_discrete(limits = unique(df$variable)) + 
	theme(axis.text.x = element_text(angle = 90))
ggsave('fi_boxplot.pdf')

df <- read.csv('count_accuracy.csv')

order <- c('count_0-2','count_1-2','count_0-1','count_2-2','count_1-1','count_0-0', 'count_2-1','count_1-0','count_3-2','count_2-0','count_3-1','count_3-0')

ggplot(df, aes(x = variable, y = value)) +
    geom_boxplot() +
    scale_x_discrete(limits = order) +
    theme(axis.text.x = element_text(angle = 90))
ggsave('count_accuracy.pdf')

##### Probabilities #####

df <- read.csv('average_over_probs.csv')

df$Probability = as.factor(df$Probability)

ggplot(df, aes(x = Probability, y = Correct)) +
    geom_boxplot() +
    #scale_y_continuous(breaks = c(10,20,30,40,50,60,70,80,90))
ggsave('probs_correct.pdf')

##### Left vs Right #####

df <- read.csv('../../left_vs_right_freqs.csv')

ggplot(df, aes(x = difference)) +
    geom_density()
ggsave('left_vs_right_diff.pdf')

##### Age vs Accuracy #####

df <- read.csv('age_vs_accuracy.csv')

ggplot(df, aes(x = age, y = rf)) +
    geom_point()
ggsave('age_vs_accuracy.pdf')

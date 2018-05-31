library('ggplot2')

df <- read.csv('pitch_type_confidence.csv')

ggplot(df, aes(x = type_confidence)) +
    geom_density(fill = 'steelblue4') +
    labs(x = 'Classification Probability', y = 'Density', title = 'Pitch Type Probability')
ggsave('pitch_type_confidence.pdf')

df2 <- read.csv('pitchers_count.csv')

df2$confidence <- as.factor(df2$confidence)

ggplot(df2, aes(x = confidence, y = pitchers_count)) +
    geom_bar(stat = 'identity', fill = 'steelblue4') +
    labs(x = 'Probability Thresehold', y = 'Count', title = 'Filtering Pitchers based on Probability Thresehold')
ggsave('pitchers_by_thresehold.pdf')

df3 <- read.csv('pitchers_mean_conf.csv')

ggplot(df3, aes(x = type_confidence)) +
    geom_density(fill = 'steelblue4') +
    labs(x = 'Mean Probability', y = 'Density', title = 'Pitchers Mean Pitch Type Probability')
ggsave('mean_pitch_type_confidence.pdf')

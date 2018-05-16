library('ggplot2')

df <- read.csv('pitch_type_nulls.csv')
temp <- df[df$type == 'Total nulls', ]

ggplot(temp, aes(x = year, y = nulls)) +
    geom_bar(stat = 'identity', fill = 'steelblue4') +
    labs(x = 'Year', y = 'Count', title = 'Nulls Pitch Types By Year')
ggsave('nulls_by_year.pdf')

df2 <- read.csv('nulls_by_game.csv')

df2$year <- as.factor(df2$year)
ggplot(df2, aes(x = year, y = nulls)) +
    geom_boxplot(fill = 'steelblue4', outlier.colour = 'steelblue4') +
    labs(title = 'Nulls Per Game (including only null games)', y = 'Count', x = 'Year')
ggsave('nulls_by_game.pdf')

df3 <- read.csv('consec_nulls.csv')

ggplot(df3, aes(x = consec_nulls)) +
    geom_histogram(binwidth = 1)
ggsave('consec_nulls.pdf')

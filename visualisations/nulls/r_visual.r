library('ggplot2')

df <- read.csv('pitch_type_nulls.csv')
# Need to make the y axis at 250 intervals
ggplot(df, aes(x = year, y = nulls, fill = type)) +
    geom_bar(stat = 'identity', position = position_dodge()) +
    labs(x = 'Year', y = 'Count')
ggsave('nulls_by_year.pdf')

df2 <- read.csv('nulls_by_game.csv')

df2$year <- as.factor(df2$year)
ggplot(df2, aes(x = year, y = nulls)) +
    geom_boxplot()
ggsave('nulls_by_game.pdf')

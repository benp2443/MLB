library('ggplot2')

##### Games played #####
df <- read.csv('games_played.csv')

ggplot(df, aes(x = games_played, fill = StartVsRelief)) +
    geom_density(alpha = 0.3) +
    labs(x = 'Games played', y = 'Density', fill = "Starter's Vs Reliever's")
ggsave('games_played.pdf')

##### Pitches per game #####
df2 <- read.csv('pitch_per_game.csv')

ggplot(df2, aes(x = pitch_count, fill = StartVsRelief)) +
    geom_density(alpha = 0.3) +
    labs(x = 'Pitches thrown in a game', y = 'Density', fill = "Starter's Vs Reliever's")
ggsave('pitchers_per_game.pdf')

##### Total pitches #####
df3 <- read.csv('total_pitches.csv')
    
ggplot(df3, aes(x = StartVsRelief, y = pitch_count)) +
    geom_boxplot() +
    labs(title = "Starter's Vs Reliever's", y = 'Total pitches')
ggsave('total_pitches.pdf')

##### Total pitchers #####
df4 <- read.csv('total_pitchers.csv')

ggplot(df4, aes(x = StartVsRelief, y = Count)) +
    geom_bar(stat = 'identity', fill = 'steelblue') 
ggsave('total_pitchers.pdf')

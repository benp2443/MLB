library('ggplot2')

##### Games played #####
#df <- read.csv('games_played.csv')
#
#ggplot(df, aes(x = games_played, fill = StartVsRelief)) +
#    geom_density(alpha = 0.3) +
#    labs(x = 'Games played', y = 'Density', fill = "Starter's Vs Reliever's")
#ggsave('games_played.pdf')
#
###### Pitches per game #####
#df2 <- read.csv('pitch_per_game.csv')
#
#ggplot(df2, aes(x = pitch_count, fill = StartVsRelief)) +
#    geom_density(alpha = 0.3) +
#    labs(x = 'Pitches thrown in a game', y = 'Density', fill = "Starter's Vs Reliever's")
#ggsave('pitchers_per_game.pdf')
#
###### Total pitches #####
#df3 <- read.csv('total_pitches.csv')
#    
#ggplot(df3, aes(x = StartVsRelief, y = pitch_count)) +
#    geom_boxplot() +
#    labs(title = "Starter's Vs Reliever's", y = 'Total pitches')
#ggsave('total_pitches.pdf')
#
###### Total pitchers #####
#df4 <- read.csv('total_pitchers.csv')
#
#ggplot(df4, aes(x = StartVsRelief, y = Count)) +
#    geom_bar(stat = 'identity', fill = 'steelblue') 
#ggsave('total_pitchers.pdf')

df <- read.csv('players_pre_post_filter.csv')

df$preVspost <- factor(df$preVspost, levels = c('Before filter', 'After filter'))
df$StartVsRelief <- factor(df$StartVsRelief, levels = c('Starter', 'Reliever'))

ggplot(df, aes(x = preVspost, y = count, fill = StartVsRelief)) +
    geom_bar(stat = 'identity', position = position_dodge()) +
    labs(x = '', y = 'Count', title = 'Pitchers Pre and Post Filter', fill = 'Pitcher type') +
    scale_y_continuous(breaks = seq(100,700,100)) +
    scale_fill_manual(values = c('steelblue4', 'steelblue2'))
ggsave('pitcher_filtering.pdf')

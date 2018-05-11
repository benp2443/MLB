library('ggplot2')

#df <- read.csv('pitch_freq.csv')
#
#ggplot(df, aes(x = pitch_id, y = value, group = variable)) +
#    geom_line(aes(color = variable))
#ggsave('pitch_freq.pdf')
#
#df2 <- read.csv('yearly_pitch_freq.csv')
#
#ggplot(df2, aes(x = year, y = value, group = variable)) +
#    geom_line(aes(color = variable))
#ggsave('yearly_pitch_freq.pdf')
#
#df3 <- read.csv('pitcher_vs_batter.csv')
#
#ggplot(df3, aes(x = count)) +
#    geom_histogram(binwidth = 1, fill = 'steelblue') +
#    scale_x_continuous(breaks = seq(0,150,10))
#ggsave('test.pdf')
#
#df4 <- read.csv('ab_vs_batter.csv')
#
#ggplot(df4, aes(x = count)) +
#    geom_histogram(binwidth = 1, fill = 'steelblue') +
#    scale_x_continuous(breaks = seq(0,30,5))
#ggsave('ab_count_vs_batters.pdf')
#
#df5 <- read.csv('pitch_freq_changes.csv')
#
#ggplot(df5, aes(x = pitch_type, y = percentage)) +
#    geom_boxplot()
#ggsave('pitch_freq_between_games.pdf')
#
#ggplot(df5, aes(x = game_id, y = percentage, group = pitch_type)) +
#    geom_line(aes(color = pitch_type))
#ggsave('test.pdf')
#
#df6 <- read.csv('pitch_freq_yearly_changes.csv')
#
#ggplot(df6, aes(x = year, y = percentage, group = pitch_type)) +
#    geom_line(aes(color = pitch_type))
#ggsave('test2.pdf')
#
#df7 <- read.csv('volatility.csv')
#
#ggplot(df7, aes(x = change_value)) +
#    geom_density(fill = 'steelblue')
#ggsave('pitcher_volatility.pdf')
#
#df8 <- read.csv('top_vol.csv')
#
#unique_pitchers <- unique(df8[, 'pitcher_id'])
#
#for (pitcher in unique_pitchers) {
#    df <- df8[df8$pitcher_id == pitcher, ]
#
#    ggplot(df, aes(x = pitch_type, y = percent, fill = train_test)) +
#        geom_bar(stat = 'identity', position = position_dodge()) 
#
#    filename <- paste('vol', pitcher, sep = '_')
#    ggsave(paste(filename, 'pdf', sep = '.'))   
#}
#ggplot(df8, aes(x = pitch_type, y = percent, fill = train_test)) +
#    geom_bar(stat = 'identity', position = position_dodge()) +
#    facet_grid(pitcher_id ~ .)
#ggsave('test.pdf')

#df9 <- read.csv('pitch_frequencies_change.csv')
#
#ggplot(df9, aes(x = game_id, y = value, group = variable)) +
#    geom_line(aes(color = variable)) +
#    theme(axis.ticks.x = element_blank(),
#          axis.text.x = element_blank())
#ggsave('test2.pdf')

df10 <- read.csv('pitch_frequencies_windows.csv')

curve <- c('w_40_CU_percent', 'w_120_CU_percent', 'w_360_CU_percent')
temp <- df10[df10$variable %in% curve, ]

ggplot(temp, aes(x = game_id, y = value, group = variable)) +
    geom_line(aes(color = variable)) +
    theme(axis.ticks.x = element_blank(),
          axis.text.x = element_blank())
ggsave('test3.pdf')

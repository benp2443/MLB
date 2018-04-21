library('ggplot2')

df <- read.csv('pitch_type_count.csv')

sorted_df <- df[order(-df$count), ]
positions <- sorted_df$pitch_type

ggplot(df, aes(x = pitch_type, y = count)) +
    geom_bar(stat = 'identity', fill = 'steelblue') +
    scale_x_discrete(limits = positions) +
    scale_y_continuous(breaks = seq(0,425000, 50000))
ggsave('pitch_type_count.pdf')

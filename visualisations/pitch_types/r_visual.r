library('ggplot2')

df <- read.csv('pitch_types_count.csv')

sorted_df <- df[order(-df$count), ]
positions <- sorted_df$pitch_type

ggplot(df, aes(x = pitch_type, y = count)) +
    geom_bar(stat = 'identity', fill = 'steelblue4') +
    scale_x_discrete(limits = positions) +
    labs(x = 'Pitch Type', y = 'Count', title = 'Pitch Type Count')
ggsave('pitch_type_count.pdf')


df3 <- read.csv('pitch_groupings_2.csv')
sorted_df <- df3[order(df3$count), ]
positions <- sorted_df$group

ggplot(df3, aes(x = group, y = count)) +
   geom_bar(stat = 'identity', fill = 'steelblue4', width = 0.6) +
   scale_x_discrete(limits = positions) +
   theme(axis.text.x = element_text(angle = 90)) +
   coord_flip() +
   labs(y = 'Count', x = 'Pitch Group', title = 'Count Of Each Pitch Grouping')
ggsave('grouped_pitch_type_count_2.pdf')

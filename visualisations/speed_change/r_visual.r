library('ggplot2')

df <- read.csv('FF_speed.csv')

df$pitch_count_bucket = as.factor(df$pitch_count_bucket)

ggplot(df, aes(x = pitch_count_bucket, y = start_speed)) +
    geom_boxplot() 
ggsave('FF_over_buckets.pdf')

df <- read.csv('../../individual_df/112526.csv')

pitch_types <- unique(df$pitch_type)
print(pitch_types)
for (pitch in pitch_types) {
    print(pitch)
    temp <- df[df$pitch_type == pitch, ]
    print(sd(temp$start_speed))
    ggplot(temp, aes(x = start_speed)) +
        geom_density(fill = 'steelblue')
    name = paste(pitch, 'pdf', sep = '.')
    ggsave(name)
}



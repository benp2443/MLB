library('ggplot2')

df <- read.csv('pitch_freq.csv')

ggplot(df, aes(x = pitch_id, y = value, group = variable)) +
    geom_line(aes(color = variable))
ggsave('pitch_freq.pdf')

library('ggplot2')

df <- read.csv('pitch_freq.csv')

ggplot(df, aes(x = pitch_id, y = value, group = variable)) +
    geom_line(aes(color = variable))
ggsave('pitch_freq.pdf')

df2 <- read.csv('yearly_pitch_freq.csv')

ggplot(df2, aes(x = year, y = value, group = variable)) +
    geom_line(aes(color = variable))
ggsave('yearly_pitch_freq.pdf')

df3 <- read.csv('pitcher_vs_batter.csv')

ggplot(df3, aes(x = count)) +
    geom_histogram(binwidth = 1, fill = 'steelblue') +
    scale_x_continuous(breaks = seq(0,150,10))
ggsave('test.pdf')

df4 <- read.csv('ab_vs_batter.csv')

ggplot(df4, aes(x = count)) +
    geom_histogram(binwidth = 1, fill = 'steelblue') +
    scale_x_continuous(breaks = seq(0,30,5))
ggsave('ab_count_vs_batters.pdf')

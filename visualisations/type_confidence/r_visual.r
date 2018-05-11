library('ggplot2')

df <- read.csv('pitches_by_count.csv')

df$thresehold <- as.factor(df$thresehold)

ggplot(df, aes(x = thresehold, y = count)) +
    geom_boxplot(fill = 'steelblue') + 
    scale_y_continuous(breaks = seq(0,20000,1000))
ggsave('test.pdf')

df2 <- read.csv('pitchers_count.csv')

df2$confidence <- as.factor(df2$confidence)

ggplot(df2, aes(x = confidence, y = pitchers)) +
    geom_bar(stat = 'identity', fill = 'steelblue')
ggsave('pitchers_by_thresehold.pdf')

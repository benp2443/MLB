library('ggplot2')

df <- read.csv('type_confidence.csv', header = TRUE)

ggplot(df, aes(x = type_confidence)) +
	geom_density()
ggsave(filename = 'type_confidence_density.pdf')

df <- read.csv('per_pitch_confidence.csv')
df <- subset(df, pitcher_id == 462382)

ggplot(df, aes(x = pitch_type, y = type_confidence)) +
       geom_bar(stat = 'identity', fill = 'steelblue')
ggsave(filename = 'bar.pdf')	

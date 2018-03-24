library('ggplot2')

df <- read.csv('type_confidence.csv', header = FALSE, col.names = 'mean_type_confidence')

ggplot(df, aes(x = mean_type_confidence)) +
	geom_density()
ggsave(filename = 'type_confidence_density.pdf')

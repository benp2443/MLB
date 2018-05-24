library('ggplot2')
library('gridExtra')
library('dplyr')


args = commandArgs(trailingOnly = TRUE)


pitch_density <- function(df, id) {
	density_plot <- ggplot(df, aes(x = type_confidence, color = pitch_type)) + 
	#	geom_freqpoly(aes(y = ..count../sum(..count..))) 
		geom_density()
	return(density_plot)
}

for (pitcher in args) {
    df = read.csv(pitcher)
    conf_denst = pitch_density(df)
    lists = strsplit(pitcher, '/')
    player = lists[[1]][5]
    player_num = strsplit(player, '_')
    saveas = paste(player_num[[1]][1], 'pitch_conf_density.pdf', sep = '_')
    ggsave(filename = saveas, plot = conf_denst)
}


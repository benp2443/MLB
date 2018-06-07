library('ggplot2')
library('gridExtra')
library('dplyr')


pitch_viz <- function(df, saveas) {

	temp <- df %>% 
		group_by(pitch_type) %>%
		sample_n(50, replace = TRUE)

	plot_1 <- ggplot(temp, aes(x = pfx_x, y = pfx_y, color = pitch_type)) +
		geom_point(shape = 1) +
                labs(colour = "") +
		stat_ellipse() +
		labs(x = 'Horizontal Movement', y = 'Vertical Movement')

	plot_2 <- ggplot(temp, aes(x = pfx_x, y = start_speed, color = pitch_type)) +
		geom_point(shape = 1) + 
                labs(colour = "") +
		stat_ellipse() +
		labs(x = 'Horizontal Movement', y = 'Pitch Speed (MPH)')

	plot_3 <- ggplot(temp, aes(x = pfx_x, y = pfx_y, color = group_pitch_type)) +
		geom_point(shape = 1) +
                labs(colour = "") +
		stat_ellipse() +
		labs(x = 'Horizontal Movement', y = 'Vertical Movement')

	plot_4 <- ggplot(temp, aes(x = pfx_x, y = start_speed, color = group_pitch_type)) +
		geom_point(shape = 1) + 
                labs(colour = "") +
		stat_ellipse() +
		labs(x = 'Horizontal Movement', y = 'Pitch Speed (MPH)')

	together = grid.arrange(plot_1, plot_2, plot_3, plot_4, nrow = 2, ncol = 2)
	ggsave(filename = saveas, plot = together)
}

pitch_density <- function(df, saveas, title_) {

        df[ , 'type_confidence'] = df[ , 'type_confidence']/2

	density_plot <- ggplot(df, aes(x = type_confidence, color = pitch_type)) + 
	#	geom_freqpoly(aes(y = ..count../sum(..count..))) 
		geom_density() +
                labs(x = 'Classification Confidence', y = 'Density', title = title_)
	#return(density_plot)
        ggsave(filename = saveas)
}


#args = commandArgs(trailingOnly = TRUE)
#
#for (i in args) {
#    print(i)
#
#    # Pitch clustering graphs
#    df = read.csv(i)
#    lists = strsplit(i, '/')
#    player = lists[[1]][5]
#    player_num = strsplit(player, '_')
#    saveas = paste(player_num[[1]][1], 'pitch_group_3.pdf', sep = '_')
#    pitch_viz(df, saveas)
#
#    # Pitch confidence densities
#    #conf_denst = pitch_density(df)
#    #saveas = paste(player_num[[1]][1], 'pitch_conf_density.pdf', sep = '_')
#    #ggsave(filename = saveas, plot = conf_denst)
#
#}



pitch_viz <- function(df, saveas1, title1, saveas2, title2) {

	temp <- df %>% 
		group_by(pitch_type) %>%
		sample_n(50, replace = TRUE)

	plot_1 <- ggplot(temp, aes(x = pfx_x, y = pfx_y, color = pitch_type)) +
		geom_point(shape = 1) +
                labs(colour = "") +
		stat_ellipse() +
		labs(x = 'Horizontal Movement', y = 'Vertical Movement')

	plot_2 <- ggplot(temp, aes(x = pfx_x, y = start_speed, color = pitch_type)) +
		geom_point(shape = 1) + 
                labs(colour = "") +
		stat_ellipse() +
		labs(x = 'Horizontal Movement', y = 'Pitch Speed (MPH)')

	together = grid.arrange(plot_1, plot_2, nrow = 1, ncol = 2, top = title1)
	ggsave(filename = saveas1, plot = together)

	plot_3 <- ggplot(temp, aes(x = pfx_x, y = pfx_y, color = group_pitch_type)) +
		geom_point(shape = 1) +
                labs(colour = "") +
		stat_ellipse() +
		labs(x = 'Horizontal Movement', y = 'Vertical Movement')

	plot_4 <- ggplot(temp, aes(x = pfx_x, y = start_speed, color = group_pitch_type)) +
		geom_point(shape = 1) + 
                labs(colour = "") +
		stat_ellipse() +
		labs(x = 'Horizontal Movement', y = 'Pitch Speed (MPH)')

	together = grid.arrange(plot_3, plot_4, nrow = 1, ncol = 2, top = title2)
	ggsave(filename = saveas2, plot = together)

}


df = read.csv('../../individual_df/527048.csv')
df2 = read.csv('../../individual_df/453265.csv')

pitch_viz(df, 'perez_low_conf.pdf', 'Perez - Pitch types by Movement and Speed', 'perez_low_conf_group.pdf', 'Perez - Grouped Pitch types by Movement and Speed')
pitch_density(df, 'perez_density.pdf', 'Perez - Pitch Type Confidence') 

pitch_viz(df2, 'watson_low_conf.pdf', 'Watson - Pitch types by Movement and Speed', 'watson_low_conf_group.pdf', 'Watson - Grouped Pitch types by Movement and Speed')
pitch_density(df2, 'watson_density.pdf', 'Watson - Pitch Type Confidence') 

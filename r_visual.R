library('ggplot2')
library('gridExtra')
library('dplyr')

# Average confidence density
df <- read.csv('type_confidence.csv', header = TRUE)

ggplot(df, aes(x = type_confidence)) +
	geom_density()
ggsave(filename = 'type_confidence_density.pdf')

# Sampled pitchers per pitch confidence densities
df <- read.csv('per_pitch_confidence.csv')

pitch_density <- function(df, id) {
	df <- subset(df, pitcher_id == id)
	density_plot <- ggplot(df, aes(x = type_confidence, color = pitch_type)) + 
	#	geom_freqpoly(aes(y = ..count../sum(..count..))) 
		geom_density()
	return(density_plot)
}

pitcher_ids = c(465657, 593372, 543144, 434378)

for (pitcher in pitcher_ids) {
	test = pitch_density(df, pitcher)
	name = paste(pitcher, 'density.pdf', sep = '_')
	ggsave(filename = name, plot = test)
}

#test <- pitch_density(df, 593372)
#ggsave(filename = '593372_density.pdf', plot = test)

# Pitch visualisation
df <- read.csv('per_pitch_confidence.csv')

pitch_viz <- function(df, id, saveas) {
	temp <- subset(df, pitcher_id = id)
	ggplot(temp, aes(x = pfx_x, y = pfx_z, color = start_speed, shape = pitch_type)) +
		geom_point() +
		stat_ellipse()
	ggsave(filename = saveas)
}

pitch_viz(df, 543144, '543133.pdf')
pitch_viz(df, 434378, '434378.pdf')


# Subset Pitch Visualisation
#temp <- df[, c('pitcher_id', 'class')]
#temp <- temp[!duplicated(temp), ]
#rownames(temp) <- 1:nrow(temp)
#
#high_conf_pitchers = c()
#low_conf_pitchers = c()
#
#i = 1
#while (i <= nrow(temp)) {
#	pitcher_id = temp[i, 'pitcher_id']
#	class = temp[i, 'class']
#
#	if (class == 'top') {
#		high_conf_pitchers = c(high_conf_pitchers, pitcher_id)
#	} else {
#		low_conf_pitchers = c(low_conf_pitchers, pitcher_id)
#	}
#	i = i + 1
#}
#
#pitch_viz <- function(df, id, saveas) {
#	temp <- subset(df, pitcher_id == id)
#	temp <- df %>% 
#		group_by(pitch_type) %>%
#		sample_n(100)
#	ggplot(temp, aes(x = pfx_x, y = pfx_z, color = start_speed, shape = pitch_type)) +
#		geom_point() +
#		stat_ellipse() +
#		labs(title = paste(pitcher_id, '- Pitch Types', sep = ' '))
#	ggsave(filename = saveas)
#}
#
#pitch_viz(df, high_conf_pitchers[1], '1_pitchviz.pdf')
#pitch_viz(df, high_conf_pitchers[2], '2_pitchviz.pdf')
#pitch_viz(df, high_conf_pitchers[3], '3_pitchviz.pdf')
#pitch_viz(df, high_conf_pitchers[4], '4_pitchviz.pdf')
#
#i = 1
#while (i < 5) {
#	pitch_viz(df, low_conf_pitchers[i], paste(i + 4, 'pitchviz.pdf', sep = '_'))
#	i = i + 1
#}


# Side by side


pitch_viz <- function(df, id, saveas) {
	df2 <- subset(df, pitcher_id == id)

	temp <- df2 %>% 
		group_by(pitch_type) %>%
		sample_n(100)

	plot_1 <- ggplot(temp, aes(x = pfx_x, y = pfx_z, color = pitch_type)) +
		geom_point(shape = 1) +
		stat_ellipse() +
		labs(x = 'Horizontal Movement', y = 'Vertical Movement')

	plot_2 <- ggplot(temp, aes(x = pfx_x, y = start_speed, color = pitch_type)) +
		geom_point(shape = 1) + 
		stat_ellipse() +
		labs(x = 'Horizontal Movement', y = 'Pitch Speed (MPH)')

	#plot_3 <- pitch_density(df, id)

	together = grid.arrange(plot_1, plot_2, ncol = 2)
	ggsave(filename = saveas, plot = together)
}

pitch_viz(df, 543144, '543144_scatter.pdf')
pitch_viz(df, 434378, '434378_scatter.pdf')

#i = 1
#while (i < 9) {
#	if (i < 5) {
#		pitch_viz(df, low_conf_pitchers[i], paste(i, 'pitchviz.pdf', sep = '_'))
#		i = i + 1
#	} else {
#		pitch_viz(df, high_conf_pitchers[i-4], paste(i, 'pitchviz.pdf', sep = '_'))
#		i = i + 1
#	}
#}

# Test
df5 <- read.csv('delete.csv')

pitch_viz <- function(df, id, saveas) {
	df2 <- subset(df, pitcher_id == id)

	temp <- df2 %>% 
		group_by(pitch_type) %>%
		sample_n(100)

	plot_1 <- ggplot(temp, aes(x = pfx_x, y = pfx_z, color = pitch_type)) +
		geom_point(shape = 1) +
		stat_ellipse() +
		labs(x = 'Horizontal Movement', y = 'Vertical Movement')

	plot_2 <- ggplot(temp, aes(x = pfx_x, y = start_speed, color = pitch_type)) +
		geom_point(shape = 1) + 
		stat_ellipse() +
		labs(x = 'Horizontal Movement', y = 'Pitch Speed (MPH)')

	plot_4 <- ggplot(temp, aes(x = pfx_x, y = pfx_z, color = cluster)) +
		geom_point(shape = 1) +
		stat_ellipse() +
		labs(x = 'Horizontal Movement', y = 'Vertical Movement')

	plot_5 <- ggplot(temp, aes(x = pfx_x, y = start_speed, color = cluster)) +
		geom_point(shape = 1) + 
		stat_ellipse() +
		labs(x = 'Horizontal Movement', y = 'Pitch Speed (MPH)')

	together = grid.arrange(plot_1, plot_2, plot_4, plot_5, nrow = 2, ncol = 2)
	ggsave(filename = saveas, plot = together)
}

pitch_viz(df5, 465657, '465657_scatter.pdf')
pitch_viz(df5, 593372, '593372_scatter.pdf')

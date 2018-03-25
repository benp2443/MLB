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
		geom_density() 
	return(density_plot)
}

test <- pitch_density(df, 523260)
ggsave(filename = 'test.pdf', plot = test)


test <- pitch_density(df, 501381)
ggsave(filename = 'test2.pdf', plot = test)

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
temp <- df[, c('pitcher_id', 'class')]
temp <- temp[!duplicated(temp), ]
rownames(temp) <- 1:nrow(temp)

high_conf_pitchers = c()
low_conf_pitchers = c()

i = 1
while (i <= nrow(temp)) {
	pitcher_id = temp[i, 'pitcher_id']
	class = temp[i, 'class']

	if (class == 'top') {
		high_conf_pitchers = c(high_conf_pitchers, pitcher_id)
	} else {
		low_conf_pitchers = c(low_conf_pitchers, pitcher_id)
	}
	i = i + 1
}

pitch_viz <- function(df, id, saveas) {
	temp <- subset(df, pitcher_id == id)
	temp <- df %>% 
		group_by(pitch_type) %>%
		sample_n(100)
	ggplot(temp, aes(x = pfx_x, y = pfx_z, color = start_speed, shape = pitch_type)) +
		geom_point() +
		stat_ellipse() +
		labs(title = paste(pitcher_id, '- Pitch Types', sep = ' '))
	ggsave(filename = saveas)
}

pitch_viz(df, high_conf_pitchers[1], '1_pitchviz.pdf')
pitch_viz(df, high_conf_pitchers[2], '2_pitchviz.pdf')
pitch_viz(df, high_conf_pitchers[3], '3_pitchviz.pdf')
pitch_viz(df, high_conf_pitchers[4], '4_pitchviz.pdf')

i = 1
while (i < 5) {
	pitch_viz(df, low_conf_pitchers[i], paste(i + 4, 'pitchviz.pdf', sep = '_'))
	i = i + 1
}


# Side by side


pitch_viz <- function(df, id, saveas) {
	df2 <- subset(df, pitcher_id == id)

	temp <- df2 %>% 
		group_by(pitch_type) %>%
		sample_n(100)

	plot_1 <- ggplot(temp, aes(x = pfx_x, y = pfx_z, color = pitch_type)) +
		geom_point() +
		stat_ellipse() +
		labs(x = 'Horizontal Movement', y = 'Vertical Movement')

	plot_2 <- ggplot(temp, aes(x = pfx_x, y = start_speed, color = pitch_type)) +
		geom_point() + 
		stat_ellipse() +
		labs(x = 'Horizontal Movement', y = 'Pitch Speed (MPH)')

	plot_3 <- pitch_density(df, id)

	together = grid.arrange(plot_1, plot_2, plot_3, nrow = 2, ncol = 2)
	ggsave(filename = saveas, plot = together)
}

pitch_viz(df, high_conf_pitchers[1], 'sideByside_1.pdf')
pitch_viz(df, high_conf_pitchers[4], 'sideByside_2.pdf')



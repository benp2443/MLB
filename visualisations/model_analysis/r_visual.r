library('ggplot2')

df <- read.csv('test.csv')

ggplot(df, aes(x = max_value, y = pitch_vol)) +
	geom_point()
ggsave('volatility.pdf')

ggplot(df, aes(x = max_value, y = ave_conf)) +
	geom_point()
ggsave('pitch_conf.pdf')

ggplot(df, aes(x = max_value, y = sd_conf)) +
	geom_point()
ggsave('sd.pdf')

ggplot(df, aes(x = max_value, y = train_size)) +
	geom_point()
ggsave('train_size.pdf')

ggplot(df, aes(x = max_value, y = unique_pitches)) +
	geom_point()
ggsave('u_pitches.pdf')

ggplot(df, aes(x = start_relief, y = max_value)) +
       geom_boxplot()
ggsave('s_vs_r.pdf')	

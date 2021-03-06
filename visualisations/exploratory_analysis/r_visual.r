library('ggplot2')

df <- read.csv('count_pitches_to_batter.csv')

ggplot(df, aes(x = count)) +
    geom_density(fill = 'steelblue4') +
    labs(x = 'Count', y = 'Density', title = 'Pitches thrown to individual batter')
ggsave('count_to_batter.pdf')

print(median(df[['count']]))
aa


##### Left vs Right #####
df <- read.csv('handedness.csv')

ggplot(df, aes(x = hand, y = count)) +
    geom_bar(stat = 'identity', fill = 'steelblue4') +
    labs(x = 'Hand', y = 'Count', title = 'Handedness of Pitcher')
ggsave('handedness.pdf')

##### Games Played #####
df <- read.csv('games_played.csv')

ggplot(df, aes(x = count, fill = StarterVsCloser)) +
    geom_density(alpha = 0.4) +
    labs(x = 'Count', y = 'Density', fill = '', title = 'Games Played')
ggsave('games_played.pdf')

##### Pitches Per Game #####
df <- read.csv('pitches_per_game.csv')

ggplot(df, aes(x = count, fill = StarterVsCloser)) +
    geom_density(alpha = 0.4) +
    labs(x = 'Count', y = 'Density', fill = '', title = 'Pitches Thrown Per Game')
ggsave('pitches_per_game.pdf')

##### Number of Pitch Types #####
df <- read.csv('pitch_type_counts.csv')

ggplot(df, aes(x = StarterVsCloser, y = count)) +
    geom_boxplot(fill = 'steelblue4') +
    labs(x = 'Starter vs Closer', y = 'Count', title = 'Number of Pitch Types')
ggsave('number_of_pitch_types.pdf')

##### Teams #####
df <- read.csv('teams.csv')
sorted_df <- df[order(-df$count), ]
positions = sorted_df$team

ggplot(df, aes(x = team, y = count)) +
    geom_bar(stat = 'identity', fill = 'steelblue4', width = 0.85) +
    scale_x_discrete(limits = positions) +
    theme(axis.text.x = element_text(angle = 90)) +
    labs(x = 'Team', y = 'Count', title = 'Pitchers Per Team')
ggsave('teams.pdf')

##### Pitch Types Count #####
df <- read.csv('pitch_types.csv')
sorted_df <- df[order(-df$Count), ]
positions = sorted_df$Pitch_Type

ggplot(df, aes(x = Pitch_Type, y = Count)) +
    geom_bar(stat = 'identity', fill = 'steelblue4', width = 0.85) +
    scale_x_discrete(limits = positions) +
    theme(axis.text.x = element_text(angle = 90)) +
    labs(x = 'Grouped Pitch Type', y = 'Count', title = 'Grouped Pitch Type Count')
ggsave('grouped_pitch_types_count.pdf')

library('ggplot2')

##### Left vs Right #####
df <- read.csv('handedness.csv')

ggplot(df, aes(x = hand, y = count)) +
    geom_bar(stat = 'identity', fill = 'steelblue4')
ggsave('handedness.pdf')

##### Games Played #####
df <- read.csv('games_played.csv')

ggplot(df, aes(x = count, fill = StarterVsCloser)) +
    geom_density()
ggsave('games_played.pdf')

##### Pitches Per Game #####
df <- read.csv('pitches_per_game.csv')

ggplot(df, aes(x = count, fill = StarterVsCloser)) +
    geom_density()
ggsave('pitches_per_game.pdf')

##### Number of Pitch Types #####
df <- read.csv('pitch_type_counts.csv')

ggplot(df, aes(x = StarterVsCloser, y = count)) +
    geom_boxplot(fill = 'steelblue4')
ggsave('number_of_pitch_types.pdf')

##### Teams #####
df <- read.csv('teams.csv')

ggplot(df, aes(x = team, y = count)) +
    geom_bar(stat = 'identity', fill = 'steelblue4')
ggsave('teams.pdf')

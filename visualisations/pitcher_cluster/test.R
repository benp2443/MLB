
str <- '../../individual_df/fe/112526_fe.csv'

lists = strsplit(str, '/')

player = lists[[1]][5]

player_num = strsplit(player, '_')

saveas = paste(player_num[[1]][1], 'pitch_group.pdf', sep = '_')
print(saveas)

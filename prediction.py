import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn import metrics
from sklearn.svm import LinearSVC
from sklearn import svm
from sklearn.multiclass import OneVsOneClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import KFold
#import keras
#from keras.models import Sequential
#from keras.layers import Dense
#from sklearn.cross_validation import KFold
import sys
import argparse

pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 300)

parser = argparse.ArgumentParser()
parser.add_argument('--input', nargs = '+', help = 'input data path')
args = parser.parse_args()

final_df = pd.DataFrame(columns = ['pitcher_id', 'rf', 'pitch_vol', 'ave_conf', 'sd_conf', 'train_size', 'unique_pitches', 'start_relief'])
feature_importance_list = []
count_accuracy_all = []
all_prob_pred_array = np.empty([0,3])

for pitcher in args.input:
    
    # Read in pitcher dataframe
    print(pitcher)
    sys.stdout.flush()
    df = pd.read_csv(pitcher)
    pitcher = df['pitcher_id'].unique()[0]
    s_or_r = df['StartVsRelief'].unique()[0]

    ## Create train_test column -> put this in feature eng
    df = df.loc[df['year'] != 2014, :]
    train_test = {2015:'train', 2016:'train', 2017:'test'}
    df['train_test'] = df['year'].map(train_test)

    #df = df.loc[df['type_confidence'] >= 1.5, :]
    #new_counts = df.groupby('year')['home_team'].count().reset_index()
    #u_years = new_counts['year'].unique()

    #if 2016 not in u_years or 2017 not in u_years:
    #    cut_pitchers += 1
    #    continue

    ave_confidence = np.mean(df.loc[df['train_test'] == 'train', 'type_confidence']/2)
    sd_confidence = np.std(df.loc[df['train_test'] == 'train', 'type_confidence']/2)

    # Drop unwanted columns and 2014 -> make this cleaner through the pipeline
    drop = ['Unnamed: 0', 'game_id', 'game_type', 'home_team', 'home_league', \
            'away_team', 'away_league', 'stadium', 'city', 'inning', 'inning_half', \
            'ab_game_num', 'batter_id', 'pitcher_id', 'ab_event_number', 'ab_event', \
            'p_description', 'type_', 'event_num', 'game_shift', 'StartVsRelief', 'new_game',\
            'start_speed', 'sz_top', 'sz_bot', 'pfx_x', 'pfx_y', 'px', 'py', 'year',\
            'pitch_type', 'type_confidence', 'zone', 'weighted_total_pitches',\
            'pitch_sequence', 'outs', 'batter_specific_count', 'prior_pitch', 'prior_speed']

    
    df.drop(drop, axis = 1, inplace = True)
    df.replace(np.inf, np.nan, inplace = True)
    df.fillna(method = 'ffill', inplace = True)
    df.fillna(method = 'bfill', inplace = True)

    cat_vars = df.select_dtypes(include = ['object']).columns.tolist()
    cat_vars.remove('group_pitch_type')
    cat_vars.remove('train_test')
   
    for col in cat_vars:
        dummies = pd.get_dummies(df[col], prefix = col, drop_first = True)
        df = pd.concat([df, dummies], axis = 1)
        df.drop(col, axis = 1, inplace = True)

    ## Find X and y variables for train and test
    y_train = df.loc[df['train_test'] == 'train', 'group_pitch_type']
    temp = df.drop(['group_pitch_type'], axis = 1)
    X_train = temp.loc[temp['train_test'] == 'train', :]
    #if len(X_train) < 200:
    #    continue
    y_test = df.loc[df['train_test'] == 'test', 'group_pitch_type']
    X_test = temp.loc[temp['train_test'] == 'test', :]
    
    X_train.drop(['train_test'], axis = 1, inplace = True)
    X_test.drop(['train_test'], axis = 1, inplace = True)
    #if len(X_test) < 100:
    #    continue
    train_counts = y_train.value_counts().reset_index()
    most_freq = train_counts.iloc[0,0]
    naive_preds = np.repeat(most_freq, len(y_test))
    naive_acc = np.sum(naive_preds == y_test.values)/float(len(y_test))

    fi_cols = ['on_first', 'on_second', 'on_third', 'outs', 'pitch_count', \
               'ab_pitch_count', 'prior_px', 'prior_py', 'score_diff', 'hand', \
               'a_global_PP', 'b_global_weighted_PP', 'c_40_PP', 'd_120_PP', \
               'e_360_PP', 'f_PP_to_batter', 'runner_on', 'weighted_runners_on', \
               'prior_group_pitch_type', 'count_', 'home_or_away_']

    cols = X_train.columns.values.tolist()

    dummys = ['a_', 'b_', 'c_', 'd_', 'e_', 'f_', 'prior_group_pitch_type', 'count_']

    dummys_idx_dict = {}

    for dummy in dummys:
        for col in cols:

            if col.startswith(dummy):
                idx = cols.index(col)
                if dummy in dummys_idx_dict:
                    dummys_idx_dict[dummy] += [idx]
                else:
                    dummys_idx_dict[dummy] = [idx]

    count_cols_idx = []
    for col in cols:
        if col.startswith('count_'):
            count_cols_idx.append(cols.index(col))

    cols_for_count_accuracy = cols + ['preds_comp']

    # Feature scaling
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    kf = KFold(n_splits = 5)

    def accuracy(predictions, y_true):
        return np.sum(predictions == y_true)/float(len(y_true))

    def pitch_volatility(y_train_array, y_test_array):
        y_train_fold = pd.DataFrame(y_train_array, columns = ['pitch_type'])
        y_train_fold['count'] = 0
        y_test_fold = pd.DataFrame(y_test_array, columns = ['pitch_type'])
        y_test_fold['count'] = 0

        y_train_counts = y_train_fold.groupby('pitch_type').count().reset_index()
        y_test_counts = y_test_fold.groupby('pitch_type').count().reset_index()

        y_train_counts['percent_train'] = y_train_counts['count']/np.sum(y_train_counts['count'])
        y_test_counts['percent_test'] = y_test_counts['count']/np.sum(y_test_counts['count'])

        merged_df = y_train_counts.merge(y_test_counts, how = 'outer', on = 'pitch_type')
        merged_df['sq_diff'] = np.square(merged_df['percent_train'] - merged_df['percent_test'])
        change = np.sqrt(np.mean(merged_df['sq_diff']))

        return change

    def train_size(y_train_array):
        return len(y_train_array)

    def number_pitch_types(y_train_array):
        return len(np.unique(y_train_array))

    def add_dropped_dummy(x):
        if x == 0:
            return 1
        else:
            return 0

    def convert_dummy_to_binary(x):
        if x > 0.0:
            return 1
        else:
            return 0

    def count_accuracy(X_train, y_train, X_val, y_val, preds_comp, cols_, dummy_cols, startswith):
        preds_comp = preds_comp.reshape(len(y_val), 1)

        temp_X = np.concatenate([X_val, preds_comp], axis = 1)
        temp_df = pd.DataFrame(temp_X, columns = cols_)

        # Add back in dropped dummy variable
        dropped_dummy_str = startswith + 'dummy'
        
        # Normalisation converted to not 1 and 0. Convert back
        temp2_df = temp_df.iloc[:, dummy_cols]
        temp2_df = temp2_df.applymap(convert_dummy_to_binary)

        # Find sum of the rows. If 1, make the dropped dummy column 0 else, 1
        temp2_df['sum'] = np.sum(temp2_df, axis = 1)
        temp2_df[dropped_dummy_str] = temp2_df['sum'].apply(add_dropped_dummy)
        temp2_df.drop('sum', axis = 1, inplace = True)

        # Find idx values of all the dummy cols
        dummy_cols_all_idx = dummy_cols + [temp_df.shape[1] -1]

        final = pd.concat([temp2_df, temp_df.loc[:, 'preds_comp']], axis = 1)
        
        melted_final = pd.melt(final, id_vars = ['preds_comp'])
        melted_final = melted_final.loc[melted_final['value'] == 1, :]
        grouped_m_final = melted_final.groupby('variable')['preds_comp'].mean().reset_index()
        grouped_m_final.rename(columns = {'preds_comp':'mean'}, inplace = True)
        grouped_m_final = grouped_m_final.sort_values('variable', ascending = False)

        return grouped_m_final

    def prediction(model, others_boolean, model_name = 'rf', kfold_object = kf, X_array = X_train, y_array = y_train, naive_pred = most_freq):
        accuracy_list = []
        vol_list = []
        train_size_list = []
        number_pitches_list = []
        feature_importances = []
        count_accuracy_player = []
        player_prob_pred_array = np.empty([0,3])

        for train_index, test_index in kf.split(X_train):
            X_training = X_train[train_index, :]
            y_training = y_train.values[train_index]

            X_val = X_train[test_index, :]
            y_val = y_train.values[test_index]

            naive_preds = np.repeat(naive_pred, X_val.shape[0])
            naive_acc = np.sum(naive_preds == y_val)/float(len(y_val))

            model.fit(X_training, y_training)
            preds = model.predict(X_val)
            preds_proba = model.predict_proba(X_val)
            pred_prob = np.amax(preds_proba, axis = 1)
            pred_prob = pred_prob.reshape(len(pred_prob), 1)
            
            
            correct_pred = preds == y_val
            correct_pred = correct_pred.reshape(len(pred_prob), 1)

            pitcher_array = np.repeat(pitcher, len(pred_prob)).reshape(len(pred_prob), 1)

            join_prob_pred = np.concatenate([pitcher_array, pred_prob, correct_pred], axis = 1)
            player_prob_pred_array = np.concatenate([player_prob_pred_array, join_prob_pred], axis = 0)

            acc = accuracy(preds, y_val)
            acc_comp = acc - naive_acc
            accuracy_list.append(acc_comp)

            

            if model_name == 'rf':
                feature_importances.append(model.feature_importances_.tolist())

            others = others_boolean
            if others == True:
                vol = pitch_volatility(y_training, y_val)
                vol_list.append(vol)

                len_train = train_size(y_training)
                train_size_list.append(len_train)

                number_pitches = number_pitch_types(y_training)
                number_pitches_list.append(number_pitches)

            # Find accuracy of model in different counts for each fold
            count_index = ['count_dummy', 'count_3-2', 'count_3-1', 'count_3-0', 'count_2-2', 'count_2-1', 'count_2-0', 'count_1-2', \
                           'count_1-1', 'count_1-0', 'count_0-2', 'count_0-1']
            count_df_ = pd.DataFrame(count_index, columns = ['count'])

            grouped_m_final = count_accuracy(X_training, y_training, X_val, y_val, correct_pred, cols_for_count_accuracy, count_cols_idx, 'count_')

            merged_count = pd.merge(left = count_df_, right = grouped_m_final, how = 'left', left_on = 'count', right_on = 'variable')
            merged_count['mean'].fillna(-1, inplace = True)
            count_accuracy_player.append(merged_count['mean'].values.tolist())
            count_values = merged_count['count']


        if others == True:
            return np.mean(accuracy_list), np.mean(vol_list), np.mean(train_size_list), np.mean(number_pitches_list), feature_importances, \
                   np.mean(count_accuracy_player, axis = 0), count_values, player_prob_pred_array
        else:
            return np.mean(accuracy_list)
           

    # Random Forest
    clf = RandomForestClassifier(n_estimators = 100, random_state = 1)
    rf_comp, vol, train_size, u_pitches, fi, player_count_acc, count_values, player_pred_prob_array = prediction(model = clf, others_boolean = True)

    feature_importance_df = pd.DataFrame(fi, columns = cols)
    mean_fi = np.mean(feature_importance_df, axis = 0).values

    pitcher_fi = []
    i = 0
    while i < len(mean_fi):
        for col in dummys_idx_dict:
            idx_list = dummys_idx_dict[col]
            not_in_list = True
            if i in idx_list:
                not_in_list = False
                if i == idx_list[0]:
                    sum_ = 0
                    for j in idx_list:
                        sum_ += mean_fi[j]
                    pitcher_fi.append(sum_)
                i += 1
                break

        if not_in_list == True:
            pitcher_fi.append(mean_fi[i])
            i += 1

    print(len(pitcher_fi))
    feature_importance_list.append(pitcher_fi)
    count_accuracy_all.append(player_count_acc)

    # Proabilities and correct predictions append
    all_prob_pred_array = np.concatenate([all_prob_pred_array, player_pred_prob_array], axis = 0)

    # SVM - radial basis function
    #clf = OneVsOneClassifier(svm.SVC(kernel = 'rbf', class_weight = 'balanced'))
    #svm2_comp = prediction(model = clf, others_boolean = False)

    temp = pd.DataFrame([[pitcher, rf_comp, vol, ave_confidence, sd_confidence, train_size, u_pitches, s_or_r]], \
                         columns = ['pitcher_id', 'rf', 'pitch_vol', 'ave_conf', 'sd_conf', 'train_size', 'unique_pitches', 'start_relief'])
    
    final_df = pd.concat([final_df, temp], ignore_index = True)


print(final_df)
players_ids = pd.read_csv('players.csv')
people_info = pd.read_csv('ids/people.csv')

players_ids = players_ids[['key_mlbam', 'name_first', 'name_last']]
people_info = people_info[['name_first', 'name_last', 'birth_year']]

final_df = pd.merge(left = final_df, right = players_ids, left_on = 'pitcher_id', right_on = 'key_mlbam', how = 'inner')
final_df = pd.merge(left = final_df, right = people_info, on = ['name_first', 'name_last'], how = 'left')

print(final_df)

final_df.to_csv('results.csv', index = False)
fi_df = pd.DataFrame(feature_importance_list, columns = fi_cols)
fi_df.to_csv('feature_importance_all.csv', index = False)

count_accuracy_df = pd.DataFrame(count_accuracy_all, columns = count_values)
count_accuracy_df.to_csv('count_accuracy.csv', index = False)
print(count_accuracy_df)

prob_pred_df = pd.DataFrame(all_prob_pred_array, columns = ['Pitcher', 'Prediction Probability', 'Correct Prediction'])
prob_pred_df.to_csv('prob_pred.csv', index = False)

#    # AdaBoost
#    clf = AdaBoostClassifier(base_estimator = RandomForestClassifier(n_estimators = 1), n_estimators = 200, random_state = 1)
#    clf.fit(X_train, y_train.values)
#    adaboostpreds = clf.predict(X_test)
#    
#    sim = no_seperation(naive_preds, adaboostpreds)
#    ada_acc = accuracy(adaboostpreds, y_test.values)
#    ada_comp = return_acc(sim, ada_acc)
#    
#    # SVM - linear
#    clf = OneVsOneClassifier(svm.SVC(kernel = 'linear', class_weight = 'balanced'))
#    clf.fit(X_train, y_train.values)
#    svmpreds = clf.predict(X_test)
#   
#    sim = no_seperation(naive_preds, svmpreds)
#    svm_acc = accuracy(svmpreds, y_test.values)
#    svm_comp = return_acc(sim, svm_acc)
#    
#    # SVM - linear
#    clf = OneVsRestClassifier(svm.SVC(kernel = 'linear'))
#    clf.fit(X_train, y_train.values)
#    svmpreds15 = clf.predict(X_test)
#   
#    sim = no_seperation(naive_preds, svmpreds15)    
#    svm15_acc = accuracy(svmpreds15, y_test.values)
#    svm15_comp = return_acc(sim, svm15_acc)
#    
#    # SVM - radial basis function
#    clf = OneVsOneClassifier(svm.SVC(kernel = 'rbf', class_weight = 'balanced'))
#    clf.fit(X_train, y_train.values)
#    svm2preds = clf.predict(X_test)
#    
#    sim = no_seperation(naive_preds, svm2preds)
#    svm2_acc = accuracy(svm2preds, y_test.values)
#    svm2_comp = return_acc(sim, svm2_acc)
#    
#    # SVM - radial basis function
#    clf = OneVsRestClassifier(svm.SVC(kernel = 'rbf', class_weight = 'balanced'))
#    clf.fit(X_train, y_train.values)
#    svm3preds = clf.predict(X_test)
#    
#    sim = no_seperation(naive_preds, svm3preds)
#    svm3_acc = accuracy(svm3preds, y_test.values)
#    svm3_comp = return_acc(sim, svm3_acc)
#    
#    temp = pd.DataFrame([[pitcher, rf_comp, ada_comp, svm_comp, svm15_comp, svm2_comp, svm3_comp]], \
#                         columns = ['pitcher_id', 'rf', 'ada_boost', 'ovo_lin_svm', 'ovr_lin_svm', 'ovo_rbf_svm', 'ovr_rbf_svm'])
#    
#    final_df = pd.concat([final_df, temp], ignore_index = True)
#
#final_df.to_csv('predictions.csv', index = False)

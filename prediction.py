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
cut_pitchers = 0
for pitcher in args.input:

    print(pitcher)
    sys.stdout.flush()
    df = pd.read_csv(pitcher)
    pitcher = df['pitcher_id'].unique()[0]
    s_or_r = df['StartVsRelief'].unique()[0]

    ## Create train_test column -> put this in feature eng
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

    # Drop unwanted columns and 2014 -> make this cleaner through he pipeline
    drop = ['Unnamed: 0', 'game_id', 'game_type', 'home_team', 'home_league', \
            'away_team', 'away_league', 'stadium', 'city', 'inning', 'inning_half', \
            'ab_game_num', 'batter_id', 'pitcher_id', 'ab_event_number', 'ab_event', \
            'p_description', 'type_', 'event_num', 'game_shift', 'StartVsRelief', \
            'start_speed', 'sz_top', 'sz_bot', 'pfx_x', 'pfx_y', 'px', 'py', \
            'pitch_type', 'type_confidence', 'zone', 'weighted_total_pitches',\
            'pitch_sequence', 'outs', 'batter_specific_count', 'prior_pitch','new_game']
    
    df.drop(drop, axis = 1, inplace = True)
    df = df.loc[df['year'] != 2014, :]
    df.replace(np.inf, np.nan, inplace = True)
    df.fillna(method = 'ffill', inplace = True)
    df.fillna(method = 'bfill', inplace = True)

    cat_vars = df.select_dtypes(include = ['object']).columns.tolist()
    cat_vars.remove('group_pitch_type')
    
    for col in cat_vars:
        dummies = pd.get_dummies(df[col], prefix = col, drop_first = True)
        df = pd.concat([df, dummies], axis = 1)
        df.drop(col, axis = 1, inplace = True)
    
    ## Create train_test column -> put this in feature eng
    train_test = {2015:'train', 2016:'train', 2017:'test'}
    df['train_test'] = df['year'].map(train_test)
    df.drop(['year'], axis = 1, inplace = True)
    
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
    
    # Feature scaling
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    kf = KFold(n_splits = 5)

    def no_seperation(naive_prediction, model_predictions):
        similiarity = np.sum(naive_preds == model_predictions)/float(len(model_predictions))
        if similiarity > 0.95:
            return similiarity
        else:
            return - 1

    def return_acc(similarity, model_accuracy, naive_accuracy = naive_acc):
        if similarity == -1:
            return model_accuracy - naive_acc
        else:
            return -1

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

    def prediction(model, others_boolean, model_name = 'rf', kfold_object = kf, training_array = X_train, naive_pred = most_freq):
        accuracy_list = []
        vol_list = []
        train_size_list = []
        number_pitches_list = []
        feature_importances = []

        for train_index, test_index in kf.split(training_array):
            X_training = X_train[train_index, :]
            y_training = y_train.values[train_index]

            X_val = X_train[test_index, :]
            y_val = y_train.values[test_index]

            naive_preds = np.repeat(naive_pred, X_val.shape[0])
            naive_acc = np.sum(naive_preds == y_val)/float(len(y_val))

            model.fit(X_training, y_training)
            preds = model.predict(X_val)
            
            acc = accuracy(preds, y_val)
            acc_comp = acc - naive_acc
            accuracy_list.append(acc_comp)

            if model_name == 'rf':
                feature_importances.append(model.feature_importances_)

            others = others_boolean
            if others == True:
                vol = pitch_volatility(y_training, y_val)
                vol_list.append(vol)

                len_train = train_size(y_training)
                train_size_list.append(len_train)

                number_pitches = number_pitch_types(y_training)
                number_pitches_list.append(number_pitches)

        if others == True:
            return np.mean(accuracy_list), np.mean(vol_list), np.mean(train_size_list), np.mean(number_pitches_list), feature_importances
        else:
            return np.mean(accuracy_list)
    

    # Random Forest
    clf = RandomForestClassifier(n_estimators = 100, random_state = 1)
    rf_comp, vol, train_size, u_pitches, fe = prediction(model = clf, others_boolean = True)

    # SVM - radial basis function
    #clf = OneVsOneClassifier(svm.SVC(kernel = 'rbf', class_weight = 'balanced'))
    #svm2_comp = prediction(model = clf, others_boolean = False)

    temp = pd.DataFrame([[pitcher, rf_comp, vol, ave_confidence, sd_confidence, train_size, u_pitches, s_or_r]], \
                         columns = ['pitcher_id', 'rf', 'pitch_vol', 'ave_conf', 'sd_conf', 'train_size', 'unique_pitches', 'start_relief'])
    
    final_df = pd.concat([final_df, temp], ignore_index = True)

    print(fe)

print(final_df)
final_df.to_csv('test.csv', index = False)
  
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

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

final_df = pd.DataFrame(columns = ['pitcher_id', 'rf', 'ada_boost', 'ovo_lin_svm', 'ovr_lin_svm', 'ovo_rbf_svm', 'ovr_rbf_svm'])

for pitcher in args.input:

    print(pitcher)
    sys.stdout.flush()
    df = pd.read_csv(pitcher)
    pitcher = df['pitcher_id'].unique()[0]
    
    # Drop unwanted columns and 2014 -> make this cleaner through he pipeline
    drop = ['Unnamed: 0', 'game_id', 'game_type', 'home_team', 'home_league', \
            'away_team', 'away_league', 'stadium', 'city', 'inning', 'inning_half', \
            'ab_game_num', 'batter_id', 'pitcher_id', 'ab_event_number', 'ab_event', \
            'home_runs', 'away_runs', 'p_description', 'type_', 'event_num', \
            'start_speed', 'sz_top', 'sz_bot', 'pfx_x', 'pfx_y', 'px', 'py', \
            'pitch_type', 'type_confidence', 'zone', 'strike_count', 'ball_count', \
            'pitch_sequence', 'outs', 'batter_specific_count', 'p_handedness']
    
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
    
    y_test = df.loc[df['train_test'] == 'test', 'group_pitch_type']
    X_test = temp.loc[temp['train_test'] == 'test', :]
    
    X_train.drop(['train_test'], axis = 1, inplace = True)
    X_test.drop(['train_test'], axis = 1, inplace = True)
    
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

    def prediction(model, kfold_object = kf, training_array = X_train, naive_pred = most_freq):
        accuracy_list = []
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
        
        print(accuracy_list)
        return np.mean(accuracy_list)
    

    # Random Forest
    clf = RandomForestClassifier(n_estimators = 50, random_state = 1)
    rf_comp = prediction(clf)

    # AdaBoost
    clf = AdaBoostClassifier(base_estimator = RandomForestClassifier(n_estimators = 1), n_estimators = 200, random_state = 1)
    ada_comp = prediction(clf)
    
    # SVM - linear
    clf = OneVsOneClassifier(svm.SVC(kernel = 'linear', class_weight = 'balanced'))
    svm_comp = prediction(clf)
    
    # SVM - linear
    clf = OneVsRestClassifier(svm.SVC(kernel = 'linear'))
    svm15_comp = prediction(clf)
   
    # SVM - radial basis function
    clf = OneVsOneClassifier(svm.SVC(kernel = 'rbf', class_weight = 'balanced'))
    svm2_comp = prediction(clf)
   
    # SVM - radial basis function
    clf = OneVsRestClassifier(svm.SVC(kernel = 'rbf', class_weight = 'balanced'))
    svm3_comp = prediction(clf)
   
    temp = pd.DataFrame([[pitcher, rf_comp, ada_comp, svm_comp, svm15_comp, svm2_comp, svm3_comp]], \
                         columns = ['pitcher_id', 'rf', 'ada_boost', 'ovo_lin_svm', 'ovr_lin_svm', 'ovo_rbf_svm', 'ovr_rbf_svm'])
    
    final_df = pd.concat([final_df, temp], ignore_index = True)

print(final_df)
  
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

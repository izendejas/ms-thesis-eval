#!/usr/bin/anaconda

from lib.Eval import *
from sklearn.ensemble import GradientBoostingRegressor,RandomForestRegressor,RandomForestClassifier
from sklearn.svm import SVR,NuSVR,SVC
from sklearn.feature_selection import *
from sklearn.metrics import *
from numpy import *
import matplotlib.pyplot as plt
from sklearn.cross_validation import KFold
import sys

output_version = sys.argv[1]

# load data
print 'loading data...'
#(data_train, y_train) = load_arff('/data/users/arffs/isKeyphraseData-training.arff',False)
#(data_test, y_test) = load_arff('/data/users/arffs/isKeyphraseData-test.arff',False)
#no_train = data_train[:,range(0,10)]
#no_test = data_test[:,range(0,10)]
# --- cross-validation
#y = hstack([y_train,y_test])
#X = vstack([data_train,data_test])
#W = vstack([no_train, no_test])

X,y = load_arff('/data/users/arffs/isKeyphraseData-all.arff') 
W = X[:,range(0,15)]

# ---- classifiers 
g = GradientBoostingRegressor(n_estimators=1000,learning_rate=0.02,max_depth=4,random_state=0,loss='ls')
rf = RandomForestRegressor(n_estimators=17,max_features=4,random_state=41)
s = SVR(C=1.0, epsilon=0.2,kernel='linear',tol=1e-4)
s2 = SVR(C=1.0, epsilon=0.2,kernel='poly',degree=2,tol=1e-3)

cv = CrossValidator(X,y)
cv2 = CrossValidator(W,y)

print 'outputting predictions...'
if output_version == '0':
	# output baseline
	output(X[:,0],fname='keyphrase-preds0.tsv')
elif output_version == '2':
	cv2_y,cv2_pred,idxs2 = cv2.predict(g)
	output(cv2_pred,fname='keyphrase-preds2.tsv')
else:
	cv_y,cv_pred,idxs = cv.predict(g)
	output(cv_pred,fname='keyphrase-preds%s.tsv' % output_version)


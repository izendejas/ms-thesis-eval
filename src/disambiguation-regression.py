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

X,y = load_arff('/data/users/arffs/disambigData-%s.arff' % output_version)
W = X[:,range(0,len(X[0]) - 6)]

# ---- classifiers 
g = GradientBoostingRegressor(n_estimators=1000,learning_rate=0.02,max_depth=4,random_state=0,loss='ls')
rf = RandomForestRegressor(n_estimators=17,max_features=3,random_state=41)
s = SVR(C=1.0, epsilon=0.2,kernel='linear',tol=1e-4)
s2 = SVR(C=1.0, epsilon=0.2,kernel='poly',degree=2,tol=1e-3)

#i -- cross validation
print 'outputting predictions...'

splits = infer_splits('/data/users/disambig-raw%s.tsv' % output_version)
cv = OneUserOutValidator(X,y,splits)
cv2 = OneUserOutValidator(W,y,splits)

if output_version == '0':
	# output baseline
	output(X[:,0],fname='disambig-preds0.tsv')
elif output_version == '2':
	cv2_y,cv2_pred,idxs2 = cv2.predict(g)
	output(cv2_pred,fname='disambig-preds2.tsv')
else:
	cv_y,cv_pred,idxs = cv.predict(g)
	fname = 'disambig-preds%s.tsv' % output_version
	output(cv_pred,fname=fname)

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
X,y = load_arff('/data/users/arffs/isKeyphraseData-%s.arff' % output_version) 
W = X[:,range(0,len(X[0]) - 2)]

# ---- classifiers 
g = GradientBoostingRegressor(n_estimators=1000,learning_rate=0.02,max_depth=4,random_state=0,loss='ls')
rf = RandomForestRegressor(n_estimators=17,max_features=4,random_state=41)
s = SVR(C=1.0, epsilon=0.2,kernel='linear',tol=1e-4)
s2 = SVR(C=1.0, epsilon=0.2,kernel='poly',degree=2,tol=1e-3)

splits = infer_splits('/data/users/keyphrase-all.tsv',lambda x: x.split('\t')[1])
cv = OneUserOutValidator(X,y,splits)
cv2 = OneUserOutValidator(W,y,splits)

print 'running cross-validation...'
p,r,T = cv.prec_recall(g)
p2,r2,T = cv2.prec_recall(g)

s2p,s2r,T = cv.prec_recall(s2)
s2wp,s2wr,T = cv2.prec_recall(s2)

plot_all([(r,p), (r2,p2),(s2r,s2p),(s2wr,s2wp)],['GBR + profile', 'GBR no profile','SVR + profile','SVR no profile'])
rankedf1 = rank_f1([(r,p,'g'), (r2,p2,'g-no prof'),(s2r,s2p,'s2'),(s2wr,s2wp,'s2-no prof')])
print 'ranked f1: %s' % str(rankedf1)

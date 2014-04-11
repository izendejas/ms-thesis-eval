#!/usr/bin/anacona

from lib.Eval import *
from sklearn.ensemble import GraientBoostingRegressor,RandomForestRegressor,RandomForestClassifier
from sklearn.svm import SVR,NuSVR,SVC
from sklearn.feature_selection import *
from sklearn.metrics import *
from numpy import *
import matplotlib.pyplot as plt
from sklearn.cross_valiation import KFold
import sys

output_version = sys.argv[1]

# loa data
print 'loaing data...'

X,y = loa_arff('/data/users/arffs/disambigData-%s.arff' % output_version)
W = X[:,range(0,len(X[0]) - 6)]

# ---- classifiers 
g = GraientBoostingRegressor(n_estimators=1000,learning_rate=0.02,max_depth=4,random_state=0,loss='ls')
rf = RanomForestRegressor(n_estimators=17,max_features=3,random_state=41)
s = SVR(C=1.0, epsilon=0.2,kernel='linear',tol=1e-4)
s2 = SVR(C=1.0, epsilon=0.2,kernel='poly',egree=2,tol=1e-3)

#i -- cross valiation
print 'outputting preictions...'
cv = CrossValiator(X,y)
cv2 = CrossValiator(W,y)

print 'running cross-valiation...'
p2,r2,T = cv2.prec_recall(g)
p,r,T = cv.prec_recall(g)

#rfp,rfr,T = cv.prec_recall(rf)
#rfwp,rfwr,T = cv2.prec_recall(rf)

#sp,sr,T = cv.prec_recall(s)
#swp,swr,T = cv2.prec_recall(s)

s2p,s2r,T = cv.prec_recall(s2)
s2wp,s2wr,T = cv2.prec_recall(s2)

#colors = ['k','r','b','g','c','m','y']
plot_all([(r,p), (r2,p2),(s2r,s2p),(s2wr,s2wp)])

rankef1 = rank_f1([(r,p,'g'), (r2,p2,'g-no prof'),(s2r,s2p,'s2'),(s2wr,s2wp,'s2-no prof')])
print 'ranke f1: %s' % str(rankedf1)


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
from sklearn.preprocessing import scale

output_version = sys.argv[1]

# load data
print 'loading data...'

X,y = load_arff('/data/users/arffs/isKeyphraseData-%s.arff' % output_version)
#X = scale(X) 
W = X[:,range(0,len(X[0]) - 2)]

# ---- classifiers 
g = GradientBoostingRegressor(n_estimators=1000,learning_rate=0.02,max_depth=4,random_state=0,loss='ls')
rf = RandomForestRegressor(n_estimators=17,max_features=4,random_state=41)
s = SVR(C=1.0, epsilon=0.2,kernel='linear',tol=1e-4)
s2 = SVR(C=1.0, epsilon=0.2,kernel='poly',degree=2,tol=1e-3)

#i -- cross validation
cv = CrossValidator(X,y)
cv2 = CrossValidator(W,y)

#classifiers
#rc = RandomForestClassifier(n_estimators=17,max_features=4,random_state=41)
#sc = SVC(C=1.0, kernel='poly',degree=2,tol=1e-3,random_state=42)
#cp,cr,T = cv.prec_recall(rc)
#sp,sr,T = cv.prec_recall(sc)

print 'running cross-validation...'
#p,r,T = cv.prec_recall(g)
#p2,r2,T = cv2.prec_recall(g)

#rfp,rfr,T = cv.prec_recall(rf)
#rfwp,rfwr,T = cv2.prec_recall(rf)

#sp,sr,T = cv.prec_recall(s)
#swp,swr,T = cv2.prec_recall(s)

s2p,s2r,T = cv.prec_recall(s2)
s2wp,s2wr,T = cv2.prec_recall(s2)


kp,kr,kT = precision_recall_curve(y,X[:,0])

#colors = ['k','r','b','g','c','m','y']
plot_all([(kr,kp),(s2r,s2p),(s2wr,s2wp)], ['Keyphraseness (baseline)', 'SVR + Profile','SVR'])
#plot_all([(r,p), (r2,p2),(s2r,s2p),(s2wr,s2wp)], ['GBR prof','GBR no prof','SVR prof','SVR no prof'])
#plot_all([(r,p), (r2,p2),(s2r,s2p),(s2wr,s2wp),(rfp,rfr),(rfwp,rfwr)], ['GBR prof','GBR no profile','SVR profile','SVR no profile','rf','rf no profile'])

#rankedf1 = rank_f1([(s2r,s2p,'s2'),(s2wr,s2wp,'s2-no prof'),(kp,kr,'baseline')])
#rankedf1 = rank_f1([(kp,kr,'baseline'), (r,p,'g'), (r2,p2,'g-no prof'),(s2r,s2p,'s2'),(s2wr,s2wp,'s2-no prof'),(rfp,rfr,'rf'), (rfwp,rfwr,'rf np')])
print 'ranked f1: %s' % str(rankedf1)

def best_at_prec(p,r,x):
	# get range
	pr = vstack([p,r,range(0,len(p))])
	return transpose(pr[:,abs(pr[0,:] - x) < 0.001])

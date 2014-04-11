#!/usr/bin/anaconda

from lib.Eval import *
from sklearn.ensemble import GradientBoostingRegressor,RandomForestRegressor,RandomForestClassifier
from sklearn.svm import SVR,NuSVR,SVC
from numpy import *
from sklearn.externals import joblib
from datetime import datetime as dt
import sys

model = sys.argv[1]
fname = sys.argv[2]
mname = '/data/users/eval/temp/%s.pkl' % model

X,y = load_arff(fname)
#W = X[:,range(0,15)]

print 'number of instances %d' % len(y)

# ---- classifiers 
g = GradientBoostingRegressor(n_estimators=1000,learning_rate=0.02,max_depth=4,random_state=0,loss='ls')
print '%s - training...' % dt.now().strftime('%H:%M:%S')
g.fit(X,y)
print '%s - serializing %s...' % (dt.now().strftime('%H:%M:%S'), mname)
joblib.dump(g, mname, compress=9)
print '%s - done' % dt.now().strftime('%H:%M:%S')

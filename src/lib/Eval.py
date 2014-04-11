#!/usr/bin/anaconda

from sklearn.ensemble import GradientBoostingRegressor,RandomForestRegressor,RandomForestClassifier
from sklearn.svm import SVR,NuSVR,SVC
from sklearn.feature_selection import *
from sklearn.metrics import *
import matplotlib.pyplot as plt
from sklearn.cross_validation import KFold
from datetime import datetime
from numpy import *
import sys

def load_arff(fname,regression=True):
	f = open(fname, 'r')
	matrix = []
	cls = []
	attributes = 0
	for line in f:
		line = line.strip()
		if line.find('@attribute') == 0:
			attributes += 1
		else:
			(v,c) = read_sparse_arff_vector(line,attributes)
			if v:
				matrix.append(v)
				cls.append(c)
	f.close()
	return (array(matrix),array(cls))

def read_sparse_arff_vector(line,num_attributes,regression=True):
	if line.find('@') < 0 and line != '':
		data = map(lambda x: 0.0, range(0, num_attributes-1))
		cls = 0.0
		features = line.strip('{}').split(',')
		for f in features:
			[fidx, v] = f.split(' ')
			idx = int(fidx)
			if idx < (num_attributes - 1):
				data[int(fidx)] = float(v)
			else:
				if regression:
					if v == 'true':
						cls = 1.0
					elif v == 'false':
						cls = 0.0
					else:
						cls = float(v)
				else:
					cls = v

		return (data,cls)
	return (None,None)

class RegressorEvaluator:
	def __init__(self,X,y,X_test,y_test):
		self.X = X
		self.y = y
		self.X_test = X_test
		self.y_test = y_test
		self.max_auc = 0.0

	def get_predictions(self,r):
		r.fit(self.X,self.y)
		pred = r.predict(self.X_test)
		return pred

	def eval(self,r):
		pred = self.get_predictions(r)
		p,r,T = precision_recall_curve(self.y_test,pred)
		a = auc(r,p)
		if a > self.max_auc:
			self.max_auc = a
			print 'new max auc: %.4f' % self.max_auc
		return p,r,T


class CrossValidator:
	
	def __init__(self,X,y):
		self.X = X 
		self.y = y

	def predict(self,cls,f = 5):
		kf = KFold(len(self.y),n_folds=f)
		curPred = None
		curY = None
		curIdx = None

		for train,test in kf:
			X_train, X_test, y_train, y_test = self.X[train], self.X[test], self.y[train], self.y[test]
			rev = RegressorEvaluator(X_train,y_train,X_test,y_test)
			pred = rev.get_predictions(cls)

			if len(pred) != len(y_test):
				raise Exception('pred %d vs. test %d' % (len(pred), len(y_test)))

			if curPred == None:
				curPred = pred
				curY = y_test
				curIdx = test
			else:
				curPred = hstack([curPred,pred])
				curY = hstack([curY,y_test])
				curIdx = hstack([curIdx,test])

		return curY,curPred,curIdx

	def prec_recall(self,cls,f=5):
		curY,curPred,curIdx = self.predict(cls,f)
		return precision_recall_curve(curY,curPred)

	def best_at_rec(self,c,x):
		# get range
		p,r,T = self.prec_recall(c)
		pr = vstack([p,r,range(0,len(p))])
		return transpose(pr[:,abs(pr[1,:] - x) < 0.02])
	
	def best_at_prec(self,c,x):
		# get range
		p,r,T = self.prec_recall(c)
		pr = vstack([p,r,range(0,len(p))])
		return transpose(pr[:,abs(pr[0,:] - x) < 0.001])

#sys.exit(0)

def sjoin(s,iterable):
	return s.join(map(lambda x: str(x), iterable))

def output_with_stuff(stuff,preds,d='/data/users/',fname='blah.tsv'):
	# output predictions
	data = transpose(vstack([stuff,preds]))
	writer = open('%s%s' % (d,fname),'w')
	s = '\n'.join([sjoin('\t',row) for row in data])
	writer.write(s)
	writer.close()

def output(preds,d='/data/users/',fname='blah.tsv'):
	# output predictions
	writer = open('%s%s' % (d,fname),'w')
	writer.write(sjoin('\n',preds))
	writer.close()

def rank_f1(scores):
	f1 = map(lambda (r,p,n): (max(2*p*r/(r+p+0.00001)),n), scores)
	f1.sort(key=lambda x: -x[0])
	return f1

def plot_all(curves,legends):
	colors = ['k','r','b','g','c','m','y']
	# display curve
	fig = plt.figure()
	ax = fig.gca()
	ax.set_xticks(arange(0,1,0.05))
	ax.set_yticks(arange(0,1,0.05))
	plt.xlabel('Recall')
	plt.ylabel('Precision')
	plt.xlim([0,1])
	plt.ylim([0,1])
	plt.grid()
	color = 0
	plots = []
	for r,p in curves:
		curp, = plt.plot(r,p,'%s-' % colors[color])
		plots.append(curp)
		color = (color + 1) % 7
	plt.legend(plots, legends, loc = 3)
	plt.show()

def plot_scatter(curves,legends,xl='recall',yl='precision'):
	colors = ['ro','bs','y^','m*','g*','c*','k*']
	# display curve
	fig = plt.figure()
	#ax = fig.gca()
	#ax.set_xticks(arange(0,1,0.05))
	#ax.set_yticks(arange(0,1,0.05))
	plt.xlabel(xl)
	plt.ylabel(yl)
	#plt.xlim([0,1])
	plt.ylim([0,1.1])
	plt.grid()
	color = 0
	plots = []
	for r,p in curves:
		curp, = plt.plot(r,p,'%s' % colors[color])
		plots.append(curp)
		color = (color + 1) % 7
	plt.legend(plots, legends,loc=4)
	plt.show()

class OneUserOutValidator:
	
	def __init__(self,X,y,kf):
		self.X = X 
		self.y = y
		self.kf = kf

	def predict(self,cls):
		#kf = KFold(len(self.y),n_folds=f)
		curPred = None
		curY = None
		curIdx = None

		num_splits = len(self.kf)
		
		i = 1 
		for train,test in self.kf:
			t = datetime.now().strftime('%H:%M:%S')
			print 'running on split %d of %d -- %s' % (i,num_splits,t)
			X_train, X_test, y_train, y_test = self.X[train], self.X[test], self.y[train], self.y[test]
			rev = RegressorEvaluator(X_train,y_train,X_test,y_test)
			pred = rev.get_predictions(cls)

			if len(pred) != len(y_test):
				raise Exception('pred %d vs. test %d' % (len(pred), len(y_test)))

			if curPred == None:
				curPred = pred
				curY = y_test
				curIdx = test
			else:
				curPred = hstack([curPred,pred])
				curY = hstack([curY,y_test])
				curIdx = hstack([curIdx,test])
			
			i += 1
		
		print 'all done! (%s)' % datetime.now().strftime('%H:%M:%S')

		return curY,curPred,curIdx 

	def prec_recall(self,cls,f=5):
		curY,curPred,curIdx = self.predict(cls)
		return precision_recall_curve(curY,curPred)

def infer_splits(fname,uid_getter=lambda x: x.split('\t')[0].split('-')[1]):
	i = 0
	startIdx = 0
	prevUid = ''
	splits = [] 
	
	f = open(fname,'r')	
	rows = [x.strip() for x in f]
	f.close()

	num_rows = len(rows)

	for line in rows:
		uid = uid_getter(line) 
		if prevUid != '' and uid != prevUid:
			# done
			test = range(startIdx,i)
			
			left,train = None, None
			if startIdx > 0:
				left = range(0,startIdx)
			
			right = range(i,num_rows)
			if left != None:
				train = hstack([left, right])
			else:
				train = array(right)

		
			splits.append((train, test))
			startIdx = i
		
		prevUid = uid
		i += 1

	test = range(startIdx,i)
	train = range(0,startIdx)
	splits.append((train,test))

	return array(splits) 

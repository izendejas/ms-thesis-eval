#!/usr/bin/python

import sys

fname = sys.argv[1]
f = open(fname, 'r')

vals = set() 
for line in f:
	[pid,kid,ksscore,score,eids] = line.strip().split('\t',4)
	vals.add(float(score))

f.close()

vals = sorted(vals)

tp = [0 for x in vals]
fp = [0 for x in vals]
fn = [0 for x in vals]

f = open(fname,'r')
r = range(0,len(vals))
for line in f:
	[pid,kid,kscore,score,eids] = line.strip().split('\t',4)

	score = float(score)
	lbls = eids.split('\t') 
	pos = len(filter(lambda x: x.split(',')[1] == '1', lbls)) == 1

	for idxv in r:
		T = vals[idxv] 
		if len(lbls) > 1:
			fn[idxv] += 1
		elif score >= T:
			if pos:
				tp[idxv] += 1
			else:
				fp[idxv] += 1
		elif score <= T and pos:
			fn[idxv] += 1

for idxv in r:
	# thresh, precision, recall
	T = vals[idxv]
	precision = float(tp[idxv])/(tp[idxv] + fp[idxv] + 0.0000001)
	recall = float(tp[idxv])/(tp[idxv] + fn[idxv])
	f1 = 2*precision*recall/(precision+recall)
	print '%.3f\t%d\t%d\t%d\t%.3f\t%.3f\t%.3f' % (T,tp[idxv], fp[idxv], fn[idxv],precision,recall,f1)

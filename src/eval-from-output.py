#!/usr/bin/python
import sys

fname1 = sys.argv[1]
fname2 = sys.argv[2]

# iterate over ground truth 
gtruth = {}
f = open(fname1, 'r')
for line in f:
	parts = line.strip('\n').split('\t',1)
	pid = parts[0]
	eids = '' if len(parts) == 1 else parts[1]
	#idx = int(pid.split('-')[0])
	#if idx >= 20:
	gt = set(eids.split('\t'))
	gtruth[pid] = gt
f.close()

#[item for sublist in l for item in sublist]
print 'number of positives: %d' % len([x for y in gtruth.values() for x in y])

# iterate over predicted 
tp = 0
fp = 0
fn = 0
f = open(fname2,'r')
for line in f:
	[pid,eids] = line.strip('\n').split('\t',1)
	eids = set(filter(lambda x: x != '', eids.split('\t')))
	
	gt = gtruth.get(pid,set())
	fps = filter(lambda x: x not in gt,eids)

	if len(fps) > 0:
		print 'fps: %s(%d) = %s -' % (pid, len(fps),','.join(fps))

	tp += len(filter(lambda x: x in gt,eids))
	fp += len(fps)
	eids = set(eids)
	fn += len(filter(lambda x: x not in eids,gt))

f.close()

# output data
prec = float(tp) / (tp + fp)
rec = float(tp) / (tp + fn)
f1 = 2*prec*rec/(prec + rec)

print ('\t'.join(map(lambda x: str(x), [tp,fp,fn,prec,rec,f1])))

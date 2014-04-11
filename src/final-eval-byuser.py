#!/usr/bin/python
import sys
	
fname1 = sys.argv[1]
fname2 = sys.argv[2]

uids = ['45614792','248404698','47672754','14248582','11679892','35432131','198057200','3533231','20713061',
		'36969785','346374264','36768575','17445752','19426551','280596494','4925881','9300262',
		'15756383','213985865','6273552']

assert(len(uids) == 20)

#print '\t'.join(['ks','tp','fp','fn','prec','rec','f1'])
print '\t'.join(['prec','rec','f1'])

for uid in uids:

	# iterate over ground truth 
	gtruth = {}
	f = open(fname1, 'r')
	for line in f:
		parts = line.strip('\n').split('\t',1)
		pid = parts[0]

		if pid.find(uid) < 0:
			continue

		eids = '' if len(parts) == 1 else parts[1]
		#idx = int(pid.split('-')[0])
		#if idx >= 20:
		gt = set(eids.split('\t'))
		gtruth[pid] = gt
	f.close()
	
	#[item for sublist in l for item in sublist]
	#print 'number of positives: %d' % len([x for y in gtruth.values() for x in y])
	
	# load data by post id
	all_preds = {}
	f = open(fname2,'r')
	for line in f:
		[pid,kid,kscore,score,eids] = line.strip().split('\t',4)
		
		if pid.find(uid) < 0:
			continue
		
		score = float(score)
		kscore = float(kscore)
		lbls = eids.split('\t')
	
		inst = {'score':score, 'kscore': kscore, 'lbls' : lbls}
		prev = all_preds.get(pid, [])
		prev.append(inst)
		all_preds[pid] = prev
	f.close()
	
	#print 'number of instances %d' % len(all_preds)
	
	#kscores = set()
	#for insts in all_preds.values():
	#	for inst in insts:
	#		kscores.add(inst['kscore'])
	
	#kscores = sorted(kscores)
	kscores = [0.555]
	
	#print 'number of scores %d' % len(kscores)
	
	for ks in kscores: 
		# iterate over predicted 
		tp = 0
		fp = 0
		fn = 0
		for pid,cur_preds in all_preds.iteritems():
			# skip anything below the threshold
			preds = filter(lambda x: x['kscore'] >= ks,cur_preds)
			
			eids = set()
			for pred in preds:
				x = pred['lbls']
				if len(x) == 1:
					eids.add(x[0].split(',')[0])	# add eid
		
			gt = gtruth.get(pid,set())
			fps = filter(lambda x: x not in gt,eids)
	
			#if len(fps) > 0:
			#	print 'fps: %s(%d) = %s -' % (pid, len(fps),','.join(fps))
	
			tp += len(filter(lambda x: x in gt,eids))
			fp += len(fps)
			eids = set(eids)
			fn += len(filter(lambda x: x not in eids,gt))
	
		# output data
		prec = float(tp) / (tp + fp)
		rec = float(tp) / (tp + fn)
		f1 = 2*prec*rec/(prec + rec + 0.0000001)
	
		#print ('\t'.join(map(lambda x: str(x), [ks,tp,fp,fn,prec,rec,f1])))
		print ('\t'.join(map(lambda x: str(x), [prec,rec,f1])))

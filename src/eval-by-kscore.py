#!/usr/bin/python
import sys

fname = sys.argv[1]
f = open(fname, 'r')

start = True
prev_id = ''
prev_ees = []

for line in f:
	[pid,kid,kscore,score,eids] = line.strip().split('\t',4)
	score = float(score)
	kscore = float(kscore)
	lbls = eids.split('\t')
	ees = map(lambda x: x.split(','), lbls)

	#print str(ees)
	if not start and prev_id != pid:
		# output
		#print '%s\t%s' % (prev_id, '\t'.join(prev_ees)) 
		prev_ees = []

	#if kscore >= 0.6934 and len(ees) == 1: # and kscore <= 1.0: 
	if kscore >= 0.6 and len(ees) == 1: # and kscore <= 1.0: 
		# output
		prev_ees.append(ees[0])
		if ees[0][1] == '1':
			print line,
		else:
			print line,

	prev_id = pid
	start = False

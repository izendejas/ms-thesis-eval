#!/usr/bin/python

import sys

fname = sys.argv[1]

def serialize_labels(t):
	s = map(lambda x: ','.join(x), t)
	return '\t'.join(s)

def get_region(s):
	parts = s.split('_')
	return (int(parts[1]),int(parts[2]))

groups = {}
f = open(fname, 'r')
for line in f:
	[pid, kid, eid, isTop, kscore, score] = line.strip().split('\t')
	lbl = '1' if isTop == 'true' else '0'
	v = float(score)
	
	data = groups.get(pid,[])
	stuff = {}
	stuff['pid'] = pid
	stuff['kid'] = kid
	stuff['eid'] = eid
	stuff['lbl'] = lbl
	stuff['score'] = v
	stuff['kscore'] = float(kscore) 
	stuff['region'] = get_region(kid) 
	data.append(stuff)
	groups[pid] = data

f.close()

#print 'len: %d' % len(groups)

# iterate over, group by fucken region
subs = []
for k,data in groups.iteritems():
	data.sort(key=lambda x: x['region'][0])
	#print 'k: %s; %s' % (k,str(data))
	
	start = True
	prev = (-1,-1)
	cur_group = []
	for e in data:
		reg = e['region']
		if prev[1] >= reg[0]:
			cur_group.append(e)
		else:
			if len(cur_group) > 0:
				subs.append(cur_group) # add group to subgroup
			cur_group = [e] # start new group

		start = False
		prev = reg

	# finalize
	if len(cur_group) > 0:
		subs.append(cur_group)

#print 'size of subs: %d' % len(subs)

for sg in subs:
	# skip groups with no positives
	blah = filter(lambda x: x['lbl'] == '1',sg)

	if len(blah) == 0:
		#print 'skipped: %s' % sg[0]['kid']
		continue
	
	# process only those that have longest keyphrase with lbl 1
	blah = map(lambda x: x['kid'].split('_')[0],blah)
	print str(blah)

	blah = blah.sort(key=lambda x: len(x))
	topks = blah[0]

	sg = filter(lambda x: x['kid'].split('_')[0] == topks,sg)

	# filter by max keyphrase score
	maxscore = max(map(lambda x: x['score'], sg))
	#if maxkscore > 0.6:
	#	maxkscore = maxkscore *0.8
	sg = filter(lambda x: x['score'] >= maxscore, sg)

	#print 'maxkscore = %.5f; size: %d' % (maxkscore, len(sg))
	best = sg[0]
	max_score = best['score']
	# remove dupes
	unique_eids = set([x['eid'] for x in sg])
	sg = sg if len(unique_eids) > 1 else sg[:1]

	print '%s\t%s\t%s\t%s\t%s' % (best['pid'], best['kid'], best['kscore'],
			str(max_score),'\t'.join(map(lambda x: '%s,%s' % (x['eid'],x['lbl']),sg)))


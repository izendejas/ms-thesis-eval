#!/usr/bin/python

from lib.Eval import plot_all,plot_scatter
from numpy import loadtxt,arange
import matplotlib.pyplot as plt

base = loadtxt('/data/users/eval/plots/scores-by-user0.tsv',delimiter='\t',skiprows=1)
prof = loadtxt('/data/users/eval/plots/scores-by-user1.tsv',delimiter='\t',skiprows=1)
noprof = loadtxt('/data/users/eval/plots/scores-by-user2.tsv',delimiter='\t',skiprows=1)

NPOSTS = 1
NENTS = 2
EPT = 3
MNENT = 4
EPTMN = 5
TKPT = 6
PREC = 7
REC = 8
F1 = 9

def plotby(X,Y,labels):
	#plots = [pr0,pr1,pr2,pr3]
	plots = [base,prof,noprof]
	for i in range(0,len(plots)):
		p = plots[i]
		plots[i] = (p[:,X], p[:,Y])

	plot_scatter(plots, ['Baseline','GBR + profile','GBR no profile'],labels[0],labels[1])

metrics = [PREC,REC,F1]
ml = ['precision','recall','f1 score']
stats = [NPOSTS,NENTS,EPT,MNENT,EPTMN,TKPT]
sl = ['number of posts in profile','number of entities in profile','entities per tweet',
	'manually labeled entities','manually labeled entities per tweet','number of words per tweet']

for i in range(0,len(metrics)):
	for j in range(0,len(stats)):
		plotby(stats[j],metrics[i],[sl[j],ml[i]])

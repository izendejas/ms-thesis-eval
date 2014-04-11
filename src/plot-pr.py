#!/usr/bin/python

from lib.Eval import plot_all
from numpy import loadtxt,arange
import matplotlib.pyplot as plt

pr0 = loadtxt('/data/users/eval/plots/precision-recall-0.tsv',delimiter='\t')
#r1 = loadtxt('/data/users/eval/plots/precision-recall-1.tsv',delimiter='\t')
pr1 = loadtxt('/data/users/eval/precision-recall-1.tsv',delimiter='\t')
pr2 = loadtxt('/data/users/eval/plots/precision-recall-2.tsv',delimiter='\t')
#pr2 = loadtxt('/data/users/eval/precision-recall-2.tsv',delimiter='\t')
#pr3 = loadtxt('/data/users/eval/pr-reg-2.tsv',delimiter='\t')
pr3 = loadtxt('/data/users/eval/precision-recall-1avg3.tsv',delimiter='\t')
pr4 = loadtxt('/data/users/tagme_res.tsv',delimiter='\t')
#pr3 = loadtxt('/data/users/eval/precision-recall-1.tsv',delimiter='\t')

PREC = 4
REC = 5 

plots = [pr0,pr1,pr2,pr3,pr4]
for i in range(0,len(plots)):
	p = plots[i]
	plots[i] = (p[:,REC], p[:,PREC])

plot_all(plots, ['Baseline','GBR + Profile','GBR','AVG (PR,R,CMNS)','TAGME'])

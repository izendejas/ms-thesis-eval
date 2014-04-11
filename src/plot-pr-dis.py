#!/usr/bin/python

from lib.Eval import plot_all
from numpy import loadtxt,arange
import matplotlib.pyplot as plt

#pr0 = loadtxt('/data/users/eval/pr-dis-0.tsv',delimiter='\t')
pr1 = loadtxt('/data/users/eval/pr-dis-reg-1.tsv',delimiter='\t')
pr1avg = loadtxt('/data/users/eval/pr-dis-avg-1.tsv',delimiter='\t')
pr2 = loadtxt('/data/users/eval/pr-dis-reg-2.tsv',delimiter='\t')
pr2avg = loadtxt('/data/users/eval/pr-dis-avg-2.tsv',delimiter='\t')

PREC = 3 
REC = 4

#plots = [pr0,pr1,pr1avg,pr2,pr2avg]
plots = [pr1,pr1avg,pr2,pr2avg]
for i in range(0,len(plots)):
	p = plots[i]
	plots[i] = (p[:,REC], p[:,PREC])

#plot_all(plots, ['Baseline','GBR + Profile','AVG(PR,R,EP)','GBR', 'AVG (R,EP)'])
plot_all(plots, ['GBR + Profile','AVG(PR,R,EP)','GBR', 'AVG (R,EP)'])

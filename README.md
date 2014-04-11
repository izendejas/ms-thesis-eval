## Evaluation Scripts for MS Thesis

A set of simple scripts used in evaluating my thesis work, which
extracted entities from tweets and disambiguated them using Wikipedia mining
techniques, while also leveraging user interest profiles.

Most of these scripts were very custom and not really meant for re-use
as is, but with some work, there's some re-usable work that can be
derived. For example, there's an opportunity to write a more robust
[ARFF]<http://www.cs.waikato.ac.nz/ml/weka/arff.html> loader as well
as a better cross-validation framework that also does a search over
possible classifier/regresssor parameters.

This marked my first use of scikit-learn, which was a joy to use.

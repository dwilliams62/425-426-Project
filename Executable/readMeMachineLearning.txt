The dataset for this machine learning algorithm was provided by Dr. Karl Maier through Zotero.
Author of this read me: Olivia Brague

List of dependencies:
-scikit-learn
-pandas
-spacy
-pickle

Status of the dataset: In its current state, the dataset does not have as many entries as
we would hope for it to have. Dr. Maier is currently working on adding more onto the dataset
in order to better aid the machine learning algorithm. This is an ongoing process and 
at the point that I am writing this we do not have that dataset.

Reasoning for choosing SVM: I chose SVM after running a series of experiments on the dataset using
different algorithms. I found that overall SVM performs consistently better than the other algorithms
for this particular set of data. I also performed hyperparameter tuning to select the best set
of parameters for SVM. With the future expansion of the dataset, the best algorithm or parameters
could be subject to change so more experiementation may be needed.

Right now, in order to better increase the performance of the algorithm with the current state of the
dataset, I have decided to only use the three main categories of biophysical, social, and psychological
for classification instead of the subcategories as I feel that in its current state the subcategories
are causing a lot of confusion for the algorithm. In the future, if the dataset gets more examples,
it may be appropriate to add in the subcategories again instead of just the main categories.

I attempted to try pickling the algorithm in order to have the slow part of vectorization be done ahead of time.
The pickle file I used is still here if someone wishes to attempt to try to use it again, but we found it was
taking just as long to load it as it would to just do the vectorization.
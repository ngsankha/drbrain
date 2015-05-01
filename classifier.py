import pickle
from network import Network
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier

class Classifier:
	def __init__(self, filename):
		self.classifiers = pickle.load(open('classifiers.clf', 'rb'))
		self.network = Network(filename)
		self.features = self.network.compute()

	def test1(self):
		feature_vec = [self.features[3], self.features[4], self.features[0]]
		return self.classifiers[0].predict([feature_vec])[0]

	def test2(self):
		feature_vec = [self.features[5], self.features[4], self.features[1]]
		return self.classifiers[1].predict([feature_vec])[0]

	def test3(self):
		feature_vec = [self.features[6], self.features[4]]
		return self.classifiers[2].predict([feature_vec])[0]
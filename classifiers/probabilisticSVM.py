from classifiers.probabilisticClassifierWithBoundary import *
from classifiers.notAllowHardFP import *
import sklearn.svm as svm

class ProbabilisticSVM(ProbabilisticClassifierWithBoundary, NotAllowHardFP):

    def __init__(self, kernel='linear', C=10, degree=3, gamma=1, coef0=1, **kwds):
        super().__init__(**kwds)
        self.c = C
        self.kernel = kernel
        self.degree = degree
        self.gamma = gamma
        self.coef0 = coef0

    def classify_by_one_classifier(self, point, classifier):
        return classifier.predict(point)

    def equals(self, c1, c2):
        return np.all(c1.support_vectors_ == c2.support_vectors_)

    def update(self, positive_data, positive_data_utility, att_support, game_matrix):
        data, validation_data, labels, weights = self.prepare_data(positive_data, positive_data_utility, att_support)
        data = data[weights > THETA]
        labels = labels[weights > THETA]
        weights = weights[weights > THETA]

        new_classifier = svm.SVC(kernel=self.kernel, degree=self.degree, gamma=self.gamma, coef0=self.coef0, C=self.c)
        new_classifier.fit(data, labels, weights)

        return self.expand_classifiers(new_classifier, positive_data, positive_data_utility, att_support, game_matrix)

    def distance_from_boundary(self, classifier, point):
        dist = classifier.decision_function(point)
        if self.kernel == 'linear':
            w_norm = np.linalg.norm(classifier.coef_)
            dist = dist / w_norm
        return dist
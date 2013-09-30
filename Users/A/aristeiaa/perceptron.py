class Perceptron(object):
    def __init__(self, weights=None, threshold=0.5):
        self.threshold = threshold
        self.weights = weights
        self.verbose = False
    def output(self, input_vector):
        if self._total(input_vector) < self.threshold:
            return 0
        else:
            return 1
    def train(self, training_set, alpha=0.1, end_after=100):
        if self.weights is None:
            self.weights = [0 for _ in range(len(training_set.keys()[0]))]
        n = 0
        updated = True
        while(updated):
            n += 1
            updated = False
            for xv, t in training_set.items():
                y = self.output(xv)
                if(y != t):
                    self._update_weights(alpha, t, y, xv)
                    self._update_threshold(alpha, t, y)
                    updated = True
            if end_after is not None and n >= end_after:
                break
        return n
    def test(self, training_set):
        for xv, t in training_set.items():
            if(self.output(xv) != t):
                return False
        return True
    def _total(self, input_vector):
        total = 0
        for w,x in zip(self.weights, input_vector):
            total += (w * x)
        return total
    def _update_weights(self, alpha, t, y, xv):
        for i in range(len(self.weights)):
            self.weights[i] = (alpha * (t - y) * xv[i]) + self.weights[i]
    def _update_threshold(self, alpha, t, y):
        self.threshold = (alpha * (t - y) * -1) + self.threshold


nand_set = {
  (0,0,0): 1,
  (0,1,0): 1,
  (1,0,0): 1,
  (1,1,0): 0
  }

nn = Perceptron()
iterations = nn.train(nand_set, alpha=.2) # alpha is the learning rate
print "Trained in {0} iterations.".format(iterations)
print "Correct?", nn.test(nand_set)
print "Weights: {0}, Threshold: {1}".format(nn.weights, nn.threshold)

class Perceptron(object):
    def __init__(self, weights=None, threshold=0.5):
        self.threshold = threshold
        self.weights = weights
        self.verbose = False
    def output(self, input_vector):
        if self._total(input_vector) < self.threshold:
            return 0
        else:
            return 1
    def train(self, training_set, alpha=0.1, end_after=100):
        if self.weights is None:
            self.weights = [0 for _ in range(len(training_set.keys()[0]))]
        n = 0
        updated = True
        while(updated):
            n += 1
            updated = False
            for xv, t in training_set.items():
                y = self.output(xv)
                if(y != t):
                    self._update_weights(alpha, t, y, xv)
                    self._update_threshold(alpha, t, y)
                    updated = True
            if end_after is not None and n >= end_after:
                break
        return n
    def test(self, training_set):
        for xv, t in training_set.items():
            if(self.output(xv) != t):
                return False
        return True
    def _total(self, input_vector):
        total = 0
        for w,x in zip(self.weights, input_vector):
            total += (w * x)
        return total
    def _update_weights(self, alpha, t, y, xv):
        for i in range(len(self.weights)):
            self.weights[i] = (alpha * (t - y) * xv[i]) + self.weights[i]
    def _update_threshold(self, alpha, t, y):
        self.threshold = (alpha * (t - y) * -1) + self.threshold


nand_set = {
  (0,0,0): 1,
  (0,1,0): 1,
  (1,0,0): 1,
  (1,1,0): 0
  }

nn = Perceptron()
iterations = nn.train(nand_set, alpha=.2) # alpha is the learning rate
print "Trained in {0} iterations.".format(iterations)
print "Correct?", nn.test(nand_set)
print "Weights: {0}, Threshold: {1}".format(nn.weights, nn.threshold)


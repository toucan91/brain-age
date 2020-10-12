import tensorflow as tf
import numpy as np
import random


class knnGuessNumber:

    def __init__(self, sample=1000):
        # load data
        
        (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
        # Rescale the images from [0,255] to the [0.0,1.0] range.
        x_train, x_test = x_train[..., np.newaxis]/255.0, x_test[..., np.newaxis]/255.0
        
        # randomly select #sample from data loaded
        x = []
        y = []
        for n in range(0, sample):
            i = random.randint(0, sample - 1)
            x.append(np.ravel(x_train[i]))
            y.append(y_train[i])
        
        self.x_train = np.asarray(x)
        self.y_train = np.asarray(y)
        
            
        
    # classifies one example
    def KNN(self, data, k):
        # reshape
        n, d = np.shape(self.x_train)
        # matrix = np.zeros((n,d))
        # matrix[:] = data
     
        # calculate l2 distance
        # distance = np.sqrt(np.sum([(row - data)**2 for row in self.x_train ], axis=1))
        
        # calculate l1 distance
        distance = np.sum(abs(self.x_train - data), axis=1)
        
        # find k neighbours with minimum distance
        min_distance = np.sort(distance)[0:k]
        
        # find indicies of closest k neighbours
        # incase for tie choose first found
        ind = np.zeros(k, dtype=int)
        if k == 1:
            ind = np.where(distance == min_distance)
            ind = ind[0]
        else:
            for i in range(0,k-1):
                ind[i] = np.where(distance == (min_distance[i]))[0][0]
                

        labels = [self.y_train[i] for i in ind]
        y_pred = np.argmax(np.bincount(labels))
        
        return y_pred, labels
    

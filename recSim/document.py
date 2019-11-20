import numpy as np


class Document:

    def __init__(self, T, pTopic, pLength, pQuality):
        """
        Constructor for document class: 
            Sets a topic for the document according to the document 
            distribution
        
        Args
            T : an integer representing the number of potential topics for the document
            pTopic : a numpy ndarray where each index represents the probablity a document
                is about the topic corresponding to that index
            pLength : a scipy distribution function representing the distribution of the length
                of a document
            pQuality : a ndarray of scipy distribution functions representing the distribution
                of the quality of documents about the topic in the corresponding index
        """
        
        topicIndex, topicVector = np.random.choice(a=T,p=pTopic) , np.zeros(T)
        topicVector[topicIndex] = 1
        pTopicQuality = pQuality[topicIndex]

        self.topic =  topicVector
        self.length = pLength.rvs()
        self.quality = pTopicQuality.rvs()

if __name__ == "__main__":
    pass
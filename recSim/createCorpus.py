from document import Document
from probability_distributions import get_normal, get_power_law, get_constant_distribution
from collections import defaultdict
import math
import numpy as np
import logging

def createCorpus(numDocuments, numTopics, pQualityDirection):
    """
    Create a corpus of documents for the simulated RecSys environment
    
    Args:
        numDocument (int) : the numebr of documents in the corpus of items 
            that could be recommended
        numTopics (int) : the number of topics that a document in the corpus 
            could be related to
        pQualityDirection (np.array) : array represnting the probability that
            a document is high/low quality
    
    Returns:
        (dict) Dictionary holding document indices as keys and document objects as values
    """ 

    logging.debug("Creating corpus")
    # storing documents
    documents = defaultdict(None)

    # Sample required distributions
    _, pTopic = get_power_law(2, numTopics)
    pLength = get_constant_distribution(10)
    pQuality = []
    qualityStdev = 2
    # Construct distribution over topic quality
    for _ in range(numTopics):
        qualityDirection = np.random.choice(a=[-3,3], p=pQualityDirection)
        minQuality = min(qualityDirection,0)
        maxQuality = max(qualityDirection,0)
        # sample mean quality uniformly between sampled min and max quality values
        # [-3, 0] if quality direction is negative
        # [0,  3] if quality direction is positive
        meanQuality = np.random.uniform(low=minQuality, high=maxQuality) 
        pQuality.append(get_normal(mean=meanQuality, sd=qualityStdev)) 


    for i in range(numDocuments):
        documents[i] = Document(T=numTopics, pTopic=pTopic, \
                                pLength=pLength, pQuality=pQuality) 

    return documents

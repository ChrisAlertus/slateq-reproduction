from createCorpus import createCorpus
import numpy as np 
import logging

def main():
    numDocuments = 10
    numTopics = 5
    pQualityDirection = np.array([0.7,0.3])    
    
    logging.debug("Foo")
    corpus = createCorpus(numDocuments=numDocuments, numTopics=numTopics,\
                             pQualityDirection=pQualityDirection)
    print(corpus)
    print(f"Document 1: {corpus[0]}")
    print(f"Document 1 topic: {corpus[0].topic}")
    print(f"Document 1 length: {corpus[0].length}")
    print(f"Document 1 quality: {corpus[0].quality}")

    print(f"Document 2: {corpus[1]}")
    print(f"Document 2 topic: {corpus[1].topic}")
    print(f"Document 2 length: {corpus[1].length}")
    print(f"Document 2 quality: {corpus[1].quality}")

if __name__ == "__main__":
    main()
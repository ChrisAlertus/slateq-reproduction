from abc import ABC, abstractmethod
import numpy as np
from document import Document

# v(s,i) where i is the null item, constant for all users
NULL_INTEREST = -0.3

class User(ABC):

    def __init__(self, T, fanatic_ratio=1):
        """
        Constructor for user class: 
            Constructs a new user including their original interests
        
        Args:
            
            T (int) : number of topics that the user could be interested in

            fanatic_ratio (float): a weighting factor that denotes how much the user's 
                satisfaction with a document weighs the quality of the document
                d against their interest in the document. 1 => only care about 
                quality 
            
        Returns
            User (object)
        """
        
        # pInterest: ~U(-1,1)
        self.interests =  np.random.uniform(-1,1,size=T)
        self.fanatic_ratio = fanatic_ratio
        self.nullInterest = NULL_INTEREST
        # static attribute
        self.gender = "male" if np.random.binomial(n=1,p=0.5) == 0 else "female"
        # logging user behaviour history as features
        self.historicalTopicViews = np.zeros(T)
        self.historicalAvgTopicTime = np.zeros(T)
        self.historicalAvgTopicQuality = np.zeros(T)
        self.historicalNumSessions = 0
        self.historicalTimeSpent = 0
        self.historicalAvgBudget = 0
        self.historicalAvgChoicesPerSession = 0.0
        self.historicalMaxChoicesPerSession = 0.0
        self.historicalMinChoicesPerSession = 0.0
        self.historicalNumNullChoice = 0
        self.historicalAvgNullChoicePerSession = 0.0
    
    # user interaction methods
    def inspectDocument(self, document):
        """
        Inspects document and computes an interest value : I(u,d) based on user
        interest compatibility with the document's topic(s)

        Args:
            document(object): object containing the document the user is 
                examining to determine their level of interest

        Returns 
            interestValue (float): scalar measure of the user's interest in document
        """
        
        interestValue = np.dot(self.interests , document.topic)
        return  interestValue

    def computeDocumentSatisfaction(self, document):
        """
        Inspects document and computes satisfaction : S(u,d) based on user
        interest in the document, and the quality of the document

        Args:
            document(object): object containing the document the user is 
                interacting with

        Returns 
            satisfactionValue (float): scalar measure of the user's interest 
            in document
        """

        
        qualityValue = self.fanatic_ratio * document.quality
        interestValue = (1- self.fanatic_ratio) * self.inspectDocument(document)
        # satisfaction is convex sum of interest and doc quality
        satisfactionValue = qualityValue + interestValue
        
        return satisfactionValue

    def userSession(self):
        """
        Let the current user experience a session of being recommended items and
        logging interactions
        """
        pass

    @abstractmethod
    def userChoice(self, recommendations):
        """
        Computes the relative likelihoods of choosing any of the (k+1) 
        options (including null item) presented in a slate of 
        recommendations based on the user's preference

        Args:
            recommendations(list document): a list of document objects 
                that 
        """
        raise NotImplementedError
# 
if __name__ == "__main__":
    pass